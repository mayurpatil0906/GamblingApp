from enum import Enum


class OddsType(Enum):
    FIXED = "FIXED"
    PROBABILITY_BASED = "PROBABILITY_BASED"
    AMERICAN = "AMERICAN"
    DECIMAL = "DECIMAL"