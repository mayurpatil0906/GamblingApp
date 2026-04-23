from db.db_connection import create_connection
from datetime import datetime
from services.stake_boundary import StakeBoundary
from services.stake_monitor import StakeMonitor
from models.transaction_type import TransactionType


class StakeManagementService:

    def __init__(self):
        self.monitor = StakeMonitor()
        self.boundary = StakeBoundary(100, 5000)

    def initialize_stake(self, gambler_id, amount):

        connection = create_connection()
        cursor = connection.cursor()

        now = datetime.now()

        cursor.execute(
            "UPDATE gamblers SET current_stake=%s WHERE gambler_id=%s",
            (amount, gambler_id)
        )

        self.monitor.update(amount)

        connection.commit()
        cursor.close()
        connection.close()

        print("Initial stake set")

    # ----------------------------------------

    def process_transaction(self, gambler_id, amount, txn_type):

        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT current_stake FROM gamblers WHERE gambler_id=%s",
            (gambler_id,)
        )

        result = cursor.fetchone()

        if not result:
            print("Gambler not found")
            return

        current = float(result[0])
        amount = float(amount)

        if txn_type == TransactionType.BET_PLACED:
            new = current - amount
        elif txn_type == TransactionType.BET_WIN:
            new = current + amount
        elif txn_type == TransactionType.BET_LOSS:
            new = current - amount
        elif txn_type == TransactionType.DEPOSIT:
            new = current + amount
        elif txn_type == TransactionType.WITHDRAWAL:
            new = current - amount
        elif txn_type == TransactionType.ADJUSTMENT:
            new = current + amount
        else:
            new = current

        # boundary validation
        valid, msg = self.boundary.validate(new)
        if not valid:
            print("Boundary Warning:", msg)

        # update stake
        cursor.execute(
            "UPDATE gamblers SET current_stake=%s WHERE gambler_id=%s",
            (new, gambler_id)
        )

        # insert transaction
        cursor.execute("""
        INSERT INTO stake_transaction (
            transaction_id, gambler_id, session_id, bet_id,
            transaction_type, amount, balance_before, balance_after, created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            int(datetime.now().timestamp()),
            gambler_id,
            None,
            None,
            txn_type.value,
            amount,
            current,
            new,
            datetime.now()
        ))

        self.monitor.update(new)

        connection.commit()
        cursor.close()
        connection.close()

        print("Transaction processed:", txn_type.value)

    # ----------------------------------------

    def report(self):
        stats = self.monitor.get_stats()

        print("\n===== STAKE REPORT =====")
        print("Peak:", stats["peak"])
        print("Lowest:", stats["lowest"])
        print("Total Changes:", stats["changes"])