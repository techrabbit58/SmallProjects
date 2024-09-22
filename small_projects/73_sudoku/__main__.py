import os
import random
import sys
import textwrap
from pathlib import Path
from typing import Final


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
    return COLUMN_INDEX.find(cell[0]) + 9 * (int(cell[1]) - 1)


def is_impossible_move(this: str, other: str) -> bool:
    return this == other or this in DIGITS


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
                sys.exit()
            case (cell_specification, new_value):  # this shall alter the grid
                position = get_cell_position(cell_specification)
                old_value = puzzle[position]
                if is_impossible_move(old_value, new_value):
                    continue
                # TODO: elaborate business logic
                print(cell_specification, '=', position, ':', old_value, '=>', new_value)

        print(rendered_grid(puzzle))


main()
