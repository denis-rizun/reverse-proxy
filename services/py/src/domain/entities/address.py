from typing import Any

from src.domain.enums.address import HealthStatusEnum


class AddressDTO:
    def __init__(self, address: dict[str, Any]) -> None:
        self.host = address["host"]
        self.port = address["port"]
        self.status = HealthStatusEnum.UP
        self.timeout = None

    def __repr__(self) -> str:
        return f"<Address(h={self.host}, p={self.port}, s={self.status})>"
