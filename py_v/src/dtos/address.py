from typing import Any


class AddressDTO:
    def __init__(self, address: dict[str, Any] | list[str]) -> None:
        if isinstance(address, list):
            host, port = address
        else:
            host, port = address["host"], address["port"]

        self.host = str(host)
        self.port = int(port)

    def __repr__(self) -> str:
        return f"<Address(h={self.host}, p={self.port})>"
