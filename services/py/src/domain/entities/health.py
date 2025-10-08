from typing import Any


class HealthDTO:
    def __init__(self, check: dict[str, Any]) -> None:
        self.interval = check["interval"]
        self.timeout = check["timeout"]
