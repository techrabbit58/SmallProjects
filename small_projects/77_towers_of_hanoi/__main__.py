"""
The Twers of Hanoi
after Al Sweigart's "Big Book of Small Python Projects"
    (https://inventwithpython.com/bigbookpython)
"""
import textwrap

TOTAL_DISKS = 5
COMPLETE_TOWER = list(range(TOTAL_DISKS, 0, -1))


def ask_player(question: str, choices: list[str]) -> str:
    while True:
        print(question)
        answer = input("> ").strip()
        choice = answer.upper()
        if choice not in choices:
            print(f"'{answer}' is not in {list(choices)}. Try again")
            continue
        break
    return choice


def intro() -> None:
    print(textwrap.dedent("""
    The Towers of Hanoi
    
    Move the tower of disks, one disk at a time, to another tower.
    Larger disks cannot rest on top of a smaller disk.
    """))


def main() -> None:
    intro()
    command = ask_player(
        "Enter the letters of the origin and destination towers, or (Q)uit.\n"
        "e.g. AB to move a disk from tower A to tower B.",
        ["Q"] + "AB AC BC BA BC CA CB".split(),
    )
    if command == "Q":
        print("Thanks for playing.")
    else:
        print(f"{command=}")


main()
