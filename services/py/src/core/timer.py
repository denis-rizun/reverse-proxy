from contextlib import asynccontextmanager
from time import perf_counter
from typing import AsyncGenerator

from src.core.logger import Logger
from src.domain.entities.address import AddressDTO

logger = Logger.setup()


class Timer:
    def __init__(self) -> None:
        self._marks = {}

    def mark(self, name: str) -> None:
        self._marks[name] = perf_counter()

    def elapsed_ms(self, start_name: str, end_name: str) -> float:
        return (self._marks[end_name] - self._marks[start_name]) * 1000

    def log_time(self, metadata: str, upstream: AddressDTO) -> None:
        logger.info(
            f"{metadata} | {upstream.host}:{upstream.port} | "
            f"R:{self.elapsed_ms('st_read', 'end_read'):.1f}ms "
            f"F:{self.elapsed_ms('st_forward', 'end_forward'):.1f}ms "
            f"TTFB:{self.elapsed_ms('st_ttfb', 'end_ttfb'):.1f}ms "
        )

    @asynccontextmanager
    async def timed(self, s: str, e: str) -> AsyncGenerator:
        self.mark(s)
        yield
        self.mark(e)

    @classmethod
    def get_timer(cls) -> "Timer":
        return Timer()
