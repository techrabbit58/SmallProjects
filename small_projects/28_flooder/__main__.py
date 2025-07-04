import random
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


@dataclass(kw_only=True, frozen=True)
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


def get_tile_by_color(color: str) -> TileType:
    return next(filter(lambda o: o.color == color, TILE_TYPES))


def get_tile_by_shape(shape: str) -> TileType:
    return next(filter(lambda o: o.shape == shape, TILE_TYPES))


Location: TypeAlias = tuple[int, int]


@dataclass(kw_only=True)
class Board:
    width: int
    height: int
    tiles: dict[Location, TileType] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        for x in range(self.width):  # Initialize the board with random tiles.
            for y in range(self.height):
                self.tiles[x, y] = random.choice(TILE_TYPES)

        for _ in range(self.width * self.height):  # Make several tiles the same as their neighbor.
            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 1)
            self.tiles[x + 1, y] = self.tiles[x, y]

    @property
    def first_tile(self) -> TileType:
        return self.tiles[0, 0]

    @property
    def is_evenly_colored(self) -> bool:
        first_tile = self.first_tile
        color = first_tile.color
        result = True
        for tile in self.tiles.values():
            if tile.color != color:
                result = False
        return result

    def show(self, display_mode: str, *, finish: bool = False):
        term.fg("white")
        print(Glyph.DOWNRIGHT.value + (Glyph.LEFTRIGHT.value * self.width) + Glyph.DOWNLEFT.value)
        for y in range(self.height):
            term.fg("white")
            glyph = ">" if y == 0 and not finish else Glyph.UPDOWN.value
            print(glyph, end="")
            for x in range(self.width):
                tile = self.tiles[x, y]
                term.fg(tile.color)
                shape = tile.shape if display_mode == "shape" else Glyph.BLOCK.value
                print(shape, end="")
            term.fg("white")
            print(Glyph.UPDOWN.value)
        print(Glyph.UPRIGHT.value + (Glyph.LEFTRIGHT.value * self.width) + Glyph.UPLEFT.value)

    def update(self, new_tile: TileType, x: int = 0, y: int = 0, original_color: str = None) -> None:
        if original_color is None:
            original_color = self.tiles[x, y].color

        if new_tile.color == original_color:
            return

        self.tiles[x, y] = new_tile

        for x1, y1 in ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)):
            tile = self.tiles.get((x1, y1))
            if tile is None:
                continue
            if tile.color == original_color:
                self.update(new_tile, x1, y1, original_color)


def intro() -> None:
    term.clear()
    term.fg("white")
    print(textwrap.dedent("""
    *** Flooder *** by Al Sweigart (al@inventwithpython.com)
    
    Set the upper left color/shape, which fills all adjacent
    squares of that color/shape. Try to make the entire board
    the same color/shape.
    """))


def let_player_select() -> str:
    """Let the player select the desired display mode for this game."""
    term.fg("white")
    print("Do you want to play in colorblind mode (Y/N)?")

    while True:
        response = input("> ").strip().upper() or "NO"
        if response in {"Y", "N", "YES", "NO"}:
            break
        print("Please enter (Y)es or (N)o. Try again.")

    print()
    return "shape" if response.startswith("Y") else "color"


def ask_player(moves_left: int, display_mode: str) -> str:
    term.fg("white")
    print(f"Moves left: {moves_left}")
    good_responses = set("q")

    print("Choose one of ", end="")
    if display_mode == "color":
        for choice in "red green blue yellow cyan purple".split():
            term.fg(choice)
            print(f"({choice[0].upper()}){choice[1:].lower()} ", end="")
            good_responses.add(choice[0].lower())
    else:
        for tile in TILE_TYPES:
            term.fg(tile.color)
            choice = Glyph(tile.shape).name
            print(f"({choice[0].upper()}){choice[1:].lower()} ", end="")
            good_responses.add(choice[0].lower())

    term.fg("white")
    print("or (Q)UIT:")

    response = input("> ").lower().strip()
    if not response:
        return "continue"

    if response not in good_responses:
        return "bad"

    if response in "qQ":
        return "quit"

    for tile in TILE_TYPES:
        if display_mode == 'color' and tile.color.startswith(response):
            return tile.color

    for glyph in Glyph:
        if glyph.name.startswith(response.upper()):
            tile = get_tile_by_shape(glyph.value)
            return tile.color

    return "bad"


def game_loop(*, board: Board, moves_left: int, display_mode: str) -> None:
    message = ""

    while True:
        board.show(display_mode)
        print(message)

        answer = ask_player(moves_left, display_mode)
        if answer == "quit":
            message = "\nYou quit. Thank you for playing.\n"
            answer = None
            break

        if answer == "continue":
            message = ""
            continue

        if answer == "bad":
            message = "This is not a valid choice. Try again."
            continue

        new_tile = get_tile_by_color(answer)
        board.update(new_tile)
        message = ""

        if board.is_evenly_colored:
            board.show(display_mode, finish=True)
            message = f"You have won! (Score: {moves_left})\n"
            break

        moves_left -= 1

        if moves_left == 0:
            board.show(display_mode, finish=True)
            message = "You ran out of moves!\n"
            break

    print(message)


def main(*, board_width: int, board_height: int, moves_per_game: int) -> None:
    intro()
    board = Board(height=board_height, width=board_width)
    display_mode = let_player_select()
    game_loop(board=board, moves_left=moves_per_game, display_mode=display_mode)


main(board_width=40, board_height=10, moves_per_game=30)
