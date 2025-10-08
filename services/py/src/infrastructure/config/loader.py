from json import load
from pathlib import Path
from typing import Any

from yaml import safe_load

from src.core.config import Config
from src.domain.entities.address import AddressDTO
from src.domain.entities.health import HealthDTO
from src.domain.entities.limit import LimitsDTO
from src.domain.entities.rate import RateLimitDTO
from src.domain.entities.timeout import TimeoutsDTO
from src.core.exceptions import (
    ConfigNotFoundError,
    ConfigNotSupportTypeError,
    ConfigMissingRequiredKeyError
)


class ConfigLoader:
    REQUIRED_KEYS = ["listen", "upstreams"]
    DEFAULTS = {
        "timeouts": {
            "connect_ms": 1000,
            "read_ms": 15000,
            "write_ms": 15000,
            "total_ms": 30000
        },
        "limits": {"max_client_conns": 1000, "max_conns_per_upstream": 100},
        "logging": {"level": "info"},
        "rate_limits": {"rate": 100, "capacity": 1000, "per_upstream": False},
        "health_check": {"interval": 100, "timeout": 5},
    }

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> Config:
        storage = self._read()
        return Config(
            listen=AddressDTO(storage["listen"][0]),
            upstreams=[AddressDTO(stream) for stream in storage["upstreams"]],
            timeouts=TimeoutsDTO(storage["timeouts"]),
            limits=LimitsDTO(storage["limits"]),
            logging_level=storage["logging"],
            rate_limits=RateLimitDTO(storage["rate_limits"]),
            health=HealthDTO(storage["health_check"]),
        )

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            raise ConfigNotFoundError(f"Configuration file not found: {self.path}")

        suffix = self.path.suffix.lower()
        if suffix in (".yaml", ".yml"):
            loaded = self._load_yaml()
        elif suffix == ".json":
            loaded = self._load_json()
        else:
            raise ConfigNotSupportTypeError(f"Unsupported config file type: {suffix}")

        for key in self.REQUIRED_KEYS:
            if key not in loaded:
                raise ConfigMissingRequiredKeyError(f"Missing required config key: {key}")

        return {**self.DEFAULTS, **loaded}

    def _load_yaml(self) -> dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as f:
            return safe_load(f) or {}

    def _load_json(self) -> dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as f:
            return load(f)
