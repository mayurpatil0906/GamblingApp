from datetime import datetime
from models.odds_type import OddsType


class GameResult:
    def __init__(
        self,
        game_id,
        session_id,
        bet_id,
        outcome,
        bet_amount,
        odds_type,
        odds_value,
        stake_before
    ):
        self.game_id = game_id
        self.session_id = session_id
        self.bet_id = bet_id
        self.outcome = outcome
        self.bet_amount = float(bet_amount)
        self.odds_type = odds_type
        self.odds_value = float(odds_value)
        self.stake_before = float(stake_before)

        self.payout_amount = 0.0
        self.loss_amount = 0.0
        self.net_change = 0.0
        self.stake_after = float(stake_before)
        self.resolved_at = datetime.now()

    def calculate_payout(self, win_probability=None):
        odds_type = self.odds_type if isinstance(self.odds_type, str) else self.odds_type.value

        if self.outcome == "LOSS":
            self.loss_amount = self.bet_amount
            self.net_change = -self.bet_amount
            self.stake_after = self.stake_before - self.bet_amount
            return

        if odds_type == OddsType.FIXED.value:
            self.payout_amount = self.bet_amount * self.odds_value

        elif odds_type == OddsType.DECIMAL.value:
            self.payout_amount = self.bet_amount * self.odds_value

        elif odds_type == OddsType.PROBABILITY_BASED.value:
            if win_probability is None or float(win_probability) <= 0:
                raise ValueError("Valid win_probability required for PROBABILITY_BASED odds")
            self.payout_amount = self.bet_amount * (1 / float(win_probability))

        elif odds_type == OddsType.AMERICAN.value:
            american = self.odds_value
            if american > 0:
                self.payout_amount = self.bet_amount + ((self.bet_amount / 100) * american)
            else:
                self.payout_amount = self.bet_amount + ((self.bet_amount * 100) / abs(american))
        else:
            raise ValueError("Unsupported odds type")

        self.net_change = self.payout_amount
        self.stake_after = self.stake_before + self.payout_amount

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "session_id": self.session_id,
            "bet_id": self.bet_id,
            "outcome": self.outcome,
            "bet_amount": self.bet_amount,
            "odds_type": self.odds_type if isinstance(self.odds_type, str) else self.odds_type.value,
            "odds_value": self.odds_value,
            "payout_amount": round(self.payout_amount, 2),
            "loss_amount": round(self.loss_amount, 2),
            "net_change": round(self.net_change, 2),
            "stake_before": round(self.stake_before, 2),
            "stake_after": round(self.stake_after, 2),
            "resolved_at": self.resolved_at
        }