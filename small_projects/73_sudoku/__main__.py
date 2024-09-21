import os
import random
import sys
import textwrap
from pathlib import Path
from typing import Final


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


COMMANDS: Final[list[str]] = 'RESET NEW UNDO QUIT'.split()
COLUMNS: Final[set[str]] = set('ABCDEFGHI')
ROWS: Final[set[str]] = set('123456789')
DIGITS = ROWS

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
            case (cell, value):  # this command shall alter the grid
                print(cell, value)

        print(rendered_grid(puzzle))


main()
