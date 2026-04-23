from db.db_connection import create_connection
from datetime import datetime


class SessionService:

    def start_session(self, session_id, gambler_id, max_games):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT current_stake FROM gamblers WHERE gambler_id = %s",
                (gambler_id,)
            )
            result = cursor.fetchone()

            if not result:
                print("Gambler not found")
                return

            current_stake = float(result[0])

            query = """
            INSERT INTO sessions (
                session_id, gambler_id, status, end_reason,
                starting_stake, ending_stake, peak_stake, lowest_stake,
                max_games, games_played, total_pause_seconds,
                started_at, created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            now = datetime.now()

            values = (
                session_id,
                gambler_id,
                "ACTIVE",
                None,
                current_stake,
                current_stake,
                current_stake,
                current_stake,
                max_games,
                0,
                0,
                now,
                now
            )

            cursor.execute(query, values)
            connection.commit()
            print("Session started successfully")

        except Exception as e:
            print(f"Error while starting session: {e}")

        finally:
            cursor.close()
            connection.close()

    def update_stake(self, gambler_id, amount, transaction_type, session_id):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT current_stake FROM gamblers WHERE gambler_id = %s",
                (gambler_id,)
            )
            result = cursor.fetchone()

            if not result:
                print("Gambler not found")
                return

            current_stake = float(result[0])
            amount = float(amount)

            if transaction_type == "BET":
                new_stake = current_stake - amount
            elif transaction_type == "WIN":
                new_stake = current_stake + amount
            elif transaction_type == "LOSS":
                new_stake = current_stake - amount
            else:
                print("Invalid transaction type")
                return

            if new_stake < 0:
                print("Insufficient stake")
                return

            update_query = """
            UPDATE gamblers
            SET current_stake = %s, updated_at = %s
            WHERE gambler_id = %s
            """

            cursor.execute(update_query, (new_stake, datetime.now(), gambler_id))

            transaction_query = """
            INSERT INTO stake_transaction (
                transaction_id, gambler_id, session_id, bet_id,
                transaction_type, amount, balance_before, balance_after, created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            now = datetime.now()
            transaction_id = int(datetime.now().timestamp() * 1000)

            cursor.execute(
                transaction_query,
                (
                    transaction_id,
                    gambler_id,
                    session_id,
                    None,
                    transaction_type,
                    amount,
                    current_stake,
                    new_stake,
                    now
                )
            )

            connection.commit()
            print(f"{transaction_type} processed successfully")

        except Exception as e:
            print(f"Error while updating stake: {e}")

        finally:
            cursor.close()
            connection.close()