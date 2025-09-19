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


class Board:
    def __init__(self, num_moves: int = 200):
        self.board = deepcopy(NEW_BOARD)
        self.blank = self._find_blank_space()
        for _ in range(num_moves):
            self._make_random_move()

    def _find_blank_space(self) -> tuple[int, int]:
        board = self.board
        for x in range(4):
            for y in range(4):
                if board[x][y] == BLANK:
                    return x, y
        return -1, -1  # this line shall never be reached

    def apply(self, move: str) -> None:
        board = self.board
        blankx, blanky = self.blank
        if move == "W":
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        if move == "A":
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        if move == "S":
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        if move == "D":
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
        self.blank = self._find_blank_space()

    def _make_random_move(self) -> None:
        blankx, blanky = self.blank
        valid_moves = []
        if blanky != 3:
            valid_moves.append("W")
        if blankx != 3:
            valid_moves.append("A")
        if blanky != 0:
            valid_moves.append("S")
        if blankx != 0:
            valid_moves.append("D")
        self.apply(move=random.choice(valid_moves))

    def __str__(self) -> str:
        board = self.board
        labels = []
        for y in range(4):
            for x in range(4):
                labels.append(board[x][y].ljust(2))
        return textwrap.dedent("""
        Sliding Tile Puzzle
        
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

    @property
    def valid_moves(self) -> tuple[str, str, str, str]:
        blankx, blanky = self.blank
        w = "W" if blanky != 3 else " "
        a = "A" if blankx != 3 else " "
        s = "S" if blanky != 0 else " "
        d = "D" if blankx != 0 else " "
        return w, a, s, d

    @property
    def is_ordered(self) -> bool:
        return self.board == NEW_BOARD


def get_next_move(valid_moves: tuple[str, str, str, str]) -> str:
    w, a, s, d = valid_moves
    answer = None
    while not answer:
        print(f"                          ({w})")
        print(f"Enter WASD (or Quit): ({a}) ({s}) ({d})")
        answer = input("> ").strip().upper()
        if answer in f"QUIT Q {w} {a} {s} {d}".split():
            continue
        answer = None
    return answer


def main() -> None:
    clear_screen()
    print(intro())
    input("Press Enter to begin...")

    board = Board()

    while True:
        clear_screen()
        print(board)
        move = get_next_move(board.valid_moves)

        if move in {"Q", "QUIT"}:
            break

        board.apply(move)

        if board.is_ordered:
            clear_screen()
            print(board)
            print("You got it!")
            break

    print("\nThanks for playing!\n")


try:
    main()
except KeyboardInterrupt:
    pass
