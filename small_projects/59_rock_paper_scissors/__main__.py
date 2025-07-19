import random
import textwrap
import time

RPS = {
    "R": "ROCK",
    "P": "PAPER",
    "S": "SCISSORS",
}
OUTCOME = {
    (1, 0, 0): "You win.",
    (0, 1, 0): "You lose.",
    (0, 0, 1): "It's a tie.",
}


def ask_player(question: str, choices: str) -> str:
    while True:
        print(question)
        answer = input("> ").strip()
        choice = answer.upper()
        if len(choice) != 1 and choice not in choices:
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


def apply_rules(player: str, computer: str) -> tuple[int, int, int]:
    if player == computer:
        return 0, 0, 1
    else:
        return {
            "RS": (1, 0, 0),
            "PR": (1, 0, 0),
            "SP": (1, 0, 0),
            "RP": (0, 1, 0),
            "PS": (0, 1, 0),
            "SR": (0, 1, 0),
        }[player + computer]


def main():
    intro()

    wins = losses = ties = 0

    while True:
        print(f"{wins} Wins, {losses} Losses, {ties} Ties")

        player = ask_player(
            "Enter your move: (R)ock (P)aper (S)cissors or (Q)uit",
            "RPSQ",
        )

        if player == "Q":
            print("Thanks for playing.")
            break

        computer = random.choice("RPS")

        print(RPS[player], "versus ...")
        pause_for_suspense()
        print(RPS[computer])
        time.sleep(0.5)

        w, l, t = apply_rules(player, computer)
        print(OUTCOME[w, l, t])

        wins, losses, ties = wins + w, losses + l, ties + t


main()
