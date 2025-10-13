from asyncio import Semaphore, Lock, create_task, sleep, wait_for, open_connection
from datetime import datetime, timedelta
from itertools import cycle

from src.core.config import Config
from src.core.exceptions import HTTPRequestError
from src.domain.entities.address import AddressDTO
from src.domain.enums.address import HealthStatusEnum


class LoadBalancer:
    def __init__(self, config: Config) -> None:
        self.upstreams = config.upstreams
        self._upstream_cycle = cycle(self.upstreams)

        self._lock = Lock()
        self._global_semaphore = Semaphore(config.limits.max_client_conns)
        self._upstream_semaphores = {
            f"{up.host}:{up.port}": Semaphore(config.limits.max_conns_per_upstream)
            for up in self.upstreams
        }

        self._error_counters = {f"{up.host}:{up.port}": 0 for up in self.upstreams}
        self._circuit_open_until = {f"{up.host}:{up.port}": None for up in self.upstreams}

        self._healthcheck_interval = config.health.interval
        self._healthcheck_timeout = config.health.timeout

        create_task(self._healthcheck_loop())

    async def acquire_next(self) -> tuple[AddressDTO, Semaphore, Semaphore]:
        now = datetime.now()
        async with self._lock:
            for _ in range(len(self.upstreams)):
                upstream = next(self._upstream_cycle)
                key = f"{upstream.host}:{upstream.port}"
                up_sem = self._upstream_semaphores[key]
                open_until = self._circuit_open_until[key]

                if (
                    upstream.status == HealthStatusEnum.DOWN
                    and open_until
                    and open_until > now
                ):
                    continue

                if upstream.status == HealthStatusEnum.UP:
                    return upstream, self._global_semaphore, up_sem

        raise HTTPRequestError("503 Service Unavailable")

    def report_failure(self, up: AddressDTO) -> None:
        key = f"{up.host}:{up.port}"
        self._error_counters[key] += 1

        if self._error_counters[key] >= 2:
            up.status = HealthStatusEnum.DOWN
            cooldown = timedelta(seconds=10)
            self._circuit_open_until[key] = datetime.now() + cooldown

    def report_success(self, up: AddressDTO) -> None:
        up.status = HealthStatusEnum.UP

        key = f"{up.host}:{up.port}"
        self._error_counters[key] = 0
        self._circuit_open_until[key] = None

    async def _healthcheck_loop(self) -> None:
        while True:
            await sleep(self._healthcheck_interval)
            for up in self.upstreams:
                try:
                    reader, writer = await wait_for(
                        open_connection(up.host, up.port),
                        timeout=self._healthcheck_timeout,
                    )
                    writer.close()
                    await writer.wait_closed()
                    self.report_success(up)
                except Exception:  # noqa
                    self.report_failure(up)
