import io
import random

from . import parameters as conf

_WIDTH = conf.get("WIDTH")
_HEIGHT = conf.get("HEIGHT")

_NUM_WALLS = conf.get("NUM_WALLS")
_NUM_DEAD_ROBOTS = conf.get("NUM_DEAD_ROBOTS")
_NUM_ROBOTS = conf.get("NUM_ROBOTS")

_WALL = conf.get("WALL")
_EMPTY = conf.get("EMPTY")
_ROBOT = conf.get("ROBOT")
_DEAD_ROBOT = conf.get("DEAD_ROBOT")
_PLAYER = conf.get("PLAYER")

_robots: list[tuple[int, int]] = [
    (random.randrange(1, _WIDTH - 1), random.randrange(1, _HEIGHT - 1))
    for _ in range(_NUM_ROBOTS)
]


def _init() -> tuple[dict[tuple[int, int], str], tuple[int, int]]:
    board = {}
    for x in range(_WIDTH):
        board[x, 0] = _WALL  # top edge
        board[x, _HEIGHT - 1] = _WALL  # bottom edge
    for y in range(1, _HEIGHT - 1):
        board[0, y] = _WALL  # left edge
        board[_WIDTH - 1, y] = _WALL  # right edge
    for _ in range(_NUM_WALLS):  # add random wall elements into non-robot spaces
        while True:
            x, y = random.randrange(1, _WIDTH - 1), random.randrange(1, _HEIGHT - 1)
            if (x, y) not in _robots:
                board[x, y] = _WALL
                break
    for _ in range(_NUM_DEAD_ROBOTS):  # add some robots that are already dead
        while True:
            x, y = random.randrange(1, _WIDTH - 1), random.randrange(1, _HEIGHT - 1)
            if (x, y) not in _robots and (x, y) not in board:
                board[x, y] = _DEAD_ROBOT
                break
    while True:  # finally set the player's starting point
        x, y = random.randrange(1, _WIDTH - 1), random.randrange(1, _HEIGHT - 1)
        if (x, y) not in _robots:
            player = x, y
            break
    return board, player


_board, _player = _init()


def render() -> str:
    text = io.StringIO()
    for y in range(_HEIGHT):
        for x in range(_WIDTH):
            text.write(
                _board.get((x, y))
                or (
                    _ROBOT if (x, y) in _robots
                    else _PLAYER if (x, y) == _player
                    else _EMPTY
                )
            )
        text.write("\n")
    return text.getvalue()
