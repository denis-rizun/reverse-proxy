from asyncio import StreamReader, StreamWriter, start_server


class FakeUpstream:
    def __init__(self, port: int, alive: bool = True) -> None:
        self.port = port
        self.alive = alive
        self._server = None

    async def start(self) -> None:
        self._server = await start_server(self._handler, "127.0.0.1", self.port)

    async def stop(self) -> None:
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    async def _handler(self, reader: StreamReader, writer: StreamWriter) -> None:
        try:
            await reader.readuntil(b"\r\n\r\n")
            if not self.alive:
                writer.close()
                await writer.wait_closed()
                return

            body = (
                f"HTTP/1.1 200 OK\r\nX-Upstream: {self.port}"
                f"\r\nContent-Length: 2\r\n\r\nOK"
            )
            writer.write(body.encode())
            await writer.drain()

        finally:
            writer.close()
            await writer.wait_closed()

