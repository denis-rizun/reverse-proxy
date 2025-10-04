from typing import Any


class UpstreamDTO:
    def __init__(self, upstream: dict[str, Any]) -> None:
        self.host = upstream["host"]
        self.port = upstream["port"]
