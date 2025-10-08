from typing import Any


class RateLimitDTO:
    def __init__(self, rates: dict[str, Any]) -> None:
        self.rate = rates["rate"]
        self.capacity = rates["capacity"]
        self.per_upstream = rates["per_upstream"]
