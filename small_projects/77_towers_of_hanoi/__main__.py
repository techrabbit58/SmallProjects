"""
The Twers of Hanoi
after Al Sweigart's "Big Book of Small Python Projects"
    (https://inventwithpython.com/bigbookpython)
"""
import textwrap
from typing import TypeAlias

TOTAL_DISKS = 5
COMPLETE_TOWER = list(range(TOTAL_DISKS, 0, -1))
ALL_BLANKS = " " * TOTAL_DISKS

OneTower: TypeAlias = list[int]
TowerKey: TypeAlias = str
TowerArrangement: TypeAlias = dict[TowerKey, OneTower]


def ask_player(question: str, choices: list[str]) -> str:
    choice = ""
    while not choice:
        if choice:
            print(question)
        answer = input("> ").strip()
        if len(answer) == 0:
            continue
        choice = answer.upper()
        if choice not in choices:
            print(f"'{answer}' is not in {list(choices)}. Try again.")
            choice = ""
            continue
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
            disk, mid = (tower[level], str(tower[level]).rjust(2, '_')) \
                if level < len(tower) \
                else (0, "||")
            spaces = ALL_BLANKS[:TOTAL_DISKS - disk]
            solid = "@" * disk
            print(f"{spaces}{solid}{mid}{solid}{spaces}", end=" ")
        print()
    for key in "ABC":
        print(f"{ALL_BLANKS}{key:>2}{ALL_BLANKS}", end=" ")
    print("\n")


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
            break

        origin, destination = command
        origin_tower, destination_tower = towers[origin], towers[destination]

        if not len(origin_tower):
            print(f"Cannot remove a disk from empty pile {origin}. Try again.\n")
            continue

        if len(destination_tower) and origin_tower[-1] > destination_tower[-1]:
            print(f"Cannot move a disk from {origin} to {destination}.")
            print("The original disk is larger then the topmost destination disk.")
            print("Try again.\n")
            continue

        disk = origin_tower.pop()
        destination_tower.append(disk)

        if COMPLETE_TOWER in (towers["B"], towers["C"]):
            display_towers(towers)
            print("You have solved the puzzle. Congratulations.")
            break

    print("Thanks for playing.\n")


main()
