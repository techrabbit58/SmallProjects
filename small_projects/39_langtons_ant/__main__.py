import copy
import random
import time
from dataclasses import dataclass, field
from typing import TypeAlias

import colterm.term as term

NUMBER_OF_ANTS = 1
DELAY = 0.1  # seconds

ANT_COLOR = "white"  # foreground
BLACK_TILE = "black"  # background
WHITE_TILE = "white"  # background

BLANK = " "

NORTH, SOUTH, EAST, WEST = "NSEW"
DIRECTIONS = NORTH, SOUTH, EAST, WEST

ANT_IMAGE = dict(zip(DIRECTIONS, "^v><"))
CLOCKWISE = dict(zip(DIRECTIONS, (EAST, WEST, SOUTH, NORTH)))
COUNTER_CLOCKWISE = dict(zip(DIRECTIONS, (WEST, EAST, NORTH, SOUTH)))

DELTA = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0),
}

Location: TypeAlias = tuple[int, int]  # Board locations are tuples: (x, y)


@dataclass
class Board:
    width: int = term.width() - 1
    height: int = term.height() - 1
    black_tiles: set[Location] = field(default_factory=set)
    next_black_tiles: set[Location] = field(default_factory=set)
    needs_update: set[Location] = field(default_factory=set)

    def __post_init__(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.needs_update.add((x, y))


@dataclass
class Ant:
    x: int = field(init=False)
    y: int = field(init=False)
    direction: str = field(init=False)

    def __post_init__(self) -> None:
        self.x = random.randrange(term.width() - 1)
        self.y = random.randrange(term.height() - 1)
        self.direction = random.choice((NORTH, SOUTH, EAST, WEST))

    def update(self, board: Board) -> None:
        x, y = self.x, self.y

        if (x, y) in board.black_tiles:
            self.direction = COUNTER_CLOCKWISE[self.direction]
            board.next_black_tiles.discard((x, y))
        else:
            self.direction = CLOCKWISE[self.direction]
            board.next_black_tiles.add((x, y))

        board.needs_update.add((x, y))

        dx, dy = DELTA[self.direction]
        self.x = (self.x + dx) % board.width
        self.y = (self.y + dy) % board.height

        board.needs_update.add((self.x, self.y))


def refresh_board(board: Board, ants: list[Ant]) -> None:
    term.hide_cursor()

    here_be_ants = {(ant.x, ant.y): ant.direction for ant in ants}
    board.black_tiles = copy.copy(board.next_black_tiles)

    term.fg(ANT_COLOR)
    for x, y in board.needs_update:
        term.bg(BLACK_TILE if (x, y) in board.black_tiles else WHITE_TILE)
        term.goto(x, y)
        mark = ANT_IMAGE[here_be_ants[x, y]] if (x, y) in here_be_ants else BLANK
        print(mark, end="", flush=True)

    board.needs_update = set()

    term.goto(0, board.height)
    term.fg("reset")
    term.bg("reset")
    print("Press Ctrl-C to quit.", end="", flush=True)

    term.show_cursor()


def main() -> None:
    term.fg(ANT_COLOR)
    term.clear()

    board = Board()
    ants = [Ant() for _ in range(NUMBER_OF_ANTS)]

    while True:
        refresh_board(board, ants)

        for ant in ants:
            ant.update(board)

        time.sleep(DELAY)


try:
    main()
except KeyboardInterrupt:
    exit()
