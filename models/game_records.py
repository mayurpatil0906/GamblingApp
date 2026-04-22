from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class GameRecord:
    game_id: int
    session_id: int
    bet_id: int
    odds_config_id: int
    outcome: str
    payout_amount: float
    loss_amount: float
    net_change: float
    stake_before: float
    stake_after: float
    consecutive_win_streak: int
    consecutive_loss_streak: int
    game_duration_seconds: int
    resolved_at: str = field(default_factory=current_timestamp)