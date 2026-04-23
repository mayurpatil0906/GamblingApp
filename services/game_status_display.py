class GameStatusDisplay:
    def display_current_status(self, gambler_data):
        if gambler_data is None:
            print("No gambler data found.")
            return

        print("\n===== CURRENT GAMBLER STATUS =====")
        print(f"Gambler ID       : {gambler_data[0]}")
        print(f"Username         : {gambler_data[1]}")
        print(f"Full Name        : {gambler_data[2]}")
        print(f"Email            : {gambler_data[3]}")
        print(f"Active           : {gambler_data[4]}")
        print(f"Initial Stake    : {gambler_data[5]}")
        print(f"Current Stake    : {gambler_data[6]}")
        print(f"Win Threshold    : {gambler_data[7]}")
        print(f"Loss Threshold   : {gambler_data[8]}")
        print(f"Min Req. Stake   : {gambler_data[9]}")
        print(f"Created At       : {gambler_data[10]}")
        print(f"Updated At       : {gambler_data[11]}")

    def display_game_outcome(self, outcome, stake_before, stake_after, payout=0.0, loss=0.0):
        print("\n===== GAME OUTCOME =====")
        print(f"Outcome          : {outcome}")
        print(f"Stake Before     : {stake_before}")
        print(f"Stake After      : {stake_after}")
        print(f"Payout Amount    : {payout}")
        print(f"Loss Amount      : {loss}")

    def display_message(self, message):
        print(f"\n>>> {message}")