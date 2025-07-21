"""
The Twers of Hanoi
after Al Sweigart's "Big Book of Small Python Projects"
    (https://inventwithpython.com/bigbookpython)
"""
import textwrap
from typing import TypeAlias

TOTAL_DISKS = 5
COMPLETE_TOWER = list(range(TOTAL_DISKS, 0, -1))


OneTower: TypeAlias = list[int]
TowerKey: TypeAlias = str
TowerArrangement: TypeAlias = dict[TowerKey, OneTower]


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


def set_up_the_towers() -> TowerArrangement:
    return {"A": COMPLETE_TOWER.copy(), "B": [], "C": []}


def display_towers(towers: TowerArrangement) -> None:
    for level in range(TOTAL_DISKS, -1, -1):
        for key in "ABC":
            tower = towers[key]
            if level >= len(tower):
                spaces = " " * TOTAL_DISKS
                print(f"{spaces}||{spaces}", end="")
            else:
                disk = tower[level]
                spaces = " " * (TOTAL_DISKS - disk)
                solid = "@" * disk
                print(f"{spaces}{solid}_{disk}{solid}{spaces}", end="")
        print()


def main() -> None:
    intro()

    towers = set_up_the_towers()

    while True:
        display_towers(towers)

        command = ask_player(
            "Enter the letters of the origin and destination towers, or (Q)uit.\n"
            "e.g. AB to move a disk from tower A to tower B.",
            ["Q"] + "AB AC BC BA BC CA CB".split(),
        )

        if command == "Q":
            print("Thanks for playing.")
            break

        print(f"{command=}")


main()
