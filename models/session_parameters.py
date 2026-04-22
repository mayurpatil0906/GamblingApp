from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class SessionParameters:
    parameter_id: int
    session_id: int
    lower_limit: float
    upper_limit: float
    min_bet: float
    max_bet: float
    default_win_probability: float
    max_session_minutes: int
    strict_mode: bool
    created_at: str = field(default_factory=current_timestamp)