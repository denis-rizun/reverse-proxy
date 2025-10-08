from asyncio import StreamReader, StreamWriter

from src.core.exceptions import HTTPRequestError


class Stream:
    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

    def get_client_ip(self) -> str:
        peername = self.writer.get_extra_info("peername")
        return peername[0] if peername else "unknown"

    async def write(self, data: bytes, is_drain: bool = False) -> None:
        self.writer.write(data)
        if is_drain:
            await self.writer.drain()

    async def read(self, n: int = 8192) -> bytes:
        return await self.reader.read(n)

    async def readline(self) -> bytes:
        return await self.reader.readline()

    async def read_exactly(self, n: int) -> bytes:
        return await self.reader.readexactly(n)

    async def close(self):
        if not self.writer.is_closing():
            try:
                self.writer.write_eof()
            except Exception:  # noqa
                pass
            finally:
                self.writer.close()
                await self.writer.wait_closed()

    async def stream_from(self, source: 'Stream', first_chunk: bytes) -> None:
        try:
            if first_chunk and not self.writer.is_closing():
                await self.write(first_chunk)

            while True:
                chunk = await source.read(8192)
                if not chunk or self.writer.is_closing():
                    break

                await self.write(chunk, is_drain=True)
        except HTTPRequestError:
            pass
        finally:
            await self.close()
