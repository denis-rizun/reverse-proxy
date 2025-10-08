from typing import Any


class TimeoutsDTO:
    def __init__(self, timeouts: dict[str, Any]) -> None:
        self.connect_ms = timeouts["connect_ms"]
        self.read_ms = timeouts["read_ms"]
        self.write_ms = timeouts["write_ms"]
        self.total_ms = timeouts["total_ms"]

    def to_seconds(self) -> dict[str, int]:
        return {k: v / 1000 for k, v in self.__dict__.items()}
