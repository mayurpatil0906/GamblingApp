class BettingSession:
    def __init__(self, session_id, gambler_id):
        self.session_id = session_id
        self.gambler_id = gambler_id
        self.total_bets = 0
        self.total_wins = 0
        self.total_losses = 0
        self.total_amount_bet = 0.0
        self.total_amount_won = 0.0
        self.bet_history = []

    def record_bet(self, bet_data):
        self.bet_history.append(bet_data)
        self.total_bets += 1
        self.total_amount_bet += float(bet_data["bet_amount"])

        if bet_data["outcome"] == "WIN":
            self.total_wins += 1
            self.total_amount_won += float(bet_data["payout_amount"])
        else:
            self.total_losses += 1

    def summary(self):
        return {
            "session_id": self.session_id,
            "gambler_id": self.gambler_id,
            "total_bets": self.total_bets,
            "total_wins": self.total_wins,
            "total_losses": self.total_losses,
            "total_amount_bet": self.total_amount_bet,
            "total_amount_won": self.total_amount_won,
            "history_count": len(self.bet_history)
        }