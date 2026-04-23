from datetime import datetime
from models.session_status import SessionStatus
from models.session_end_reason import SessionEndReason


class GamingSession:
    def __init__(
        self,
        session_id,
        gambler_id,
        starting_stake,
        lower_limit,
        upper_limit,
        min_bet,
        max_bet,
        max_games,
        max_session_minutes,
        default_win_probability
    ):
        self.session_id = session_id
        self.gambler_id = gambler_id
        self.status = SessionStatus.INITIALIZED
        self.end_reason = None

        self.starting_stake = float(starting_stake)
        self.current_stake = float(starting_stake)
        self.ending_stake = float(starting_stake)

        self.lower_limit = float(lower_limit)
        self.upper_limit = float(upper_limit)
        self.min_bet = float(min_bet)
        self.max_bet = float(max_bet)
        self.max_games = int(max_games)
        self.max_session_minutes = int(max_session_minutes)
        self.default_win_probability = float(default_win_probability)

        self.peak_stake = float(starting_stake)
        self.lowest_stake = float(starting_stake)

        self.games_played = 0
        self.total_pause_seconds = 0
        self.pause_history = []

        self.started_at = None
        self.ended_at = None
        self.current_pause_started_at = None

        self.game_history = []

    def start(self):
        self.status = SessionStatus.ACTIVE
        self.started_at = datetime.now()

    def pause(self, reason):
        if self.status != SessionStatus.ACTIVE:
            return False, "Session is not active"

        self.status = SessionStatus.PAUSED
        self.current_pause_started_at = datetime.now()
        self.pause_history.append({
            "reason": reason,
            "paused_at": self.current_pause_started_at,
            "resumed_at": None,
            "pause_seconds": 0
        })
        return True, "Session paused successfully"

    def resume(self):
        if self.status != SessionStatus.PAUSED:
            return False, "Session is not paused"

        resumed_at = datetime.now()
        last_pause = self.pause_history[-1]
        pause_seconds = int((resumed_at - last_pause["paused_at"]).total_seconds())

        last_pause["resumed_at"] = resumed_at
        last_pause["pause_seconds"] = pause_seconds

        self.total_pause_seconds += pause_seconds
        self.current_pause_started_at = None
        self.status = SessionStatus.ACTIVE
        return True, "Session resumed successfully"

    def record_game(self, bet_amount, outcome, stake_before, stake_after):
        self.games_played += 1
        self.current_stake = float(stake_after)
        self.ending_stake = float(stake_after)

        self.peak_stake = max(self.peak_stake, float(stake_after))
        self.lowest_stake = min(self.lowest_stake, float(stake_after))

        self.game_history.append({
            "game_no": self.games_played,
            "bet_amount": float(bet_amount),
            "outcome": outcome,
            "stake_before": float(stake_before),
            "stake_after": float(stake_after),
            "played_at": datetime.now()
        })

    def check_boundaries(self):
        if self.current_stake >= self.upper_limit:
            self.status = SessionStatus.ENDED_WIN
            self.end_reason = SessionEndReason.UPPER_LIMIT_REACHED
            self.ended_at = datetime.now()
            return True, "Upper limit reached"

        if self.current_stake <= self.lower_limit:
            self.status = SessionStatus.ENDED_LOSS
            self.end_reason = SessionEndReason.LOWER_LIMIT_REACHED
            self.ended_at = datetime.now()
            return True, "Lower limit reached"

        if self.games_played >= self.max_games:
            self.status = SessionStatus.ENDED_MANUAL
            self.end_reason = SessionEndReason.MAX_GAMES_REACHED
            self.ended_at = datetime.now()
            return True, "Max games reached"

        if self.started_at is not None:
            elapsed_minutes = int((datetime.now() - self.started_at).total_seconds() / 60)
            if elapsed_minutes >= self.max_session_minutes:
                self.status = SessionStatus.ENDED_TIMEOUT
                self.end_reason = SessionEndReason.TIMEOUT
                self.ended_at = datetime.now()
                return True, "Session timed out"

        return False, "Session still active"

    def end_manually(self):
        self.status = SessionStatus.ENDED_MANUAL
        self.end_reason = SessionEndReason.MANUAL
        self.ended_at = datetime.now()

    def get_total_duration_seconds(self):
        if self.started_at is None:
            return 0

        end_time = self.ended_at if self.ended_at else datetime.now()
        return int((end_time - self.started_at).total_seconds())

    def get_active_play_duration_seconds(self):
        return self.get_total_duration_seconds() - self.total_pause_seconds

    def summary(self):
        total_duration = self.get_total_duration_seconds()
        active_duration = self.get_active_play_duration_seconds()

        wins = sum(1 for g in self.game_history if g["outcome"] == "WIN")
        losses = sum(1 for g in self.game_history if g["outcome"] == "LOSS")
        win_rate = (wins / self.games_played * 100) if self.games_played > 0 else 0.0
        roi = ((self.ending_stake - self.starting_stake) / self.starting_stake * 100) if self.starting_stake > 0 else 0.0
        avg_bet = (sum(g["bet_amount"] for g in self.game_history) / self.games_played) if self.games_played > 0 else 0.0

        return {
            "session_id": self.session_id,
            "gambler_id": self.gambler_id,
            "status": self.status.value,
            "end_reason": self.end_reason.value if self.end_reason else None,
            "starting_stake": self.starting_stake,
            "ending_stake": self.ending_stake,
            "peak_stake": self.peak_stake,
            "lowest_stake": self.lowest_stake,
            "games_played": self.games_played,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 2),
            "roi": round(roi, 2),
            "average_bet": round(avg_bet, 2),
            "total_pause_seconds": self.total_pause_seconds,
            "total_duration_seconds": total_duration,
            "active_play_duration_seconds": active_duration,
            "pause_count": len(self.pause_history),
        }