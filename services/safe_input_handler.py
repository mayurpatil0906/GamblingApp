from services.input_validator import InputValidator


class SafeInputHandler:
    def __init__(self):
        self.validator = InputValidator()

    def get_int(self, prompt):
        while True:
            value = input(prompt).strip()
            try:
                return int(value)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def get_float(self, prompt):
        while True:
            value = input(prompt).strip()
            try:
                return self.validator.parse_and_validate_numeric(value)
            except Exception as e:
                print(e)

    def get_valid_initial_stake(self, prompt):
        while True:
            value = input(prompt).strip()
            try:
                return self.validator.validate_initial_stake(value)
            except Exception as e:
                print(e)

    def get_valid_bet_amount(self, prompt, current_stake, min_bet=None, max_bet=None):
        while True:
            value = input(prompt).strip()
            try:
                return self.validator.validate_bet_amount(value, current_stake, min_bet, max_bet)
            except Exception as e:
                print(e)

    def get_valid_probability(self, prompt):
        while True:
            value = input(prompt).strip()
            try:
                return self.validator.validate_probability(value)
            except Exception as e:
                print(e)

    def get_valid_limits(self):
        while True:
            lower = input("Enter lower limit: ").strip()
            upper = input("Enter upper limit: ").strip()
            initial = input("Enter initial stake: ").strip()

            try:
                lower_limit, upper_limit = self.validator.validate_limits(lower, upper, initial)
                return lower_limit, upper_limit, float(initial)
            except Exception as e:
                print(e)