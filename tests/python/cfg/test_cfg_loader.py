from pathlib import Path

import pytest
from yaml import safe_dump
from py_v.src.core.config import Config
from py_v.src.core.exceptions import (
    ConfigNotSupportTypeError,
    ConfigNotFoundError,
    ConfigMissingRequiredKeyError
)


class TestConfigLoader:

    def test_success(self, tmp_path: Path) -> None:
        data = {
            "listen": "127.0.0.1:8000",
            "upstreams": [{"host": "127.0.0.1", "port": 9000}],
            "timeouts": {
                "connect_ms": 2000,
                "read_ms": 20000,
                "write_ms": 20000,
                "total_ms": 40000
            },
            "limits": {"max_client_conns": 2000, "max_conns_per_upstream": 200},
            "logging": {"level": "debug"},
        }
        file_path = tmp_path / "config.yaml"
        file_path.write_text(safe_dump(data))

        cfg = Config(file_path)

        assert cfg.listen.host == "127.0.0.1"
        assert len(cfg.upstreams) == 1
        assert cfg.timeouts.connect_ms == 2000
        assert cfg.limits.max_client_conns == 2000
        assert cfg.logging.level == "debug"

    def test_success__default_params(self, tmp_path: Path) -> None:
        data = {
            "listen": "127.0.0.1:8000",
            "upstreams": [{"host": "127.0.0.1", "port": 9000}],
        }
        file_path = tmp_path / "config.yaml"
        file_path.write_text(safe_dump(data))

        cfg = Config(file_path)

        assert cfg.listen.host == "127.0.0.1"
        assert len(cfg.upstreams) == 1
        assert cfg.timeouts.connect_ms == Config.DEFAULTS["timeouts"]["connect_ms"]
        assert cfg.limits.max_client_conns == Config.DEFAULTS["limits"]["max_client_conns"]
        assert cfg.logging.level == Config.DEFAULTS["logging"]["level"]

    def test_failed__not_found_file(self) -> None:
        with pytest.raises(ConfigNotFoundError):
            Config("not_exists.yaml")

    def test_failed__not_support_type(self, tmp_path: Path) -> None:
        file_path = tmp_path / "config.txt"
        file_path.write_text("unsupported content")
        with pytest.raises(ConfigNotSupportTypeError):
            Config(file_path)

    def test_failed__missing_required_key(self, tmp_path: Path) -> None:
        data = {"timeouts": {"connect_ms": 1000}}
        file_path = tmp_path / "config.yaml"
        file_path.write_text(safe_dump(data))

        with pytest.raises(ConfigMissingRequiredKeyError):
            Config(file_path)
