from json import load
from pathlib import Path
from typing import Any

from yaml import safe_load

from py_v.src.core.exceptions import (
    ConfigNotFoundError,
    ConfigNotSupportTypeError,
    ConfigMissingRequiredKeyError
)
from py_v.src.dtos.limit import LimitsDTO
from py_v.src.dtos.logging import LoggingDTO
from py_v.src.dtos.timeout import TimeoutsDTO
from py_v.src.dtos.upstream import UpstreamDTO


class Config:
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
    }

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.listen = None
        self.upstreams = None
        self.timeouts = None
        self.limits = None
        self.logging = None
        self.load()

    def load(self) -> None:
        storage = self._read()
        self.listen = storage["listen"]
        self.upstreams = [UpstreamDTO(stream) for stream in storage["upstreams"]]
        self.timeouts = TimeoutsDTO(storage["timeouts"])
        self.limits = LimitsDTO(storage["limits"])
        self.logging = LoggingDTO(storage["logging"])

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
