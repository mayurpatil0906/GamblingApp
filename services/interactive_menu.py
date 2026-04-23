class InteractiveMenu:
    def display_main_menu(self):
        print("\n========== GAMBLING APP ==========")
        print("1. Use Case 1 - Gambler Profile Management")
        print("2. Use Case 2 - Stake Management")
        print("3. Use Case 3 - Betting Mechanism")
        print("4. Use Case 4 - Game Session Management")
        print("5. Use Case 5 - Win/Loss Calculation")
        print("6. Use Case 6 - Input Validation and Error Handling")
        print("7. Use Case 7 - User Interaction Demo")
        print("0. Exit")

    def display_user_interaction_menu(self):
        print("\n===== USE CASE 7: USER INTERACTION =====")
        print("1. Display Current Stake and Status")
        print("2. Prompt for Bet Amount")
        print("3. Show Game Outcome")
        print("4. Present Session Summary")
        print("5. Start Interactive Demo")

    def prompt_for_bet_amount(self):
        while True:
            value = input("Enter bet amount: ").strip()
            try:
                amount = float(value)
                if amount <= 0:
                    print("Bet amount must be greater than zero.")
                    continue
                return amount
            except ValueError:
                print("Invalid input. Please enter a valid number.")