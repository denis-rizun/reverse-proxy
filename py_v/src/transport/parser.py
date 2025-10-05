from asyncio import StreamReader

from py_v.src.core.exceptions import HTTPInvalidRequestError
from py_v.src.dtos.request import RequestDTO


class RequestParser:

    async def receive_request(self, reader: StreamReader) -> RequestDTO:
        request_line = await reader.readline()
        if not request_line:
            return RequestDTO(None, None, None, None)

        method, path, version = self._decode_request_line(request_line)
        headers = await self._decode_headers(reader)

        return RequestDTO(method, path, version, headers)

    @staticmethod
    def _decode_request_line(request_line: bytes) -> tuple[str, str, str]:
        request_line = request_line.decode().strip()
        parts = request_line.split()
        if len(parts) != 3:
            raise HTTPInvalidRequestError(f"Invalid HTTP request line: {request_line}")

        return parts

    @staticmethod
    async def _decode_headers(reader: StreamReader) -> dict[str, str]:
        headers = {}
        while True:
            line = await reader.readline()
            if not line:
                break

            line = line.decode().strip()
            if not line:
                break

            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

        return headers
