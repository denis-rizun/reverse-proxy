from dataclasses import dataclass

from src.domain.entities.health import HealthDTO
from src.domain.entities.limit import LimitsDTO
from src.domain.entities.rate import RateLimitDTO
from src.domain.entities.timeout import TimeoutsDTO
from src.domain.entities.address import AddressDTO


@dataclass
class Config:
    listen: AddressDTO
    upstreams: list[AddressDTO]
    timeouts: TimeoutsDTO
    limits: LimitsDTO
    logging_level: str
    rate_limits: RateLimitDTO
    health: HealthDTO
