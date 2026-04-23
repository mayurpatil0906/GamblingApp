class WinLossStatistics:
    def __init__(self):
        self.total_games = 0
        self.win_count = 0
        self.loss_count = 0
        self.push_count = 0

        self.total_winnings = 0.0
        self.total_losses = 0.0

        self.largest_win = 0.0
        self.largest_loss = 0.0

        self.current_win_streak = 0
        self.current_loss_streak = 0
        self.longest_win_streak = 0
        self.longest_loss_streak = 0

        self.win_amounts = []
        self.loss_amounts = []

    def record_result(self, game_result):
        self.total_games += 1

        if game_result.outcome == "WIN":
            self.win_count += 1
            self.total_winnings += float(game_result.payout_amount)
            self.win_amounts.append(float(game_result.payout_amount))
            self.largest_win = max(self.largest_win, float(game_result.payout_amount))

            self.current_win_streak += 1
            self.current_loss_streak = 0
            self.longest_win_streak = max(self.longest_win_streak, self.current_win_streak)

        elif game_result.outcome == "LOSS":
            self.loss_count += 1
            self.total_losses += float(game_result.loss_amount)
            self.loss_amounts.append(float(game_result.loss_amount))
            self.largest_loss = max(self.largest_loss, float(game_result.loss_amount))

            self.current_loss_streak += 1
            self.current_win_streak = 0
            self.longest_loss_streak = max(self.longest_loss_streak, self.current_loss_streak)

    def get_win_rate(self):
        if self.total_games == 0:
            return 0.0
        return round((self.win_count / self.total_games) * 100, 2)

    def get_loss_rate(self):
        if self.total_games == 0:
            return 0.0
        return round((self.loss_count / self.total_games) * 100, 2)

    def get_win_loss_ratio(self):
        if self.loss_count == 0:
            return 0.0
        return round(self.win_count / self.loss_count, 2)

    def get_average_win(self):
        if not self.win_amounts:
            return 0.0
        return round(sum(self.win_amounts) / len(self.win_amounts), 2)

    def get_average_loss(self):
        if not self.loss_amounts:
            return 0.0
        return round(sum(self.loss_amounts) / len(self.loss_amounts), 2)

    def summary(self, running_totals):
        return {
            "total_games": self.total_games,
            "wins": self.win_count,
            "losses": self.loss_count,
            "win_rate": self.get_win_rate(),
            "loss_rate": self.get_loss_rate(),
            "win_loss_ratio": self.get_win_loss_ratio(),
            "total_winnings": round(self.total_winnings, 2),
            "total_losses": round(self.total_losses, 2),
            "average_win": self.get_average_win(),
            "average_loss": self.get_average_loss(),
            "largest_win": round(self.largest_win, 2),
            "largest_loss": round(self.largest_loss, 2),
            "current_win_streak": self.current_win_streak,
            "current_loss_streak": self.current_loss_streak,
            "longest_win_streak": self.longest_win_streak,
            "longest_loss_streak": self.longest_loss_streak,
            "net_profit_loss": round(running_totals.net_profit_loss, 2),
            "profit_factor": running_totals.get_profit_factor(),
            "roi": running_totals.get_roi(),
            "current_balance": round(running_totals.current_balance, 2)
        }