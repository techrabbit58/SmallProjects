import textwrap
from dataclasses import field, dataclass
from enum import Enum

from colterm import term
from typing_extensions import TypeAlias


class Glyph(Enum):
    HEART = chr(9829)
    DIAMOND = chr(9830)
    SPADE = chr(9824)
    CLUB = chr(9827)
    BALL = chr(9679)
    TRIANGLE = chr(9650)
    BLOCK = chr(9608)
    LEFTRIGHT = chr(9472)
    UPDOWN = chr(9474)
    DOWNRIGHT = chr(9484)
    DOWNLEFT = chr(9488)
    UPRIGHT = chr(9492)
    UPLEFT = chr(9496)


@dataclass(kw_only=True)
class TileType:
    color: str
    shape: str


TILE_TYPES = [
    TileType(color=color, shape=shape)
    for color, shape in zip(
        "red green blue yellow cyan purple".split(),
        map(lambda o: o.value,
            (Glyph.HEART, Glyph.TRIANGLE, Glyph.DIAMOND, Glyph.BALL, Glyph.CLUB, Glyph.SPADE))
    )
]

Location: TypeAlias = tuple[int, int]


@dataclass(kw_only=True)
class Board:
    width: int
    height: int
    tiles: dict[Location, int] = field(default_factory=dict, init=False)

    @property
    def first_tile(self) -> int:
        return self.tiles[0, 0]

    @property
    def is_evenly_colored(self) -> bool:
        first_tile = self.first_tile
        result = True
        for tile in self.tiles.values():
            if tile != first_tile:
                result = False
        return result


def intro() -> None:
    term.clear()
    term.fg("white")
    print(textwrap.dedent("""
    *** Flooder *** by Al Sweigart (al@inventwithpython.com)
    
    Set the upper left color/shape, which fills all adjacent
    squares of that color/shape. Try to make the entire board
    the same color/shape.
    """))


def game_loop(*, board: Board, moves_per_game: int) -> None:
    print(f"{board=}\n{moves_per_game=}\nshapes=", end="")
    for tt in TILE_TYPES:
        term.fg(tt.color)
        print(tt.shape, end="")
    print("\n")


def endcard() -> None:
    term.fg("white")
    print("Thank you for playing.\n")


def main(*, board_width: int, board_height: int, moves_per_game: int) -> None:
    intro()
    board = Board(height=board_height, width=board_width)
    game_loop(board=board, moves_per_game=moves_per_game)
    endcard()


main(board_width=16, board_height=14, moves_per_game=20)
