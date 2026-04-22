from dataclasses import dataclass, field
from typing import Optional
from utils.helpers import current_timestamp


@dataclass
class PauseRecord:
    pause_id: int
    session_id: int
    pause_reason: str
    paused_at: str = field(default_factory=current_timestamp)
    resumed_at: Optional[str] = None
    pause_seconds: int = 0