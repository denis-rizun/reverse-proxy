from asyncio import Semaphore, Lock
from itertools import cycle

from py_v.src.core.config import Config
from py_v.src.dtos.address import AddressDTO


class LoadBalancer:
    def __init__(self, config: Config) -> None:
        self._upstreams = config.upstreams
        self._upstream_cycle = cycle(config.upstreams)
        self._lock = Lock()
        self._global_semaphore = Semaphore(config.limits.max_client_conns)
        self._upstream_semaphores = {
            f"{up.host}:{up.port}": Semaphore(config.limits.max_conns_per_upstream)
            for up in config.upstreams
        }

    async def acquire_next(self) -> tuple[AddressDTO, Semaphore, Semaphore]:
        async with self._lock:
            upstream = next(self._upstream_cycle)

        up_sem = self._upstream_semaphores[f"{upstream.host}:{upstream.port}"]
        return upstream, self._global_semaphore, up_sem
