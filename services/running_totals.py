class RunningTotals:
    def __init__(self, starting_balance):
        self.starting_balance = float(starting_balance)
        self.current_balance = float(starting_balance)
        self.balance_history = [float(starting_balance)]

        self.total_winnings = 0.0
        self.total_losses = 0.0
        self.net_profit_loss = 0.0

    def apply_result(self, game_result):
        self.current_balance = float(game_result.stake_after)
        self.balance_history.append(self.current_balance)

        self.total_winnings += float(game_result.payout_amount)
        self.total_losses += float(game_result.loss_amount)
        self.net_profit_loss = self.current_balance - self.starting_balance

    def get_profit_factor(self):
        if self.total_losses == 0:
            return 0.0
        return round(self.total_winnings / self.total_losses, 2)

    def get_roi(self):
        if self.starting_balance == 0:
            return 0.0
        return round((self.net_profit_loss / self.starting_balance) * 100, 2)