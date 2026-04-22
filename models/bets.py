from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class Bet:
    bet_id: int
    session_id: int
    gambler_id: int
    strategy_id: int
    game_index: int
    bet_amount: float
    win_probability: float
    odds_type: str
    odds_value: float
    potential_win: float
    stake_before: float
    stake_after: float
    is_settled: bool
    placed_at: str = field(default_factory=current_timestamp)