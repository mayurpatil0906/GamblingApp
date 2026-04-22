from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class OddsConfiguration:
    odds_config_id: int
    odds_type: str
    fixed_multiplier: float
    american_odds: int
    decimal_odds: float
    probability_payout_factor: float
    house_edge: float
    is_default: bool
    created_at: str = field(default_factory=current_timestamp)