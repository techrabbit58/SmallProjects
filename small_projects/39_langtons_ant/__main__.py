import copy
import random
import time
from dataclasses import dataclass, field
from typing import TypeAlias

import colterm.term as term

NUMBER_OF_ANTS = 10
DELAY = 0.1  # seconds

BLACK_TILE = "green"  # background
WHITE_TILE = "blue"  # background
ANT_COLOR = "cyan"  # foreground

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
    changed_tiles: set[Location] = field(default_factory=set)

    def update(self) -> None:
        self.black_tiles = copy.copy(self.next_black_tiles)

    def render(self, ants: list["Ant"]) -> None:
        term.hide_cursor()

        here_be_ants = {(ant.x, ant.y): ant.direction for ant in ants}

        term.fg(ANT_COLOR)
        for x, y in self.changed_tiles:
            term.bg(BLACK_TILE if (x, y) in self.black_tiles else WHITE_TILE)
            term.goto(x, y)
            mark = ANT_IMAGE[here_be_ants[x, y]] if (x, y) in here_be_ants else BLANK
            print(mark, end="", flush=True)

        term.goto(0, self.height)
        term.fg("reset")
        term.bg("reset")
        print("Press Ctrl-C to quit.", end="", flush=True)

        term.show_cursor()

        self.changed_tiles = set()


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

        board.changed_tiles.add((x, y))

        dx, dy = DELTA[self.direction]
        self.x = (self.x + dx) % board.width
        self.y = (self.y + dy) % board.height

        board.changed_tiles.add((self.x, self.y))


def main() -> None:
    board = Board()
    ants = [Ant() for _ in range(NUMBER_OF_ANTS)]

    term.fg(ANT_COLOR)
    term.clear()

    while True:
        board.update()
        board.render(ants)
        for ant in ants:
            ant.update(board)
        time.sleep(DELAY)


try:
    main()
except KeyboardInterrupt:
    exit()
