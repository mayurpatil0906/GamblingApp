from services.gambler_service import GamblerService
from services.session_service import SessionService
from services.stake_management_service import StakeManagementService
from models.transaction_type import TransactionType


gambler_service = GamblerService()
session_service = SessionService()
stake_service = StakeManagementService()

def use_case_1_menu():
    print("\n===== USE CASE 1: GAMBLER PROFILE MANAGEMENT =====")
    print("1. Create Gambler")
    print("2. Get Gambler")
    print("3. Update Gambler Stake")
    print("4. Validate Gambler")
    print("5. Reset Gambler")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        gambler_id = int(input("Enter ID: "))
        username = input("Enter username: ")
        full_name = input("Enter full name: ")
        email = input("Enter email: ")
        initial_stake = float(input("Enter initial stake: "))
        win_threshold = float(input("Enter win threshold: "))
        loss_threshold = float(input("Enter loss threshold: "))
        min_required_stake = float(input("Enter minimum required stake: "))

        gambler_service.create_gambler(
            gambler_id,
            username,
            full_name,
            email,
            initial_stake,
            win_threshold,
            loss_threshold,
            min_required_stake
        )

    elif choice == "2":
        gambler_id = int(input("Enter gambler ID: "))
        gambler = gambler_service.get_gambler(gambler_id)
        print("Gambler Data:", gambler)

    elif choice == "3":
        gambler_id = int(input("Enter gambler ID: "))
        new_stake = float(input("Enter new stake: "))
        gambler_service.update_gambler(gambler_id, new_stake)

    elif choice == "4":
        gambler_id = int(input("Enter gambler ID: "))
        status, message = gambler_service.validate_gambler(gambler_id)
        print("Validation:", status, message)

    elif choice == "5":
        gambler_id = int(input("Enter gambler ID: "))
        gambler_service.reset_gambler(gambler_id)

    else:
        print("Invalid choice")


def use_case_2_menu():
    print("\n===== USE CASE 2: STAKE MANAGEMENT =====")
    print("1. Initialize Stake")
    print("2. Place Bet")
    print("3. Win")
    print("4. Loss")
    print("5. Deposit")
    print("6. Withdrawal")
    print("7. Adjustment")
    print("8. Report")

    choice = input("Enter choice: ").strip()
    gambler_id = int(input("Enter gambler ID: "))

    if choice == "1":
        amount = float(input("Enter initial stake: "))
        stake_service.initialize_stake(gambler_id, amount)

    elif choice == "2":
        amount = float(input("Enter bet amount: "))
        stake_service.process_transaction(
            gambler_id, amount, TransactionType.BET_PLACED
        )

    elif choice == "3":
        amount = float(input("Enter win amount: "))
        stake_service.process_transaction(
            gambler_id, amount, TransactionType.BET_WIN
        )

    elif choice == "4":
        amount = float(input("Enter loss amount: "))
        stake_service.process_transaction(
            gambler_id, amount, TransactionType.BET_LOSS
        )

    elif choice == "5":
        amount = float(input("Enter deposit amount: "))
        stake_service.process_transaction(
            gambler_id, amount, TransactionType.DEPOSIT
        )

    elif choice == "6":
        amount = float(input("Enter withdrawal amount: "))
        stake_service.process_transaction(
            gambler_id, amount, TransactionType.WITHDRAWAL
        )

    elif choice == "7":
        amount = float(input("Enter adjustment amount: "))
        stake_service.process_transaction(
            gambler_id, amount, TransactionType.ADJUSTMENT
        )

    elif choice == "8":
        stake_service.report()

    else:
        print("Invalid choice")

def main():
    while True:
        print("\n========== GAMBLING APP ==========")
        print("1. Use Case 1 - Gambler Profile Management")
        print("2. Use Case 2 - Stake Management")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            use_case_1_menu()
        elif choice == "2":
            use_case_2_menu()
        elif choice == "0":
            print("Exiting application...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()