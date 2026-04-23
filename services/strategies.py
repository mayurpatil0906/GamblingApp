class FixedAmountStrategy:
    def calculate_bet(self, current_stake, base_amount, **kwargs):
        return base_amount


class PercentageStrategy:
    def calculate_bet(self, current_stake, percentage=0.05, **kwargs):
        return round(current_stake * percentage, 2)


class MartingaleStrategy:
    def calculate_bet(self, current_stake, base_amount, last_outcome=None, last_bet_amount=None, **kwargs):
        if last_outcome == "LOSS" and last_bet_amount is not None:
            return min(last_bet_amount * 2, current_stake)
        return min(base_amount, current_stake)


class ReverseMartingaleStrategy:
    def calculate_bet(self, current_stake, base_amount, last_outcome=None, last_bet_amount=None, **kwargs):
        if last_outcome == "WIN" and last_bet_amount is not None:
            return min(last_bet_amount * 2, current_stake)
        return min(base_amount, current_stake)


class FibonacciStrategy:
    def __init__(self):
        self.sequence = [1, 1]
        self.index = 0

    def calculate_bet(self, current_stake, base_amount, last_outcome=None, **kwargs):
        if last_outcome == "LOSS":
            self.index += 1
            if self.index >= len(self.sequence):
                self.sequence.append(self.sequence[-1] + self.sequence[-2])
        elif last_outcome == "WIN":
            self.index = max(0, self.index - 2)

        bet = self.sequence[self.index] * base_amount
        return min(bet, current_stake)


class DAlembertStrategy:
    def calculate_bet(self, current_stake, base_amount, last_outcome=None, last_bet_amount=None, increment=10, **kwargs):
        if last_bet_amount is None:
            return min(base_amount, current_stake)

        if last_outcome == "LOSS":
            return min(last_bet_amount + increment, current_stake)
        elif last_outcome == "WIN":
            return min(max(base_amount, last_bet_amount - increment), current_stake)

        return min(base_amount, current_stake)