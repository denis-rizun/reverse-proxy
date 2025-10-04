from typing import Any


class LoggingDTO:
    def __init__(self, logging: dict[str, Any]) -> None:
        self.level = logging["level"]
