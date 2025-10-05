from asyncio import start_server, StreamReader, StreamWriter
from logging import Logger
from py_v.src.core.config import Config
from py_v.src.services.proxy import Proxy


class Server:
    def __init__(self, config: Config, proxy: Proxy, logger: Logger) -> None:
        self._host = config.listen.host
        self._port = config.listen.port
        self._proxy = proxy
        self._logger = logger

    async def run(self) -> None:
        srv = await start_server(self._handle_client, self._host, self._port)
        async with srv:
            await srv.serve_forever()

    async def _handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        try:
            while True:
                keep_alive = await self._proxy.handle_request(reader, writer)
                if not keep_alive:
                    break
        finally:
            writer.close()
            await writer.wait_closed()
