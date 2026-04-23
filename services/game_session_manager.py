from datetime import datetime
from db.db_connection import create_connection
from services.gaming_session import GamingSession


class GameSessionManager:
    def __init__(self):
        self.active_sessions = {}
        self.completed_sessions = {}

    def _save_session_to_db(self, session_obj):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO sessions (
                    session_id, gambler_id, status, end_reason,
                    starting_stake, ending_stake, peak_stake, lowest_stake,
                    max_games, games_played, total_pause_seconds,
                    started_at, ended_at, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                session_obj.session_id,
                session_obj.gambler_id,
                session_obj.status.value,
                session_obj.end_reason.value if session_obj.end_reason else None,
                session_obj.starting_stake,
                session_obj.ending_stake,
                session_obj.peak_stake,
                session_obj.lowest_stake,
                session_obj.max_games,
                session_obj.games_played,
                session_obj.total_pause_seconds,
                session_obj.started_at,
                session_obj.ended_at,
                datetime.now()
            ))

            cursor.execute("""
                INSERT INTO session_parameters (
                    parameter_id, session_id, lower_limit, upper_limit,
                    min_bet, max_bet, default_win_probability,
                    max_session_minutes, strict_mode, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(datetime.now().timestamp() * 1000),
                session_obj.session_id,
                session_obj.lower_limit,
                session_obj.upper_limit,
                session_obj.min_bet,
                session_obj.max_bet,
                session_obj.default_win_probability,
                session_obj.max_session_minutes,
                True,
                datetime.now()
            ))

            connection.commit()

        except Exception as e:
            print(f"Error while saving session: {e}")
        finally:
            cursor.close()
            connection.close()

    def _update_session_in_db(self, session_obj):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE sessions
                SET status = %s,
                    end_reason = %s,
                    ending_stake = %s,
                    peak_stake = %s,
                    lowest_stake = %s,
                    games_played = %s,
                    total_pause_seconds = %s,
                    ended_at = %s
                WHERE session_id = %s
            """, (
                session_obj.status.value,
                session_obj.end_reason.value if session_obj.end_reason else None,
                session_obj.ending_stake,
                session_obj.peak_stake,
                session_obj.lowest_stake,
                session_obj.games_played,
                session_obj.total_pause_seconds,
                session_obj.ended_at,
                session_obj.session_id
            ))

            for pause in session_obj.pause_history:
                cursor.execute("""
                    INSERT INTO pause_records (
                        pause_id, session_id, pause_reason, paused_at, resumed_at, pause_seconds
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    int(datetime.now().timestamp() * 1000000),
                    session_obj.session_id,
                    pause["reason"],
                    pause["paused_at"],
                    pause["resumed_at"],
                    pause["pause_seconds"]
                ))

            connection.commit()

        except Exception as e:
            print(f"Error while updating session: {e}")
        finally:
            cursor.close()
            connection.close()

    def start_new_session(
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
        if gambler_id in self.active_sessions:
            print("This gambler already has an active session")
            return None

        session_obj = GamingSession(
            session_id=session_id,
            gambler_id=gambler_id,
            starting_stake=starting_stake,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            min_bet=min_bet,
            max_bet=max_bet,
            max_games=max_games,
            max_session_minutes=max_session_minutes,
            default_win_probability=default_win_probability
        )

        session_obj.start()
        self.active_sessions[gambler_id] = session_obj
        self._save_session_to_db(session_obj)

        print("New gambling session started successfully")
        return session_obj

    def continue_session(self, gambler_id, bet_amount, outcome):
        session_obj = self.active_sessions.get(gambler_id)

        if session_obj is None:
            print("No active session found")
            return

        if session_obj.status != session_obj.status.ACTIVE:
            print("Session is not active")
            return

        stake_before = session_obj.current_stake

        if outcome == "WIN":
            stake_after = stake_before + bet_amount
        else:
            stake_after = stake_before - bet_amount

        session_obj.record_game(
            bet_amount=bet_amount,
            outcome=outcome,
            stake_before=stake_before,
            stake_after=stake_after
        )

        ended, message = session_obj.check_boundaries()
        self._update_session_in_db(session_obj)

        print(f"Game recorded. {message}")

        if ended:
            self.completed_sessions[gambler_id] = session_obj
            del self.active_sessions[gambler_id]

    def pause_session(self, gambler_id, reason):
        session_obj = self.active_sessions.get(gambler_id)

        if session_obj is None:
            print("No active session found")
            return

        success, message = session_obj.pause(reason)
        self._update_session_in_db(session_obj)
        print(message)

    def resume_session(self, gambler_id):
        session_obj = self.active_sessions.get(gambler_id)

        if session_obj is None:
            print("No active session found")
            return

        success, message = session_obj.resume()
        self._update_session_in_db(session_obj)
        print(message)

    def end_session_manually(self, gambler_id):
        session_obj = self.active_sessions.get(gambler_id)

        if session_obj is None:
            print("No active session found")
            return

        session_obj.end_manually()
        self._update_session_in_db(session_obj)

        self.completed_sessions[gambler_id] = session_obj
        del self.active_sessions[gambler_id]

        print("Session ended manually")

    def session_summary(self, gambler_id):
        session_obj = self.active_sessions.get(gambler_id) or self.completed_sessions.get(gambler_id)

        if session_obj is None:
            print("No session found")
            return

        summary = session_obj.summary()

        print("\n===== GAME SESSION SUMMARY =====")
        for key, value in summary.items():
            print(f"{key}: {value}")

        print("\n===== GAME-BY-GAME HISTORY =====")
        for game in session_obj.game_history:
            print(game)