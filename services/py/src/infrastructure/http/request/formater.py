from typing import Any

from src.domain.entities.request import RequestDTO


class RequestFormatter:
    HEADERS_HOP_BY_HOP_KEYS = {
        "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
        "te", "trailers", "transfer-encoding", "upgrade", "proxy-connection"
    }

    @classmethod
    def format_headers(cls, rq: RequestDTO, client_ip: str) -> dict[str, Any]:
        headers = dict(rq.headers)
        if client_ip:
            if "x-forwarded-for" in headers:
                headers["x-forwarded-for"] += f", {client_ip}"
            else:
                headers["x-forwarded-for"] = client_ip

        via = "1.1 my-proxy"
        if "via" in headers:
            headers["via"] += f", {via}"
        else:
            headers["via"] = via

        headers["connection"] = "keep-alive"

        for h in list(headers.keys()):
            if h.lower() in cls.HEADERS_HOP_BY_HOP_KEYS:
                headers.pop(h, None)

        return headers
