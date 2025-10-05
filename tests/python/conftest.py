import asyncio
from asyncio import create_task, sleep
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from yaml import safe_dump

from py_v.src.core.config import Config
from py_v.src.core.logger import Logger
from py_v.src.services.balancer import LoadBalancer
from py_v.src.services.proxy import Proxy
from py_v.src.transport.parser import RequestParser
from py_v.src.transport.server import Server
from tests.python.http.conftest import FakeUpstream


class GlobalConftest:
    HOST = "127.0.0.1"
    PORT = 8081

    @staticmethod
    def load_temp_config(path: Path, data: dict[str, Any]) -> Config:
        file_path = path / "config.yaml"
        file_path.write_text(safe_dump(data))
        return Config(file_path)

    @staticmethod
    def get_cfg_data_for_proxy(up_s: list[FakeUpstream]) -> dict[str, Any]:
        return {
            "listen": f"127.0.0.1:{GlobalConftest.PORT}",
            "upstreams": [{"host": "127.0.0.1", "port": u.port} for u in up_s],
            "limits": {"max_client_conns": 10, "max_conns_per_upstream": 10},
            "timeouts": {"connect_ms": 500, "read_ms": 500, "write_ms": 500, "total_ms": 1000},
            "logging": {"level": "INFO"},
        }

    @staticmethod
    @asynccontextmanager
    async def running_server(tmp_path: Path) -> None:
        up1 = FakeUpstream(port=9001, alive=True)
        up2 = FakeUpstream(port=9002, alive=True)
        await up1.start()
        await up2.start()

        data = GlobalConftest.get_cfg_data_for_proxy([up1, up2])
        config = GlobalConftest.load_temp_config(tmp_path, data)
        logger = Logger.setup(config.logging.level)
        proxy = Proxy(config, logger, RequestParser(), LoadBalancer(config))
        server = Server(config, proxy, logger)

        task = create_task(server.run())
        await sleep(0.2)

        yield

        task.cancel()
        await up1.stop()
        await up2.stop()

    @staticmethod
    async def send_request(url: str = "/") -> str:
        r, w = await asyncio.open_connection(GlobalConftest.HOST, GlobalConftest.PORT)
        w.write(f"GET {url} HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())
        await w.drain()
        resp = await r.read(1024)
        w.close()
        await w.wait_closed()
        return resp.decode()
