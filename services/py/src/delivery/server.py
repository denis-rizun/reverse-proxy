from asyncio import start_server, StreamReader, StreamWriter

from src.application.proxy import Proxy
from src.core.config import Config
from src.core.logger import Logger
from src.infrastructure.http.network.stream import Stream

logger = Logger.setup()


class Server:
    def __init__(self, cfg: Config, proxy: Proxy) -> None:
        self._host = cfg.listen.host
        self._port = cfg.listen.port
        self._proxy = proxy

    async def run(self) -> None:
        srv = await start_server(self._handle_client, self._host, self._port)
        async with srv:
            logger.info(f"Listening on {self._host}:{self._port}")
            await srv.serve_forever()

    async def _handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        client_stream = Stream(reader, writer)
        try:
            while True:
                keep_alive = await self._proxy.handle_request(client_stream)
                if not keep_alive:
                    break
        finally:
            writer.close()
            await writer.wait_closed()
