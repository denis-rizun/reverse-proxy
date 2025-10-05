from asyncio import StreamReader, StreamWriter, wait_for, create_task, open_connection
from logging import Logger

from py_v.src.core.config import Config
from py_v.src.core.exceptions import HTTPRequestError, HTTPError
from py_v.src.dtos.address import AddressDTO
from py_v.src.dtos.request import RequestDTO
from py_v.src.services.balancer import LoadBalancer
from py_v.src.services.timer import Timer
from py_v.src.transport.parser import RequestParser


class Proxy:
    def __init__(
        self,
        config: Config,
        logger: Logger,
        parser: RequestParser,
        balancer: LoadBalancer,
    ) -> None:
        self.logger = logger
        self._config = config
        self._parser = parser
        self._balancer = balancer

    async def handle_request(self, r: StreamReader, w: StreamWriter) -> bool:
        timer = Timer()
        timer.mark("start_read")
        request = await self._parser.receive_request(r)
        timer.mark("end_read")

        if not request.method:
            return False

        request_metadata = f"{request.method} {request.path} {request.version}"
        upstream, global_sem, up_sem = await self._balancer.acquire_next()

        async with global_sem, up_sem:
            up_writer = None
            try:
                up_reader, up_writer = await self._connect_to_upstream(upstream)

                timer.mark("start_forward")
                await self._forward_headers(f"{request_metadata}\r\n", up_writer, request)
                await self._forward_body(request.headers, r, up_writer)
                timer.mark("end_forward")

                timer.mark("start_ttfb")
                first_chunk = await up_reader.read(1)
                timer.mark("end_ttfb")

                timer.mark("start_stream")
                _ = create_task(self._stream_response(up_reader, w, first_chunk))
                timer.mark("end_stream")

            finally:
                if up_writer:
                    up_writer.close()
                    await up_writer.wait_closed()

        self._log_response_time(request_metadata, upstream, timer)
        return True

    @staticmethod
    async def _stream_response(
        up_r: StreamReader,
        cl_w: StreamWriter,
        first_chunk: bytes
    ) -> None:
        try:
            cl_w.write(first_chunk)
            await cl_w.drain()

            while True:
                chunk = await up_r.read(8192)
                if not chunk:
                    break

                cl_w.write(chunk)
                await cl_w.drain()

        except Exception as e:
            raise HTTPRequestError(e) from e

        finally:
            try:
                cl_w.write_eof()
            except Exception as e:
                raise HTTPError(e) from e

    async def _connect_to_upstream(self, up: AddressDTO) -> tuple[StreamReader, StreamWriter]:
        return await wait_for(
            open_connection(up.host, up.port),
            timeout=self._config.timeouts.connect_ms
        )

    @staticmethod
    async def _forward_headers(md: str, up_w: StreamWriter, request: RequestDTO) -> None:
        up_w.write(md.encode())
        for k, v in request.headers.items():
            up_w.write(f"{k}: {v}\r\n".encode())

        up_w.write(b"\r\n")
        await up_w.drain()

    @staticmethod
    async def _forward_body(
        headers: dict[str, str],
        cl_r: StreamReader,
        up_w: StreamWriter
    ) -> None:
        if "content-length" in headers:
            remaining = int(headers["content-length"])
            while remaining > 0:
                chunk = await cl_r.read(min(8192, remaining))  # noqa
                if not chunk:
                    break

                up_w.write(chunk)
                await up_w.drain()
                remaining -= len(chunk)

        elif headers.get("transfer-encoding") == "chunked":
            while True:
                line = await cl_r.readline()
                if not line:
                    break

                up_w.write(line)
                await up_w.drain()
                size = int(line.strip(), 16)
                if size == 0:
                    break

                chunk = await cl_r.readexactly(size + 2)
                up_w.write(chunk)
                await up_w.drain()

    def _log_response_time(self, metadata: str, upstream: AddressDTO, timer: Timer) -> None:
        self.logger.info(
            f"{metadata} | {upstream.host}:{upstream.port} | "
            f"R:{timer.elapsed_ms('start_read', 'end_read'):.1f}ms "
            f"F:{timer.elapsed_ms('start_forward', 'end_forward'):.1f}ms "
            f"TTFB:{timer.elapsed_ms('start_ttfb', 'end_ttfb'):.1f}ms "
            f"S:{timer.elapsed_ms('start_stream', 'end_stream'):.1f}ms"
        )
