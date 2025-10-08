from src.domain.entities.request import RequestDTO
from src.infrastructure.http.network.stream import Stream
from src.infrastructure.http.request.formater import RequestFormatter


class HttpForwarder:

    @staticmethod
    async def forward(
        request: RequestDTO,
        client: Stream,
        upstream: Stream,
        client_ip: str
    ) -> None:
        headers = RequestFormatter.format_headers(request, client_ip)
        await HttpForwarder._forward_headers(request, upstream, headers)
        await HttpForwarder._forward_body(headers, client, upstream)

    @staticmethod
    async def _forward_headers(request: RequestDTO, upstream: Stream, headers) -> None:
        new_line = f"{request.build_line()}\r\n"
        await upstream.write(data=new_line.encode())
        for k, v in headers.items():
            await upstream.write(data=f"{k}: {v}\r\n".encode())

        await upstream.write(data=b"\r\n", is_drain=True)

    @staticmethod
    async def _forward_body(headers: dict[str, str], client: Stream, upstream: Stream) -> None:
        if "content-length" in headers:
            remaining = int(headers["content-length"])
            while remaining > 0:
                chunk = await client.read(min(8192, remaining))
                if not chunk:
                    break
                await upstream.write(chunk, is_drain=True)
                remaining -= len(chunk)

        elif headers.get("transfer-encoding") == "chunked":
            while True:
                line = await client.readline()
                if not line:
                    break

                await upstream.write(line, is_drain=True)
                size = int(line.strip(), 16)
                if size == 0:
                    break

                chunk = await client.read_exactly(size + 2)
                await upstream.write(chunk, is_drain=True)
