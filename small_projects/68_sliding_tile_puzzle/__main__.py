import os
import random
import sys
import textwrap
from copy import deepcopy

BLANK = "  "  # two spaces!!!
NEW_BOARD = [
    "1 5 9 13".split(),
    "2 6 10 14".split(),
    "3 7 11 15".split(),
    "4 8 12".split() + [BLANK]
]


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)


def intro():
    return textwrap.dedent("""
    Sliding Tile Puzzle
    
    Use the WASD keys to move tiles back into their original order:
    
        1   2   3   4
        5   6   7   8
        9   10  11  12
        13  14  15
    """)


def find_blank_space(board: list[list[str]]) -> tuple[int, int]:
    for x in range(4):
        for y in range(4):
            if board[x][y] == BLANK:
                return x, y
    return -1, -1  # this line shall never be reached


def apply_move(board: list[list[str]], *, move: str) -> None:
    bx, by = find_blank_space(board)
    if move == "W":
        board[bx][by], board[bx][by + 1] = board[bx][by + 1], board[bx][by]
    if move == "A":
        board[bx][by], board[bx + 1][by] = board[bx + 1][by], board[bx][by]
    if move == "S":
        board[bx][by], board[bx][by - 1] = board[bx][by - 1], board[bx][by]
    if move == "D":
        board[bx][by], board[bx - 1][by] = board[bx - 1][by], board[bx][by]


def make_random_move(board: list[list[str]]) -> None:
    blankx, blanky = find_blank_space(board)
    valid_moves = []
    if blanky != 3:
        valid_moves.append("W")
    if blankx != 3:
        valid_moves.append("A")
    if blanky != 0:
        valid_moves.append("S")
    if blankx != 0:
        valid_moves.append("D")
    apply_move(board, move=random.choice(valid_moves))


def create_new_puzzle(num_moves: int = 200) -> list[list[str]]:
    puzzle = deepcopy(NEW_BOARD)
    for i in range(num_moves):
        make_random_move(puzzle)
    return puzzle


def render_the_board(board: list[list[str]]) -> str:
    labels = []
    for y in range(4):
        for x in range(4):
            labels.append(board[x][y].ljust(2))
    return textwrap.dedent("""
    +------+------+------+------+
    |      |      |      |      |
    |  {}  |  {}  |  {}  |  {}  |
    |      |      |      |      |
    +------+------+------+------+
    |      |      |      |      |
    |  {}  |  {}  |  {}  |  {}  |
    |      |      |      |      |
    +------+------+------+------+
    |      |      |      |      |
    |  {}  |  {}  |  {}  |  {}  |
    |      |      |      |      |
    +------+------+------+------+
    |      |      |      |      |
    |  {}  |  {}  |  {}  |  {}  |
    |      |      |      |      |
    +------+------+------+------+
    """.format(*labels))


def get_next_move(board: list[list[str]]) -> str:
    blankx, blanky = find_blank_space(board)
    w = "W" if blanky != 3 else " "
    a = "A" if blankx != 3 else " "
    s = "S" if blanky != 0 else " "
    d = "D" if blankx != 0 else " "
    answer = None
    while not answer:
        print(f"                       ({w})")
        print(f"Enter WASD (or Q): ({a}) ({s}) ({d})")
        answer = input("> ").strip().upper()
        if answer in "QUIT" + (w + a + s + d).replace(" ", ""):
            continue
        answer = None
    return answer


def main() -> None:
    clear_screen()
    print(intro())
    input("Press Enter to begin...")

    board = create_new_puzzle()

    while True:
        clear_screen()
        print(render_the_board(board))
        move = get_next_move(board)

        if move in {"Q", "QUIT"}:
            break

        apply_move(board, move=move)

        if board == NEW_BOARD:
            clear_screen()
            print(render_the_board(board))
            print("You got it!")
            break

    print("\nThanks for playing!\n")


try:
    main()
except KeyboardInterrupt:
    pass
