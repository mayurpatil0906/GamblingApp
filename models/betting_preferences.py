from dataclasses import dataclass, field
from utils.helpers import current_timestamp


@dataclass
class BettingPreferences:
    preference_id: int
    gambler_id: int
    min_bet: float
    max_bet: float
    preferred_game_type: str
    auto_play_enabled: bool
    auto_play_max_games: int
    session_loss_limit: float
    session_win_target: float
    updated_at: str = field(default_factory=current_timestamp)