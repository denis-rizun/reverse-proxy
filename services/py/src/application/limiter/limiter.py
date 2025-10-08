from collections import defaultdict

from src.application.limiter.bucket import TokenBucket
from src.core.config import Config


class RateLimiter:
    def __init__(self, cfg: Config) -> None:
        rate, capacity = cfg.rate_limits.rate, cfg.rate_limits.capacity

        self.per_upstream = cfg.rate_limits.per_upstream
        self.global_bucket = TokenBucket(rate, capacity)
        self.client_buckets = defaultdict(lambda: TokenBucket(rate, capacity))

    async def allow(self, client_ip: str | None = None) -> bool:
        if self.per_upstream and client_ip:
            bucket = self.client_buckets[client_ip]
            return await bucket.consume()
        else:
            return await self.global_bucket.consume()
