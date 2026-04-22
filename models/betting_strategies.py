from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class BettingStrategy:
    strategy_id: int
    strategy_name: str
    description: str
    is_active: bool
    created_at: str = field(default_factory=current_timestamp)