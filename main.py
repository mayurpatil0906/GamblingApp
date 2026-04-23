from services.gambler_service import GamblerService


def main():
    service = GamblerService()

    print("===== CREATE GAMBLER =====")

    gambler_id = int(input("Enter ID: "))
    username = input("Enter username: ")
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    initial_stake = float(input("Enter initial stake: "))
    win_threshold = float(input("Enter win threshold: "))
    loss_threshold = float(input("Enter loss threshold: "))
    min_required_stake = float(input("Enter minimum required stake: "))

    service.create_gambler(
        gambler_id,
        username,
        full_name,
        email,
        initial_stake,
        win_threshold,
        loss_threshold,
        min_required_stake
    )

    print("Gambler created successfully")


if __name__ == "__main__":
    main()