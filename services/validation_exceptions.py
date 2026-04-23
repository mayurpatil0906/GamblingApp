from models.validation_error_type import ValidationErrorType


class ValidationException(Exception):
    def __init__(self, message, error_type, field_name=None, attempted_value=None):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.field_name = field_name
        self.attempted_value = attempted_value

    def __str__(self):
        return (
            f"{self.message} | "
            f"error_type={self.error_type.value} | "
            f"field={self.field_name} | "
            f"attempted_value={self.attempted_value}"
        )


class StakeValidationException(ValidationException):
    def __init__(self, message, field_name="stake", attempted_value=None):
        super().__init__(
            message,
            ValidationErrorType.STAKE_ERROR,
            field_name,
            attempted_value
        )


class BetValidationException(ValidationException):
    def __init__(self, message, field_name="bet_amount", attempted_value=None):
        super().__init__(
            message,
            ValidationErrorType.BET_ERROR,
            field_name,
            attempted_value
        )


class LimitValidationException(ValidationException):
    def __init__(self, message, field_name="limits", attempted_value=None):
        super().__init__(
            message,
            ValidationErrorType.LIMIT_ERROR,
            field_name,
            attempted_value
        )


class ProbabilityValidationException(ValidationException):
    def __init__(self, message, field_name="probability", attempted_value=None):
        super().__init__(
            message,
            ValidationErrorType.PROBABILITY_ERROR,
            field_name,
            attempted_value
        )


class NumericValidationException(ValidationException):
    def __init__(self, message, field_name="numeric_value", attempted_value=None):
        super().__init__(
            message,
            ValidationErrorType.NUMERIC_ERROR,
            field_name,
            attempted_value
        )