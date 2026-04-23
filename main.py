from services.gambler_service import GamblerService
from services.session_service import SessionService
from services.stake_management_service import StakeManagementService
from models.transaction_type import TransactionType
from services.betting_service import BettingService
from services.game_session_manager import GameSessionManager
from services.win_loss_calculator_service import WinLossCalculatorService
from models.odds_type import OddsType
from services.input_validator import InputValidator
from services.safe_input_handler import SafeInputHandler

gambler_service = GamblerService()
session_service = SessionService()
stake_service = StakeManagementService()
betting_service = BettingService()
game_session_manager = GameSessionManager()
win_loss_service = WinLossCalculatorService()
input_validator = InputValidator()
safe_input = SafeInputHandler()

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
        
def use_case_4_menu():
    print("\n===== USE CASE 4: GAME SESSION MANAGEMENT =====")
    print("1. Start New Session")
    print("2. Continue Session")
    print("3. Pause Session")
    print("4. Resume Session")
    print("5. End Session Manually")
    print("6. Session Summary")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        session_id = int(input("Enter session ID: "))
        gambler_id = int(input("Enter gambler ID: "))
        starting_stake = float(input("Enter starting stake: "))
        lower_limit = float(input("Enter lower limit: "))
        upper_limit = float(input("Enter upper limit: "))
        min_bet = float(input("Enter min bet: "))
        max_bet = float(input("Enter max bet: "))
        max_games = int(input("Enter max games: "))
        max_session_minutes = int(input("Enter max session minutes: "))
        default_win_probability = float(input("Enter default win probability: "))

        game_session_manager.start_new_session(
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

    elif choice == "2":
        gambler_id = int(input("Enter gambler ID: "))
        bet_amount = float(input("Enter bet amount: "))
        outcome = input("Enter outcome (WIN / LOSS): ").strip().upper()

        game_session_manager.continue_session(
            gambler_id=gambler_id,
            bet_amount=bet_amount,
            outcome=outcome
        )

    elif choice == "3":
        gambler_id = int(input("Enter gambler ID: "))
        reason = input("Enter pause reason: ")
        game_session_manager.pause_session(gambler_id, reason)

    elif choice == "4":
        gambler_id = int(input("Enter gambler ID: "))
        game_session_manager.resume_session(gambler_id)

    elif choice == "5":
        gambler_id = int(input("Enter gambler ID: "))
        game_session_manager.end_session_manually(gambler_id)

    elif choice == "6":
        gambler_id = int(input("Enter gambler ID: "))
        game_session_manager.session_summary(gambler_id)

    else:
        print("Invalid choice")
        
def use_case_5_menu():
    print("\n===== USE CASE 5: WIN/LOSS CALCULATION =====")
    print("1. Process Game Result")
    print("2. Show Session Statistics")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        game_id = int(input("Enter game ID: "))
        session_id = int(input("Enter session ID: "))
        bet_id = int(input("Enter bet ID: "))
        gambler_id = int(input("Enter gambler ID: "))
        bet_amount = float(input("Enter bet amount: "))
        odds_type = input("Enter odds type (FIXED / PROBABILITY_BASED / AMERICAN / DECIMAL): ").strip().upper()
        odds_value = float(input("Enter odds value: "))
        win_probability = float(input("Enter win probability (0 to 1): "))
        strategy_type = input("Enter outcome strategy (RANDOM / WEIGHTED): ").strip().upper()

        if strategy_type == "WEIGHTED":
            house_edge = float(input("Enter house edge (e.g. 0.05): "))
        else:
            house_edge = 0.05

        win_loss_service.process_game_result(
            game_id=game_id,
            session_id=session_id,
            bet_id=bet_id,
            gambler_id=gambler_id,
            bet_amount=bet_amount,
            odds_type=odds_type,
            odds_value=odds_value,
            win_probability=win_probability,
            strategy_type=strategy_type,
            house_edge=house_edge
        )

    elif choice == "2":
        session_id = int(input("Enter session ID: "))
        win_loss_service.show_session_statistics(session_id)

    else:
        print("Invalid choice")
        
def use_case_6_menu():
    print("\n===== USE CASE 6: INPUT VALIDATION AND ERROR HANDLING =====")
    print("1. Validate Initial Stake")
    print("2. Validate Bet Amount")
    print("3. Validate Limits")
    print("4. Validate Probability")
    print("5. Validate Stake Non-Negative")
    print("6. Batch Validation")
    print("7. Safe Input Demo")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        try:
            stake = input("Enter initial stake: ")
            valid_stake = input_validator.validate_initial_stake(stake)
            print("Valid initial stake:", valid_stake)
        except Exception as e:
            print(e)

    elif choice == "2":
        try:
            bet_amount = input("Enter bet amount: ")
            current_stake = input("Enter current stake: ")
            min_bet = input("Enter min bet (or press Enter): ").strip()
            max_bet = input("Enter max bet (or press Enter): ").strip()

            min_bet = None if min_bet == "" else float(min_bet)
            max_bet = None if max_bet == "" else float(max_bet)

            valid_bet = input_validator.validate_bet_amount(
                bet_amount,
                current_stake,
                min_bet,
                max_bet
            )
            print("Valid bet amount:", valid_bet)
        except Exception as e:
            print(e)

    elif choice == "3":
        try:
            lower_limit = input("Enter lower limit: ")
            upper_limit = input("Enter upper limit: ")
            initial_stake = input("Enter initial stake: ")

            low, up = input_validator.validate_limits(
                lower_limit,
                upper_limit,
                initial_stake
            )
            print("Valid limits:", low, up)
        except Exception as e:
            print(e)

    elif choice == "4":
        try:
            probability = input("Enter probability: ")
            valid_probability = input_validator.validate_probability(probability)
            print("Valid probability:", valid_probability)
        except Exception as e:
            print(e)

    elif choice == "5":
        try:
            stake = input("Enter stake: ")
            valid_stake = input_validator.validate_stake_non_negative(stake)
            print("Valid stake:", valid_stake)
        except Exception as e:
            print(e)

    elif choice == "6":
        initial_stake = input("Enter initial stake: ")
        lower_limit = input("Enter lower limit: ")
        upper_limit = input("Enter upper limit: ")
        bet_amount = input("Enter bet amount: ")
        current_stake = input("Enter current stake: ")
        probability = input("Enter probability: ")

        result = input_validator.validate_all(
            initial_stake=initial_stake,
            bet_amount=bet_amount,
            current_stake=current_stake,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            probability=probability
        )
        result.print_summary()

    elif choice == "7":
        print("\n--- Safe Input Demo ---")
        stake = safe_input.get_valid_initial_stake("Enter valid initial stake: ")
        print("Accepted initial stake:", stake)

        probability = safe_input.get_valid_probability("Enter valid probability: ")
        print("Accepted probability:", probability)

    else:
        print("Invalid choice")

def main():
    while True:
        print("\n========== GAMBLING APP ==========")
        print("1. Use Case 1 - Gambler Profile Management")
        print("2. Use Case 2 - Stake Management")
        print("3. Use Case 3 - Betting Mechanism")
        print("4. Use Case 4 - Game Session Management")
        print("5. Use Case 5 - Win/Loss Calculation")
        print("6. Use Case 6 - Input Validation and Error Handling")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            use_case_1_menu()
        elif choice == "2":
            use_case_2_menu()
        elif choice == "3":
            use_case_3_menu()
        elif choice == "4":
            use_case_4_menu()
        elif choice == "5":
            use_case_5_menu()
        elif choice == "6":
            use_case_6_menu()
        elif choice == "0":
            print("Exiting application...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()