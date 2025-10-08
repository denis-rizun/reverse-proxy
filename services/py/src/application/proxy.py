import asyncio

from src.application.balancer import LoadBalancer
from src.application.limiter.limiter import RateLimiter
from src.core.config import Config
from src.core.exceptions import HTTPRequestError
from src.core.logger import Logger
from src.core.timer import Timer
from src.domain.entities.metrics import metrics_storage
from src.infrastructure.http.network.connector import HttpConnector
from src.infrastructure.http.network.forwarder import HttpForwarder
from src.infrastructure.http.network.stream import Stream
from src.infrastructure.http.request.parser import RequestParser

logger = Logger.setup()


class Proxy:
    def __init__(
        self,
        cfg: Config,
        parser: RequestParser,
        balancer: LoadBalancer,
        limiter: RateLimiter,
        connector: HttpConnector,
    ) -> None:
        self._config = cfg
        self._parser = parser
        self._balancer = balancer
        self._limiter = limiter
        self._connector = connector
        self.metrics = metrics_storage

    async def handle_request(self, client: Stream) -> bool:
        client_ip, allowed = await self._check_limits(client)
        if not allowed:
            return False

        self.metrics.total_requests += 1
        self.metrics.requests_per_ip[client_ip] += 1
        timer = Timer.get_timer()

        async with timer.timed("st_read", "end_read"):
            request = await self._parser.receive_request(client)
            if not request.method:
                return False

        upstream, global_sem, up_sem = await self._balancer.acquire_next()
        if global_sem._value <= 0 or up_sem._value <= 0:
            raise HTTPRequestError("503 Service Unavailable")

        try:
            async with global_sem, up_sem:
                up_stream = await self._connector.connect(upstream)

                async with timer.timed("st_forward", "end_forward"):
                    await HttpForwarder.forward(request, client, up_stream, client_ip)

                async with timer.timed("st_ttfb", "end_ttfb"):
                    first_chunk = await up_stream.read(1)

                asyncio.create_task(client.stream_from(up_stream, first_chunk))

        except TimeoutError:
            raise HTTPRequestError("503 Service Unavailable")

        timer.log_time(request.build_line(), upstream)
        return True

    async def _check_limits(self, client: Stream) -> tuple[str, bool]:
        client_ip = client.get_client_ip()
        allowed = await self._limiter.allow(client_ip)
        if not allowed:
            await client.write(b"HTTP/1.1 429 Too Many Requests\r\n\r\n", is_drain=True)

        return client_ip, allowed
