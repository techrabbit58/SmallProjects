import os
import random
import sys
import textwrap
from pathlib import Path
from typing import Final

PUZZLE_SIZE: Final[int] = 9
NUM_BOXES: Final[int] = PUZZLE_SIZE
BOX_SIZE: Final[int] = 3

COMMANDS: Final[list[str]] = 'RESET NEW UNDO QUIT'.split()
COLUMN_INDEX: Final[str] = 'ABCDEFGHI'
COLUMNS: Final[set[str]] = set(COLUMN_INDEX)
ROWS: Final[set[str]] = set('123456789')
DIGITS: Final[set[str]] = ROWS


def intro() -> str:
    return textwrap.dedent("""
        P l a y  S u d o k u !
        ### based on some content and requirements that were originally
        ### created by Al Sweigart <al@inventwithpython.com>
    """)


def rendered_grid(puzzle: list[str]) -> str:
    return textwrap.dedent("""
           A B C   D E F   G H I
        1  {} {} {} | {} {} {} | {} {} {}
        2  {} {} {} | {} {} {} | {} {} {}
        3  {} {} {} | {} {} {} | {} {} {}
           ------+-------+------
        4  {} {} {} | {} {} {} | {} {} {}
        5  {} {} {} | {} {} {} | {} {} {}
        6  {} {} {} | {} {} {} | {} {} {}
           ------+-------+------
        7  {} {} {} | {} {} {} | {} {} {}
        8  {} {} {} | {} {} {} | {} {} {}
        9  {} {} {} | {} {} {} | {} {} {}
        """.format(*puzzle)).strip('\n')


def info() -> str:
    return textwrap.dedent("""
            Enter your move, or RESET, NEW, UNDO, or QUIT.
            For example, a move looks like "B4 9".
        """)


def get_response() -> tuple[str, str]:
    while True:
        try:
            answer = input('> ').strip().upper()
        except KeyboardInterrupt:
            print('^C')
            sys.exit()

        for i, cmd in enumerate(COMMANDS):
            if cmd.startswith(answer):
                return cmd[0], ''

        parts = answer.split()
        if len(parts) == 2:
            cmd, val = parts
            if len(cmd) == 2 and cmd[0] in COLUMNS and cmd[1] in ROWS and val in DIGITS:
                return cmd, val

        print(info())


def new_puzzle() -> list[str]:
    with open(Path(os.path.dirname(sys.argv[0])) / 'sudokupuzzles.txt') as fd:
        return list(random.choice(fd.read().strip().splitlines()))


def get_cell_position(cell: str) -> int:
    return COLUMN_INDEX.find(cell[0]) + PUZZLE_SIZE * (int(cell[1]) - 1)


def rows_are_solved(puzzle: list[str]) -> bool:
    # TODO: fix the row checker
    for row in range(PUZZLE_SIZE):
        all_digits = DIGITS.copy()
        for col in range(PUZZLE_SIZE):
            position = row * PUZZLE_SIZE + col
            all_digits.discard(puzzle[position])
        if len(all_digits) != 0:
            return False

    return True


def columns_are_solved(puzzle: list[str]) -> bool:
    # TODO: fix the column checker
    for col in range(PUZZLE_SIZE):
        all_digits = DIGITS.copy()
        for row in range(PUZZLE_SIZE):
            position = row * PUZZLE_SIZE + col
            all_digits.discard(puzzle[position])
        if len(all_digits) != 0:
            return False

    return True


def boxes_are_solved(puzzle: list[str]) -> bool:
    # TODO: fix the box checker
    for box in range(NUM_BOXES):
        all_digits = DIGITS.copy()
        anchor = box * BOX_SIZE
        for row in range(BOX_SIZE):
            for col in range(BOX_SIZE):
                position = anchor + row * PUZZLE_SIZE + col
                all_digits.discard(puzzle[position])
        if len(all_digits) != 0:
            return False

    return True


def is_solved(puzzle: list[str]) -> bool:
    return all((rows_are_solved(puzzle), columns_are_solved(puzzle), boxes_are_solved(puzzle)))


def main():
    print(intro())

    original = new_puzzle()
    puzzle = original.copy()

    print(rendered_grid(puzzle))
    print(info())

    while True:  # command loop
        match get_response():
            case ('R', _):
                puzzle = original.copy()
            case ('N', _):
                original = new_puzzle()
                puzzle = original.copy()
            case ('U', _):
                pass
            case ('Q', _):
                print('Bye!')
                break
            case (cell_specification, new_value):  # this shall alter the grid
                position = get_cell_position(cell_specification)
                old_value = puzzle[position]
                original_value = original[position]
                if original_value in DIGITS:
                    print('Original values cannot be overridden.')
                elif new_value == old_value:
                    print('No change.')
                else:
                    puzzle[position] = new_value
            case _:
                continue

        print(rendered_grid(puzzle))

        if is_solved(puzzle):
            print('Congratulations! You solved it.')
            break


main()
