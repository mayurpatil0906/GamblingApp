from datetime import datetime
from db.db_connection import create_connection
from services.outcome_strategies import RandomOutcomeStrategy, WeightedProbabilityStrategy
from services.game_result_model import GameResult
from services.win_loss_statistics import WinLossStatistics
from services.running_totals import RunningTotals
from models.odds_type import OddsType


class WinLossCalculatorService:
    def __init__(self):
        self.random_strategy = RandomOutcomeStrategy()
        self.weighted_strategy = WeightedProbabilityStrategy()
        self.session_stats = {}
        self.session_running_totals = {}

    def _get_or_create_state(self, session_id, starting_balance):
        if session_id not in self.session_stats:
            self.session_stats[session_id] = WinLossStatistics()
        if session_id not in self.session_running_totals:
            self.session_running_totals[session_id] = RunningTotals(starting_balance)

        return self.session_stats[session_id], self.session_running_totals[session_id]

    def _get_current_stake(self, cursor, gambler_id):
        cursor.execute(
            "SELECT current_stake FROM gamblers WHERE gambler_id = %s",
            (gambler_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return float(row[0])

    def determine_outcome(self, strategy_type, win_probability, house_edge=0.05):
        if strategy_type == "WEIGHTED":
            return self.weighted_strategy.determine_outcome(win_probability, house_edge)
        return self.random_strategy.determine_outcome(win_probability)

    def process_game_result(
        self,
        game_id,
        session_id,
        bet_id,
        gambler_id,
        bet_amount,
        odds_type,
        odds_value,
        win_probability,
        strategy_type="RANDOM",
        house_edge=0.05
    ):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        try:
            stake_before = self._get_current_stake(cursor, gambler_id)
            if stake_before is None:
                print("Gambler not found")
                return

            stats, running_totals = self._get_or_create_state(session_id, stake_before)

            outcome = self.determine_outcome(strategy_type, win_probability, house_edge)

            result = GameResult(
                game_id=game_id,
                session_id=session_id,
                bet_id=bet_id,
                outcome=outcome,
                bet_amount=bet_amount,
                odds_type=odds_type,
                odds_value=odds_value,
                stake_before=stake_before
            )

            result.calculate_payout(win_probability=win_probability)

            stats.record_result(result)
            running_totals.apply_result(result)

            cursor.execute("""
                INSERT INTO game_records (
                    game_id, session_id, bet_id, odds_config_id,
                    outcome, payout_amount, loss_amount, net_change,
                    stake_before, stake_after,
                    consecutive_win_streak, consecutive_loss_streak,
                    game_duration_seconds, resolved_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                game_id,
                session_id,
                bet_id,
                1,
                result.outcome,
                round(result.payout_amount, 2),
                round(result.loss_amount, 2),
                round(result.net_change, 2),
                round(result.stake_before, 2),
                round(result.stake_after, 2),
                stats.current_win_streak,
                stats.current_loss_streak,
                5,
                result.resolved_at
            ))

            cursor.execute("""
                UPDATE gamblers
                SET current_stake = %s, updated_at = %s
                WHERE gambler_id = %s
            """, (
                round(result.stake_after, 2),
                datetime.now(),
                gambler_id
            ))

            snapshot_id = int(datetime.now().timestamp() * 1000000)

            cursor.execute("""
                INSERT INTO running_total_snapshots (
                    snapshot_id, session_id, game_id, total_games,
                    total_wins, total_losses, total_pushes, total_winnings,
                    total_losses_amount, net_profit, win_rate, profit_factor,
                    roi, longest_win_streak, longest_loss_streak, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                snapshot_id,
                session_id,
                game_id,
                stats.total_games,
                stats.win_count,
                stats.loss_count,
                stats.push_count,
                round(stats.total_winnings, 2),
                round(stats.total_losses, 2),
                round(running_totals.net_profit_loss, 2),
                stats.get_win_rate(),
                running_totals.get_profit_factor(),
                running_totals.get_roi(),
                stats.longest_win_streak,
                stats.longest_loss_streak,
                datetime.now()
            ))

            connection.commit()
            print(f"Game processed successfully. Outcome: {result.outcome}")

        except Exception as e:
            print(f"Error in process_game_result: {e}")

        finally:
            cursor.close()
            connection.close()

    def show_session_statistics(self, session_id):
        stats = self.session_stats.get(session_id)
        running = self.session_running_totals.get(session_id)

        if stats is None or running is None:
            print("No statistics found for this session")
            return

        summary = stats.summary(running)

        print("\n===== WIN/LOSS SESSION STATISTICS =====")
        for key, value in summary.items():
            print(f"{key}: {value}")

        print("\n===== BALANCE HISTORY =====")
        print(running.balance_history)