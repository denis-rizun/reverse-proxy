from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MetricsDTO:
    total_requests: int = 0
    requests_per_ip: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    upstream_status: dict[str, str] = field(default_factory=dict)
    global_semaphore_count: int = 0
    upstream_semaphores_count: dict[str, int] = field(default_factory=dict)


metrics_storage = MetricsDTO()
