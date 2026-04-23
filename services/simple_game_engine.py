from services.game_status_display import GameStatusDisplay
from services.interactive_menu import InteractiveMenu
from services.session_summary import SessionSummary


class SimpleGameEngine:
    def __init__(
        self,
        gambler_service,
        betting_service,
        win_loss_service,
        game_session_manager
    ):
        self.gambler_service = gambler_service
        self.betting_service = betting_service
        self.win_loss_service = win_loss_service
        self.game_session_manager = game_session_manager

        self.display = GameStatusDisplay()
        self.menu = InteractiveMenu()
        self.summary = SessionSummary()

    def display_current_status(self):
        gambler_id = int(input("Enter gambler ID: "))
        gambler_data = self.gambler_service.get_gambler(gambler_id)
        self.display.display_current_status(gambler_data)

    def prompt_for_bet_amount(self):
        amount = self.menu.prompt_for_bet_amount()
        self.display.display_message(f"Accepted bet amount: {amount}")
        return amount

    def show_game_outcome(self):
        outcome = input("Enter outcome (WIN / LOSS): ").strip().upper()
        stake_before = float(input("Enter stake before: "))
        stake_after = float(input("Enter stake after: "))
        payout = float(input("Enter payout amount: "))
        loss = float(input("Enter loss amount: "))

        self.display.display_game_outcome(
            outcome=outcome,
            stake_before=stake_before,
            stake_after=stake_after,
            payout=payout,
            loss=loss
        )

    def present_session_summary(self):
        gambler_id = int(input("Enter gambler ID: "))
        self.game_session_manager.session_summary(gambler_id)

    def start_interactive_demo(self):
        print("\n===== SIMPLE GAME ENGINE DEMO =====")

        gambler_id = int(input("Enter gambler ID: "))
        session_id = int(input("Enter session ID: "))

        while True:
            print("\n--- Demo Actions ---")
            print("1. Show Current Status")
            print("2. Place Single Bet")
            print("3. Show Win/Loss Statistics")
            print("4. Show Session Summary")
            print("0. Exit Demo")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                gambler_data = self.gambler_service.get_gambler(gambler_id)
                self.display.display_current_status(gambler_data)

            elif choice == "2":
                bet_id = int(input("Enter bet ID: "))
                bet_amount = self.menu.prompt_for_bet_amount()
                win_probability = float(input("Enter win probability (0 to 1): "))
                odds_value = float(input("Enter odds value: "))

                self.betting_service.place_bet(
                    bet_id=bet_id,
                    gambler_id=gambler_id,
                    session_id=session_id,
                    bet_amount=bet_amount,
                    win_probability=win_probability,
                    odds_value=odds_value
                )

                gambler_data = self.gambler_service.get_gambler(gambler_id)
                current_stake = gambler_data[6]
                self.display.display_message(f"Updated stake: {current_stake}")

            elif choice == "3":
                self.win_loss_service.show_session_statistics(session_id)

            elif choice == "4":
                self.game_session_manager.session_summary(gambler_id)

            elif choice == "0":
                self.display.display_message("Exiting interactive demo.")
                break

            else:
                print("Invalid choice.")