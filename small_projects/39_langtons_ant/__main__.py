import copy
import random
import time
from dataclasses import dataclass, field
from typing import TypeAlias

import colterm.term as term

SCREEN_WIDTH, SCREEN_HEIGHT = (n - 1 for n in term.size())

NUMBER_OF_ANTS = 10
DELAY = 0.1  # seconds

ANT_UP, ANT_DOWN, ANT_LEFT, ANT_RIGHT = "^v<>"

ANT_COLOR = "red"  # foreground
BLACK_TILE = "black"  # background
WHITE_TILE = "white"  # background

NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"

ANT_IMAGE = dict(zip((NORTH, SOUTH, EAST, WEST), (ANT_UP, ANT_DOWN, ANT_LEFT, ANT_RIGHT)))
CLOCKWISE = dict(zip((NORTH, SOUTH, EAST, WEST), (EAST, WEST, SOUTH, NORTH)))
COUNTER_CLOCKWISE = dict(zip((NORTH, SOUTH, EAST, WEST), (WEST, EAST, NORTH, SOUTH)))

DISPLACEMENT = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0),
}

Location: TypeAlias = tuple[int, int]  # Board locations are tuples: (x, y)


@dataclass
class Ant:
    x: int = field(init=False)
    y: int = field(init=False)
    direction: str = field(init=False)

    def __post_init__(self) -> None:
        self.x = random.randint(0, SCREEN_WIDTH - 1)
        self.y = random.randint(0, SCREEN_HEIGHT - 2)
        self.direction = random.choice((NORTH, SOUTH, EAST, WEST))


@dataclass
class Board:
    width: int = SCREEN_WIDTH
    height: int = SCREEN_HEIGHT
    tracks: set[Location] = field(default_factory=set)
    changes: list[Location] = field(default_factory=list)

    def show(self, ants: list[Ant]) -> None:
        for x, y in self.changes:
            term.goto(x, y)
            term.bg(BLACK_TILE if (x, y) in self.tracks else WHITE_TILE)

            for ant in ants:
                if (x, y) == (ant.x, ant.y):
                    print(ANT_IMAGE[ant.direction], end="")
                    break
            else:
                print(" ", end="")

        term.goto(0, SCREEN_HEIGHT)
        term.bg(WHITE_TILE)
        print("Press Ctrl-C to quit.", end="", flush=True)

        time.sleep(DELAY)


def main() -> None:
    term.fg(ANT_COLOR)
    term.bg(WHITE_TILE)
    term.clear()

    board = Board()
    ants = [Ant() for _ in range(NUMBER_OF_ANTS)]

    while True:
        board.show(ants)
        next_board = copy.copy(board)

        for ant in ants:
            if (ant.x, ant.y) in board.tracks:
                ant.direction = CLOCKWISE[ant.direction]
            else:
                next_board.tracks.add((ant.x, ant.y))
                ant.direction = COUNTER_CLOCKWISE[ant.direction]
            next_board.changes.append((ant.x, ant.y))

            dx, dy = DISPLACEMENT[ant.direction]

            ant.x = (ant.x + dx) % SCREEN_WIDTH
            ant.y = (ant.y + dy) % SCREEN_HEIGHT
            next_board.changes.append((ant.x, ant.y))

        board = next_board


main()
