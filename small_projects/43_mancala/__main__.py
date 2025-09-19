import os
import sys
import textwrap
from collections.abc import Iterable
from dataclasses import dataclass

PLAYER_1_PITS = tuple("ABCDEF")
PLAYER_1_STORE = "1"
PLAYER_2_PITS = tuple("GHIKLM")
PLAYER_2_STORE = "2"

PIT_LABELS = ''.join(PLAYER_1_PITS) + PLAYER_1_STORE + ''.join(reversed(PLAYER_2_PITS)) + PLAYER_2_STORE
OPPOSITE_PIT = dict(zip(PLAYER_1_PITS + PLAYER_2_PITS, PLAYER_2_PITS + PLAYER_1_PITS))
NEXT_PIT = {a: b for a, b in zip(PIT_LABELS, PIT_LABELS[1:] + PIT_LABELS)}
RENDER_SEQUENCE = PLAYER_2_PITS + (PLAYER_2_STORE, PLAYER_1_STORE) + PLAYER_1_PITS

INITIAL_SEEDS_PER_PIT = 4
INITIAL_SEEDS_PER_STORE = 0

INTRO_TEXT = """
M A N C A L A

Two players try to grab as many seeds as possible from a two rows,
six pits each. Every pit does initially contain {} seeds. The players
take alternating turns. The player whose turn it is grabs all seeds
from one of the pits on her side and places them one by one to the
subsequent pits in counterclockwise direction, but always skips the
store of the opponent. If the last seed lands in an empty pit, the
player grabs all the seeds from the pit on the opposite side. Seeds
can never be grabbed from a store.

The game ends if all of one player's pits are empty. The other player
then claims all remaining seeds from his own pits for their store.

The winner is who eventually has the most seeds in her store.
""".format(INITIAL_SEEDS_PER_PIT)


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)


class Board:
    def __init__(self) -> None:
        self._board: dict[str, int] = {}
        for store in PLAYER_1_STORE + PLAYER_2_STORE:
            self._board[store] = INITIAL_SEEDS_PER_STORE
        for pit in PLAYER_1_PITS + PLAYER_2_PITS:
            self._board[pit] = INITIAL_SEEDS_PER_PIT

    def __str__(self) -> str:
        return textwrap.dedent("""
        M A N C A L A
        
        +------+------+--<<<<<-Player 2----+------+------+------+
        2      |G     |H     |I     |K     |L     |M     |      1
               |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |       
        S      |      |      |      |      |      |      |      S
        T  {}  +------+------+------+------+------+------+  {}  T
        O      |A     |B     |C     |D     |E     |F     |      O
        R      |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      R
        E      |      |      |      |      |      |      |      E
        +------+------+------+-Player 1->>>>>-----+------+------+
        """.format(*(f"{self._board[label]:2d}" for label in RENDER_SEQUENCE)))

    def is_empty_pit(self, move: str) -> bool:
        return self._board[move] == 0


@dataclass(kw_only=True, frozen=True)
class Player:
    store: str
    pits: Iterable[str]


def main() -> None:
    clear_screen()
    print(INTRO_TEXT)
    input("Press Enter to begin...")

    board = Board()
    player = Player(store=PLAYER_1_STORE, pits=PLAYER_1_PITS)
    opponent = Player(store=PLAYER_2_STORE, pits=PLAYER_2_PITS)
    error = False

    while True:
        clear_screen()
        print(board)

        print(f"Ready player {player.store}.")
        if error:
            print("You can only choose from the non-empty pits on your own side.")
            error = False
        print(f"Choose your move: {', '.join(player.pits)} (or Quit).")

        valid_moves = {"QUIT", "Q"}.union(*(pit for pit in player.pits if not board.is_empty_pit(pit)))
        move = input("> ").strip().upper()

        if not move:
            continue

        if move not in valid_moves:
            error = True
            continue

        if move in {"Q", "QUIT"}:
            break

        player, opponent = opponent, player

    print("\nThanks for playing!\n")


try:
    main()
except KeyboardInterrupt:
    pass