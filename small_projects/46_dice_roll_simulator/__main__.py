import random
import textwrap
import time


def intro() -> None:
    print(textwrap.dedent("""
    The Million Dice Roll Statistics Simulator 
    by Al Sweigart (al@inventwithpython.com)
        +++ refactored version +++
    """))


def ask_player() -> int:
    print("Enter how many six-sided dice you want to roll:")
    num_dice = 0
    while not num_dice:
        answer = input("> ").strip()
        if not answer.isdigit():
            print("Please give a positive interger number. Try again.")
        elif answer == "0":
            print("Your answer must be greater than zero. Try again.")
        else:
            num_dice = int(answer)
    print()
    return num_dice


def simulate(num_dice: int) -> list[int]:
    print(f"Simulating 1,000,000 rolls of {num_dice} dice ...")

    def roll_dice() -> int:
        return sum(random.randint(1, 6) for _ in range(num_dice))

    results = [0] * (num_dice * 6 + 1)
    timestamp = time.time()
    for turn in range(1_000_000):
        now = time.time()
        if now >= timestamp + 1:
            print(f"{turn / 10_000:.0f}% done ...")
            timestamp = now
        results[roll_dice()] += 1
    print("100% done ...\n")
    return results


def display(num_dice: int, results: list[int]) -> None:
    print("TOTAL -  ROLLS - PERCENTAGE")
    for n, rolls in enumerate(results[num_dice:], num_dice):
        percentage = rolls / 10_000
        print(f"  {n:3d} - {rolls:6d} - {percentage:4.1f}%")
    print()


def main() -> None:
    intro()
    num_dice = ask_player()
    results = simulate(num_dice)
    display(num_dice, results)


main()
