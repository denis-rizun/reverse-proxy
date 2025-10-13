import asyncio

from src.application.balancer import LoadBalancer
from src.application.limiter.limiter import RateLimiter
from src.core.config import Config
from src.core.exceptions import HTTPRequestError
from src.core.logger import Logger
from src.core.timer import Timer
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

    async def handle_request(self, client: Stream) -> bool:
        client_ip, allowed = await self._check_limits(client)
        if not allowed:
            return False

        timer = Timer.get_timer()

        async with timer.timed("st_read", "end_read"):
            request = await self._parser.receive_request(client)
            if not request.method:
                return False

        for _ in range(len(self._balancer.upstreams)):
            upstream, global_sem, up_sem = await self._balancer.acquire_next()

            if global_sem._value <= 0 or up_sem._value <= 0:  # noqa
                continue

            try:
                async with global_sem, up_sem:
                    up_stream = await self._connector.connect(upstream)

                    async with timer.timed("st_forward", "end_forward"):
                        await HttpForwarder.forward(request, client, up_stream, client_ip)

                    async with timer.timed("st_ttfb", "end_ttfb"):
                        first_chunk = await up_stream.read(1)

                    stream_task = asyncio.create_task(client.stream_from(up_stream, first_chunk))
                    client.track_task(stream_task)

                timer.log_time(request.build_line(), upstream)
                return True

            except (TimeoutError, OSError):
                logger.warning("Upstream %s failed, trying next...", upstream)
                continue

        raise HTTPRequestError("503 Service Unavailable")

    async def _check_limits(self, client: Stream) -> tuple[str, bool]:
        client_ip = client.get_client_ip()
        allowed = await self._limiter.allow(client_ip)
        if not allowed:
            await client.write(b"HTTP/1.1 429 Too Many Requests\r\n\r\n", is_drain=True)

        return client_ip, allowed
