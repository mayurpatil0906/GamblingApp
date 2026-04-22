from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class Gambler:
    gambler_id: int
    username: str
    full_name: str
    email: str
    is_active: bool
    initial_stake: float
    current_stake: float
    win_threshold: float
    loss_threshold: float
    min_required_stake: float
    created_at: str = field(default_factory=current_timestamp)
    updated_at: str = field(default_factory=current_timestamp)