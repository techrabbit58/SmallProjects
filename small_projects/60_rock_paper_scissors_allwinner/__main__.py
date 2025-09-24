import textwrap
import time

RPS = {
    "R": "ROCK",
    "P": "PAPER",
    "S": "SCISSORS",
}


def ask_player(question: str, choices: str) -> str:
    while True:
        print(question)
        answer = input("> ").strip()
        choice = answer.upper()
        if len(choice) != 1 or choice not in choices:
            print(f"'{answer}' is not in {list(choices)}. Try again")
            continue
        break
    return choice


def intro() -> None:
    print(textwrap.dedent("""
    Rock, Paper, Scissors

    - Rock beats scissors.
    - Paper beats rocks.
    - Scissors beats paper.    
    """))


def pause_for_suspense() -> None:
    for n in (1, 2, 3):
        time.sleep(0.5)
        print(n, "...")
        time.sleep(0.25)


def main():
    intro()

    wins = 0

    while True:
        print(f"{wins} Wins, 0 Losses, 0 Ties")

        player = ask_player(
            "Enter your move: (R)ock (P)aper (S)cissors or (Q)uit",
            "RPSQ",
        )

        if player == "Q":
            print("Thanks for playing.")
            break

        computer = dict(zip("RPS", "SRP"))[player]

        print(RPS[player], "versus ...")
        pause_for_suspense()
        print(RPS[computer])

        print("You win.")

        wins += 1


main()
