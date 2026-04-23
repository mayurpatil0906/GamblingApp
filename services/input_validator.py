import math
from services.validation_exceptions import (
    StakeValidationException,
    BetValidationException,
    LimitValidationException,
    ProbabilityValidationException,
    NumericValidationException,
)
from services.validation_result import ValidationResult
from services.validation_config import ValidationConfig


class InputValidator:
    def __init__(self, config=None):
        self.config = config if config else ValidationConfig()

    def parse_and_validate_numeric(self, value, field_name="numeric_value"):
        if value is None:
            raise NumericValidationException(
                "Value cannot be null",
                field_name=field_name,
                attempted_value=value
            )

        if isinstance(value, str):
            value = value.strip()
            if value == "":
                raise NumericValidationException(
                    "Value cannot be empty",
                    field_name=field_name,
                    attempted_value=value
                )

        try:
            parsed = float(value)
        except (ValueError, TypeError):
            raise NumericValidationException(
                "Invalid numeric input",
                field_name=field_name,
                attempted_value=value
            )

        if math.isnan(parsed):
            raise NumericValidationException(
                "NaN is not allowed",
                field_name=field_name,
                attempted_value=value
            )

        if math.isinf(parsed):
            raise NumericValidationException(
                "Infinity is not allowed",
                field_name=field_name,
                attempted_value=value
            )

        return parsed

    def validate_initial_stake(self, stake):
        stake = self.parse_and_validate_numeric(stake, "initial_stake")

        if not self.config.allow_zero_stake and stake <= 0:
            raise StakeValidationException(
                "Initial stake must be greater than zero",
                field_name="initial_stake",
                attempted_value=stake
            )

        if stake < self.config.min_stake:
            raise StakeValidationException(
                f"Initial stake is below minimum allowed ({self.config.min_stake})",
                field_name="initial_stake",
                attempted_value=stake
            )

        if stake > self.config.max_stake:
            raise StakeValidationException(
                f"Initial stake exceeds maximum allowed ({self.config.max_stake})",
                field_name="initial_stake",
                attempted_value=stake
            )

        return stake

    def validate_bet_amount(self, bet_amount, current_stake, min_bet=None, max_bet=None):
        bet_amount = self.parse_and_validate_numeric(bet_amount, "bet_amount")
        current_stake = self.parse_and_validate_numeric(current_stake, "current_stake")

        min_bet = self.config.min_bet if min_bet is None else float(min_bet)
        max_bet = self.config.max_bet if max_bet is None else float(max_bet)

        if bet_amount <= 0:
            raise BetValidationException(
                "Bet amount must be greater than zero",
                attempted_value=bet_amount
            )

        if bet_amount > current_stake:
            raise BetValidationException(
                "Bet amount cannot exceed current stake",
                attempted_value=bet_amount
            )

        if bet_amount < min_bet:
            raise BetValidationException(
                f"Bet amount is below minimum bet ({min_bet})",
                attempted_value=bet_amount
            )

        if bet_amount > max_bet:
            raise BetValidationException(
                f"Bet amount exceeds maximum bet ({max_bet})",
                attempted_value=bet_amount
            )

        return bet_amount

    def validate_limits(self, lower_limit, upper_limit, initial_stake=None):
        lower_limit = self.parse_and_validate_numeric(lower_limit, "lower_limit")
        upper_limit = self.parse_and_validate_numeric(upper_limit, "upper_limit")

        if lower_limit < 0:
            raise LimitValidationException(
                "Lower limit cannot be negative",
                field_name="lower_limit",
                attempted_value=lower_limit
            )

        if upper_limit < 0:
            raise LimitValidationException(
                "Upper limit cannot be negative",
                field_name="upper_limit",
                attempted_value=upper_limit
            )

        if upper_limit <= lower_limit:
            raise LimitValidationException(
                "Upper limit must be greater than lower limit",
                field_name="limits",
                attempted_value=f"{lower_limit}, {upper_limit}"
            )

        if initial_stake is not None:
            initial_stake = self.parse_and_validate_numeric(initial_stake, "initial_stake")

            if not (lower_limit < initial_stake < upper_limit):
                raise LimitValidationException(
                    "Initial stake must lie between lower and upper limits",
                    field_name="initial_stake",
                    attempted_value=initial_stake
                )

        return lower_limit, upper_limit

    def validate_stake_non_negative(self, stake):
        stake = self.parse_and_validate_numeric(stake, "stake")

        if stake < 0:
            raise StakeValidationException(
                "Stake cannot be negative",
                field_name="stake",
                attempted_value=stake
            )

        if not self.config.allow_zero_stake and stake == 0 and self.config.strict_mode:
            raise StakeValidationException(
                "Zero stake is not allowed in strict mode",
                field_name="stake",
                attempted_value=stake
            )

        return stake

    def validate_probability(self, probability):
        probability = self.parse_and_validate_numeric(probability, "probability")

        if probability < self.config.min_probability or probability > self.config.max_probability:
            raise ProbabilityValidationException(
                "Probability must be between 0 and 1",
                attempted_value=probability
            )

        return probability

    def validate_all(
        self,
        initial_stake=None,
        bet_amount=None,
        current_stake=None,
        lower_limit=None,
        upper_limit=None,
        probability=None
    ):
        result = ValidationResult()

        try:
            if initial_stake is not None:
                self.validate_initial_stake(initial_stake)
        except Exception as e:
            result.add_error(e)

        try:
            if lower_limit is not None and upper_limit is not None:
                self.validate_limits(lower_limit, upper_limit, initial_stake)
        except Exception as e:
            result.add_error(e)

        try:
            if bet_amount is not None and current_stake is not None:
                self.validate_bet_amount(bet_amount, current_stake)
        except Exception as e:
            result.add_error(e)

        try:
            if probability is not None:
                self.validate_probability(probability)
        except Exception as e:
            result.add_error(e)

        return result