import os
import random
import sys
import textwrap
from pathlib import Path
from typing import Final

PUZZLE_SIZE: Final[int] = 9
NUM_BOXES: Final[int] = PUZZLE_SIZE
BOX_SIZE: Final[int] = 3

COMMANDS: Final[list[str]] = 'RESET NEW UNDO QUIT HELP'.split()
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
            Enter your move, or HELP, RESET, NEW, UNDO, or QUIT.
            For example, a move looks like "B4 9".
        """)


def get_response() -> tuple[str, str]:
    while True:
        try:
            answer = input('> ').strip().upper()
        except KeyboardInterrupt:
            print('^C')
            sys.exit()

        if not answer:
            return 'CONTINUE', ''

        for cmd in COMMANDS:
            if cmd.startswith(answer):
                return cmd, ''

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
    for row in range(PUZZLE_SIZE):
        all_digits = DIGITS.copy()
        for col in range(PUZZLE_SIZE):
            position = row * PUZZLE_SIZE + col
            all_digits.discard(puzzle[position])
        if len(all_digits) != 0:
            return False

    return True


def columns_are_solved(puzzle: list[str]) -> bool:
    for col in range(PUZZLE_SIZE):
        all_digits = DIGITS.copy()
        for row in range(PUZZLE_SIZE):
            position = row * PUZZLE_SIZE + col
            all_digits.discard(puzzle[position])
        if len(all_digits) != 0:
            return False

    return True


def boxes_are_solved(puzzle: list[str]) -> bool:
    for box_x in (0, BOX_SIZE, BOX_SIZE * 2):
        for box_y in (0, BOX_SIZE, BOX_SIZE * 2):
            all_digits = DIGITS.copy()
            anchor = box_x + box_y * PUZZLE_SIZE
            for col in range(BOX_SIZE):
                for row in range(BOX_SIZE):
                    position = anchor + col + row * PUZZLE_SIZE
                    all_digits.discard(puzzle[position])
        if len(all_digits) != 0:
            return False

    return True


def is_solved(puzzle: list[str]) -> bool:
    return all((rows_are_solved(puzzle), columns_are_solved(puzzle), boxes_are_solved(puzzle)))


def main():
    print(intro())

    original = new_puzzle()
    # original = list('6543219873729586141987645329654321788.7516493431879265213685749746293851589147326')
    puzzle = original.copy()

    print(rendered_grid(puzzle))
    print(info())

    undo_stack = []

    while True:  # command loop
        command = get_response()
        match command:
            case ('RESET', _):
                puzzle = original.copy()
            case ('NEW', _):
                original = new_puzzle()
                puzzle = original.copy()
            case ('UNDO', _):
                if undo_stack:
                    cell_specification, old_value = undo_stack.pop()
                    position = get_cell_position(cell_specification)
                    puzzle[position] = old_value
                else:
                    print('No change. Undo stack is empty.')
            case ('QUIT', _):
                print('Bye!')
                break
            case ('HELP', _):
                print(info())
                continue
            case ('CONTINUE', _):
                pass
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
                    undo_stack.append((cell_specification, old_value))

        print(rendered_grid(puzzle))

        if is_solved(puzzle):
            print('Congratulations! You solved it.')
            break


if __name__ == '__main__':
    main()
