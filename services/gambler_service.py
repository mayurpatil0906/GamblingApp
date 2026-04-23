from db.db_connection import create_connection
from datetime import datetime


class GamblerService:

    def create_gambler(
        self,
        gambler_id,
        username,
        full_name,
        email,
        initial_stake,
        win_threshold,
        loss_threshold,
        min_required_stake
    ):
        connection = create_connection()
        if connection is None:
            print("Database connection failed")
            return

        cursor = connection.cursor()

        query = """
        INSERT INTO gamblers (
            gambler_id, username, full_name, email, is_active,
            initial_stake, current_stake, win_threshold, loss_threshold,
            min_required_stake, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        now = datetime.now()

        values = (
            gambler_id,
            username,
            full_name,
            email,
            True,
            initial_stake,
            initial_stake,
            win_threshold,
            loss_threshold,
            min_required_stake,
            now,
            now
        )

        try:
            cursor.execute(query, values)
            connection.commit()
            print("Gambler created successfully")
        except Exception as e:
            print(f"Error creating gambler: {e}")
        finally:
            cursor.close()
            connection.close()

    def get_all_gamblers(self):
        connection = create_connection()
        if connection is None:
            return []

        cursor = connection.cursor()

        try:
            query = "SELECT * FROM gamblers"
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error fetching gamblers: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    def get_gambler(self, gambler_id):
        connection = create_connection()
        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            query = "SELECT * FROM gamblers WHERE gambler_id = %s"
            cursor.execute(query, (gambler_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching gambler: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    def update_gambler(self, gambler_id, new_stake):
        connection = create_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        UPDATE gamblers
        SET current_stake = %s, updated_at = %s
        WHERE gambler_id = %s
        """

        try:
            cursor.execute(query, (new_stake, datetime.now(), gambler_id))
            connection.commit()
            print("Gambler updated successfully")
        except Exception as e:
            print(f"Error updating gambler: {e}")
        finally:
            cursor.close()
            connection.close()

    def validate_gambler(self, gambler_id):
        gambler = self.get_gambler(gambler_id)

        if gambler is None:
            return False, "Gambler not found"

        current_stake = float(gambler[6])
        min_required = float(gambler[9])
        is_active = gambler[4]

        if not is_active:
            return False, "Account inactive"

        if current_stake < min_required:
            return False, "Insufficient stake"

        return True, "Eligible"

    def reset_gambler(self, gambler_id):
        connection = create_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        UPDATE gamblers
        SET current_stake = initial_stake,
            updated_at = %s
        WHERE gambler_id = %s
        """

        try:
            cursor.execute(query, (datetime.now(), gambler_id))
            connection.commit()
            print("Gambler reset successfully")
        except Exception as e:
            print(f"Error resetting gambler: {e}")
        finally:
            cursor.close()
            connection.close()