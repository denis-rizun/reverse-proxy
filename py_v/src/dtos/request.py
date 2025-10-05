from typing import Any


class RequestDTO:
    def __init__(
        self,
        method: str | None,
        path: str | None,
        version: str | None,
        headers: dict[str, Any] | None
    ) -> None:
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
