from asyncio import wait_for, open_connection

from src.application.balancer import LoadBalancer
from src.core.config import Config
from src.domain.entities.address import AddressDTO
from src.infrastructure.http.network.stream import Stream


class HttpConnector:
    def __init__(self, cfg: Config, balancer: LoadBalancer) -> None:
        self._cfg = cfg
        self._balancer = balancer

    async def connect(self, addr: AddressDTO) -> Stream:
        try:
            r, w = await wait_for(
                open_connection(addr.host, addr.port),
                timeout=self._cfg.timeouts.connect_ms
            )
            return Stream(r, w)
        except (TimeoutError, ConnectionRefusedError):
            self._balancer.report_failure(addr)
            raise
