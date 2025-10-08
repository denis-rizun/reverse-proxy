from typing import Any


class LimitsDTO:
    def __init__(self, limits: dict[str, Any]) -> None:
        self.max_client_conns = limits["max_client_conns"]
        self.max_conns_per_upstream = limits["max_conns_per_upstream"]
