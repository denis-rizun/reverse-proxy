from asyncio import run
from pathlib import Path

from py_v.src.core.config import Config
from py_v.src.core.logger import Logger
from py_v.src.services.balancer import LoadBalancer
from py_v.src.services.proxy import Proxy
from py_v.src.transport.parser import RequestParser
from py_v.src.transport.server import Server

BASE_DIR = Path(__file__).resolve().parent.parent


async def main() -> None:
    cfg = Config(BASE_DIR / "config.yml")
    logger = Logger.setup(cfg.logging.level)
    logger.info(f"Booted {cfg.upstreams!r}")


    load_balancer = LoadBalancer(cfg)
    parser = RequestParser()
    proxy = Proxy(cfg, logger, parser, load_balancer)

    server = Server(cfg, proxy, logger)
    await server.run()


if __name__ == "__main__":
    run(main())
