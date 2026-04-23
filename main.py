from services.gambler_service import GamblerService
from services.session_service import SessionService
from services.stake_management_service import StakeManagementService
from models.transaction_type import TransactionType
from services.betting_service import BettingService

gambler_service = GamblerService()
session_service = SessionService()
stake_service = StakeManagementService()
betting_service = BettingService()

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
        
def use_case_3_menu():
    print("\n===== USE CASE 3: BETTING MECHANISM =====")
    print("1. Place Single Bet")
    print("2. Place Bet with Strategy")
    print("3. Place Multiple Consecutive Bets")
    print("4. Betting Session Summary")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        bet_id = int(input("Enter bet ID: "))
        gambler_id = int(input("Enter gambler ID: "))
        session_id = int(input("Enter session ID: "))
        bet_amount = float(input("Enter bet amount: "))
        win_probability = float(input("Enter win probability (0 to 1): "))
        odds_value = float(input("Enter odds value: "))

        betting_service.place_bet(
            bet_id, gambler_id, session_id,
            bet_amount, win_probability, odds_value
        )

    elif choice == "2":
        bet_id = int(input("Enter bet ID: "))
        gambler_id = int(input("Enter gambler ID: "))
        session_id = int(input("Enter session ID: "))
        strategy_name = input("Enter strategy (FIXED / PERCENTAGE / MARTINGALE / REVERSE_MARTINGALE / FIBONACCI / DALEMBERT): ").strip()
        base_amount = float(input("Enter base amount: "))
        odds_value = float(input("Enter odds value: "))
        win_probability_input = input("Enter win probability or press Enter for default: ").strip()

        win_probability = float(win_probability_input) if win_probability_input else None

        betting_service.place_bet_with_strategy(
            bet_id=bet_id,
            gambler_id=gambler_id,
            session_id=session_id,
            strategy_name=strategy_name,
            base_amount=base_amount,
            odds_value=odds_value,
            win_probability=win_probability
        )

    elif choice == "3":
        start_bet_id = int(input("Enter starting bet ID: "))
        gambler_id = int(input("Enter gambler ID: "))
        session_id = int(input("Enter session ID: "))
        strategy_name = input("Enter strategy: ").strip()
        rounds = int(input("Enter number of rounds: "))
        base_amount = float(input("Enter base amount: "))
        odds_value = float(input("Enter odds value: "))
        win_probability_input = input("Enter win probability or press Enter for default: ").strip()

        win_probability = float(win_probability_input) if win_probability_input else None

        betting_service.place_consecutive_bets(
            start_bet_id=start_bet_id,
            gambler_id=gambler_id,
            session_id=session_id,
            strategy_name=strategy_name,
            rounds=rounds,
            base_amount=base_amount,
            odds_value=odds_value,
            win_probability=win_probability
        )

    elif choice == "4":
        session_id = int(input("Enter session ID: "))
        gambler_id = int(input("Enter gambler ID: "))
        betting_service.get_betting_session_summary(session_id, gambler_id)

    else:
        print("Invalid choice")

def main():
    while True:
        print("\n========== GAMBLING APP ==========")
        print("1. Use Case 1 - Gambler Profile Management")
        print("2. Use Case 2 - Stake Management")
        print("3. Use Case 3 - Betting Mechanism")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            use_case_1_menu()
        elif choice == "2":
            use_case_2_menu()
        elif choice == "3":
            use_case_3_menu()
        elif choice == "0":
            print("Exiting application...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()