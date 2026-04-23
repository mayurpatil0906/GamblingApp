from db.db_connection import create_connection
from datetime import datetime
import random

from services.betting_session import BettingSession
from services.strategies import (
    FixedAmountStrategy,
    PercentageStrategy,
    MartingaleStrategy,
    ReverseMartingaleStrategy,
    FibonacciStrategy,
    DAlembertStrategy
)
from models.transaction_type import TransactionType


class BettingService:
    def __init__(self):
        self.sessions = {}
        self.strategies = {
            "FIXED": FixedAmountStrategy(),
            "PERCENTAGE": PercentageStrategy(),
            "MARTINGALE": MartingaleStrategy(),
            "REVERSE_MARTINGALE": ReverseMartingaleStrategy(),
            "FIBONACCI": FibonacciStrategy(),
            "DALEMBERT": DAlembertStrategy(),
        }

    def get_or_create_betting_session(self, session_id, gambler_id):
        key = (session_id, gambler_id)
        if key not in self.sessions:
            self.sessions[key] = BettingSession(session_id, gambler_id)
        return self.sessions[key]

    def get_current_stake(self, cursor, gambler_id):
        cursor.execute(
            "SELECT current_stake FROM gamblers WHERE gambler_id = %s",
            (gambler_id,)
        )
        result = cursor.fetchone()
        if not result:
            return None
        return float(result[0])

    def get_session_limits(self, cursor, session_id):
        cursor.execute("""
            SELECT min_bet, max_bet, default_win_probability
            FROM session_parameters
            WHERE session_id = %s
        """, (session_id,))
        result = cursor.fetchone()
        if result:
            return {
                "min_bet": float(result[0]),
                "max_bet": float(result[1]),
                "default_win_probability": float(result[2]),
            }
        return None

    def validate_bet_amount(self, bet_amount, current_stake, min_bet, max_bet):
        if bet_amount <= 0:
            return False, "Bet amount must be greater than zero"
        if bet_amount > current_stake:
            return False, "Bet amount exceeds current stake"
        if bet_amount < min_bet:
            return False, f"Bet amount is below minimum bet ({min_bet})"
        if bet_amount > max_bet:
            return False, f"Bet amount exceeds maximum bet ({max_bet})"
        return True, "Valid bet"

    def determine_bet_outcome(self, win_probability):
        rnd = random.random()
        return "WIN" if rnd <= win_probability else "LOSS"

    def calculate_potential_win(self, bet_amount, odds_value):
        return round(float(bet_amount) * float(odds_value), 2)

    def place_bet(self, bet_id, gambler_id, session_id, bet_amount, win_probability, odds_value, strategy_id=1):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        try:
            current_stake = self.get_current_stake(cursor, gambler_id)
            if current_stake is None:
                print("Gambler not found")
                return

            session_limits = self.get_session_limits(cursor, session_id)
            if session_limits is None:
                print("Session parameters not found")
                return

            valid, msg = self.validate_bet_amount(
                bet_amount,
                current_stake,
                session_limits["min_bet"],
                session_limits["max_bet"]
            )

            if not valid:
                print(msg)
                return

            stake_before = current_stake
            outcome = self.determine_bet_outcome(win_probability)
            potential_win = self.calculate_potential_win(bet_amount, odds_value)

            if outcome == "WIN":
                payout_amount = potential_win
                loss_amount = 0.0
                net_change = payout_amount
                stake_after = stake_before + payout_amount
                txn_type = TransactionType.BET_WIN.value
            else:
                payout_amount = 0.0
                loss_amount = float(bet_amount)
                net_change = -float(bet_amount)
                stake_after = stake_before - float(bet_amount)
                txn_type = TransactionType.BET_LOSS.value

            bet_query = """
            INSERT INTO bets (
                bet_id, session_id, gambler_id, strategy_id,
                game_index, bet_amount, win_probability,
                odds_type, odds_value, potential_win,
                stake_before, stake_after, is_settled, placed_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            session_obj = self.get_or_create_betting_session(session_id, gambler_id)
            game_index = session_obj.total_bets + 1

            cursor.execute(
                bet_query,
                (
                    bet_id,
                    session_id,
                    gambler_id,
                    strategy_id,
                    game_index,
                    float(bet_amount),
                    float(win_probability),
                    "FIXED",
                    float(odds_value),
                    potential_win,
                    stake_before,
                    stake_after,
                    True,
                    datetime.now()
                )
            )

            game_id = int(datetime.now().timestamp() * 1000)

            game_query = """
            INSERT INTO game_records (
                game_id, session_id, bet_id, odds_config_id,
                outcome, payout_amount, loss_amount, net_change,
                stake_before, stake_after,
                consecutive_win_streak, consecutive_loss_streak,
                game_duration_seconds, resolved_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                game_query,
                (
                    game_id,
                    session_id,
                    bet_id,
                    1,
                    outcome,
                    payout_amount,
                    loss_amount,
                    net_change,
                    stake_before,
                    stake_after,
                    0,
                    0,
                    5,
                    datetime.now()
                )
            )

            cursor.execute("""
                UPDATE gamblers
                SET current_stake = %s, updated_at = %s
                WHERE gambler_id = %s
            """, (stake_after, datetime.now(), gambler_id))

            transaction_id = int(datetime.now().timestamp() * 1000000)

            cursor.execute("""
                INSERT INTO stake_transaction (
                    transaction_id, gambler_id, session_id, bet_id,
                    transaction_type, amount, balance_before, balance_after, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                transaction_id,
                gambler_id,
                session_id,
                bet_id,
                txn_type,
                abs(net_change),
                stake_before,
                stake_after,
                datetime.now()
            ))

            cursor.execute("""
                UPDATE sessions
                SET games_played = games_played + 1,
                    ending_stake = %s,
                    peak_stake = GREATEST(peak_stake, %s),
                    lowest_stake = LEAST(lowest_stake, %s)
                WHERE session_id = %s
            """, (stake_after, stake_after, stake_after, session_id))

            session_obj.record_bet({
                "bet_id": bet_id,
                "bet_amount": bet_amount,
                "outcome": outcome,
                "payout_amount": payout_amount
            })

            connection.commit()
            print(f"Bet placed and resolved successfully. Outcome: {outcome}")

        except Exception as e:
            print(f"Error in place_bet: {e}")

        finally:
            cursor.close()
            connection.close()

    def place_bet_with_strategy(
        self,
        bet_id,
        gambler_id,
        session_id,
        strategy_name,
        base_amount,
        odds_value,
        win_probability=None,
        percentage=0.05,
        increment=10
    ):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        try:
            current_stake = self.get_current_stake(cursor, gambler_id)
            if current_stake is None:
                print("Gambler not found")
                return

            session_limits = self.get_session_limits(cursor, session_id)
            if session_limits is None:
                print("Session parameters not found")
                return

            if win_probability is None:
                win_probability = session_limits["default_win_probability"]

            session_obj = self.get_or_create_betting_session(session_id, gambler_id)
            last_outcome = None
            last_bet_amount = None

            if session_obj.bet_history:
                last_outcome = session_obj.bet_history[-1]["outcome"]
                last_bet_amount = float(session_obj.bet_history[-1]["bet_amount"])

            strategy = self.strategies.get(strategy_name.upper())
            if strategy is None:
                print("Invalid strategy")
                return

            if strategy_name.upper() == "PERCENTAGE":
                bet_amount = strategy.calculate_bet(
                    current_stake=current_stake,
                    percentage=percentage
                )
            elif strategy_name.upper() == "DALEMBERT":
                bet_amount = strategy.calculate_bet(
                    current_stake=current_stake,
                    base_amount=base_amount,
                    last_outcome=last_outcome,
                    last_bet_amount=last_bet_amount,
                    increment=increment
                )
            else:
                bet_amount = strategy.calculate_bet(
                    current_stake=current_stake,
                    base_amount=base_amount,
                    last_outcome=last_outcome,
                    last_bet_amount=last_bet_amount
                )

            self.place_bet(
                bet_id=bet_id,
                gambler_id=gambler_id,
                session_id=session_id,
                bet_amount=bet_amount,
                win_probability=win_probability,
                odds_value=odds_value,
                strategy_id=1
            )

        finally:
            cursor.close()
            connection.close()

    def place_consecutive_bets(
        self,
        start_bet_id,
        gambler_id,
        session_id,
        strategy_name,
        rounds,
        base_amount,
        odds_value,
        win_probability=None
    ):
        for i in range(rounds):
            bet_id = start_bet_id + i
            self.place_bet_with_strategy(
                bet_id=bet_id,
                gambler_id=gambler_id,
                session_id=session_id,
                strategy_name=strategy_name,
                base_amount=base_amount,
                odds_value=odds_value,
                win_probability=win_probability
            )

    def get_betting_session_summary(self, session_id, gambler_id):
        session_obj = self.get_or_create_betting_session(session_id, gambler_id)
        summary = session_obj.summary()

        print("\n===== BETTING SESSION SUMMARY =====")
        print("Session ID       :", summary["session_id"])
        print("Gambler ID       :", summary["gambler_id"])
        print("Total Bets       :", summary["total_bets"])
        print("Total Wins       :", summary["total_wins"])
        print("Total Losses     :", summary["total_losses"])
        print("Total Amount Bet :", summary["total_amount_bet"])
        print("Total Amount Won :", summary["total_amount_won"])
        print("History Count    :", summary["history_count"])