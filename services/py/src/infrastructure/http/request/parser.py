from src.core.exceptions import HTTPInvalidRequestError
from src.domain.entities.request import RequestDTO
from src.infrastructure.http.network.stream import Stream


class RequestParser:

    async def receive_request(self, client: Stream) -> RequestDTO:
        request_line = await client.readline()
        if not request_line:
            return RequestDTO(None, None, None, None)

        method, path, version = self._decode_request_line(request_line)
        headers = await self._decode_headers(client)

        return RequestDTO(method, path, version, headers)

    @staticmethod
    def _decode_request_line(request_line: bytes) -> tuple[str, str, str]:
        request_line = request_line.decode().strip()
        parts = request_line.split()
        if len(parts) != 3:
            raise HTTPInvalidRequestError(f"Invalid HTTP request line: {request_line}")

        return parts

    @staticmethod
    async def _decode_headers(client: Stream) -> dict[str, str]:
        headers = {}
        while True:
            line = await client.readline()
            if not line:
                break

            line = line.decode().strip()
            if not line:
                break

            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

        return headers
