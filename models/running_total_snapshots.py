from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class RunningTotalSnapshot:
    snapshot_id: int
    session_id: int
    game_id: int
    total_games: int
    total_wins: int
    total_losses: int
    total_pushes: int
    total_winnings: float
    total_losses_amount: float
    net_profit: float
    win_rate: float
    profit_factor: float
    roi: float
    longest_win_streak: int
    longest_loss_streak: int
    created_at: str = field(default_factory=current_timestamp)