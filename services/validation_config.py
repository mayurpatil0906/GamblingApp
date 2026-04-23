class ValidationConfig:
    def __init__(self):
        self.min_stake = 1.0
        self.max_stake = 100000.0

        self.min_bet = 1.0
        self.max_bet = 10000.0

        self.min_probability = 0.0
        self.max_probability = 1.0

        self.strict_mode = True
        self.allow_zero_stake = False