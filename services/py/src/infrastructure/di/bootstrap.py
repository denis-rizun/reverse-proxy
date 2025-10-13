from pathlib import Path

from src.application.balancer import LoadBalancer
from src.application.limiter.limiter import RateLimiter
from src.application.proxy import Proxy
from src.core.config import Config
from src.delivery.server import Server
from src.infrastructure.config.loader import ConfigLoader
from src.infrastructure.http.network.connector import HttpConnector
from src.infrastructure.http.request.parser import RequestParser


class Bootstrap:

    async def boot(self, path: Path) -> None:
        cfg = self._get_config(path)
        parser = RequestParser()
        balancer = LoadBalancer(cfg)
        limiter = RateLimiter(cfg)
        connector = HttpConnector(cfg, balancer)
        proxy = Proxy(cfg, parser, balancer, limiter, connector)
        srv = Server(cfg, proxy)

        await srv.run()

    @staticmethod
    def _get_config(path: Path) -> Config:
        loader = ConfigLoader(path=path)
        return loader.load()
