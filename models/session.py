from dataclasses import dataclass, field
from typing import Optional
from utils.helpers import current_timestamp


@dataclass
class Session:
    session_id: int
    gambler_id: int
    status: str
    end_reason: Optional[str]
    starting_stake: float
    ending_stake: float
    peak_stake: float
    lowest_stake: float
    max_games: int
    games_played: int
    total_pause_seconds: int
    started_at: str = field(default_factory=current_timestamp)
    ended_at: Optional[str] = None
    created_at: str = field(default_factory=current_timestamp)