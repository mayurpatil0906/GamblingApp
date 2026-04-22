from dataclasses import dataclass, field
from typing import Optional
from utils.helpers import current_timestamp


@dataclass
class ValidationEvent:
    validation_id: int
    session_id: Optional[int]
    gambler_id: Optional[int]
    error_type: str
    severity: str
    field_name: str
    attempted_value: str
    message: str
    created_at: str = field(default_factory=current_timestamp)