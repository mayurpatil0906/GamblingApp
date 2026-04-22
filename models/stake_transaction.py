from dataclasses import dataclass, field
from typing import Optional
from utils.helpers import current_timestamp


@dataclass
class StakeTransaction:
    transaction_id: int
    gambler_id: int
    session_id: Optional[int]
    bet_id: Optional[int]
    transaction_type: str
    amount: float
    balance_before: float
    balance_after: float
    created_at: str = field(default_factory=current_timestamp)