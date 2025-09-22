import io
import random
from typing import TypeAlias

from . import parameters as conf

_WIDTH = conf.get("WIDTH")
_HEIGHT = conf.get("HEIGHT")

_NUM_WALLS = conf.get("NUM_WALLS")
_NUM_DEAD_ROBOTS = conf.get("NUM_DEAD_ROBOTS")
_NUM_ROBOTS = conf.get("NUM_ROBOTS")

XYPair: TypeAlias = tuple[int, int]


def _colorized(symbol: str, *, color: str) -> str:
    return f"\x1b[{color}m{symbol}\x1b[0m"


_WALL = conf.get("WALL")
_EMPTY = conf.get("EMPTY")
_CRASH_SITE = _colorized(conf.get('DEAD_ROBOT'), color="1")
_ROBOT_SYMBOL = _colorized(conf.get('ROBOT'), color="33")
_player_symbol = _colorized(conf.get('PLAYER'), color="1;32")


def _init() -> tuple[dict[XYPair, str], list[XYPair], XYPair]:
    robots = []
    for _ in range(_NUM_ROBOTS):
        while True:
            x, y = random.randrange(1, _WIDTH - 1), random.randrange(1, _HEIGHT - 1)
            if (x, y) not in robots:
                robots.append((x, y))
                break

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
            if (x, y) not in robots:
                board[x, y] = _WALL
                break

    for _ in range(_NUM_DEAD_ROBOTS):  # add some robots to the board that are already dead
        while True:
            x, y = random.randrange(1, _WIDTH - 1), random.randrange(1, _HEIGHT - 1)
            if (x, y) not in robots and (x, y) not in board:
                board[x, y] = _CRASH_SITE
                break

    while True:  # finally set the player's starting point
        x, y = random.randrange(1, _WIDTH - 1), random.randrange(1, _HEIGHT - 1)
        if not ((x, y) in board or (x, y) in robots):
            player = x, y
            break

    return board, robots, player


_board, _robots, _player = _init()
_teleports = conf.get("NUM_TELEPORTS")
_messages: list[str] = []


def render() -> str:
    text = io.StringIO()

    for y in range(_HEIGHT):
        for x in range(_WIDTH):
            text.write(
                _board.get((x, y))
                or (
                    _player_symbol if (x, y) == _player
                    else _ROBOT_SYMBOL if (x, y) in _robots
                    else _EMPTY
                )
            )
        text.write("\n")

    print("\n".join(_messages), file=text)
    _messages.clear()

    if not is_frozen():
        print(f"(T)eleports remaining: {_teleports}", file=text)
        print("                         ({}) ({}) ({})\n"
              "                         ({}) (S) ({})\n"
              "Enter your move or QUIT: ({}) ({}) ({})".format(*get_valid_moves()), file=text)

    return text.getvalue().strip()


NEIGHBOURSHIP = {
    (-1, -1): "Q",
    (0, -1): "W",
    (1, -1): "E",
    (-1, 0): "A",
    (1, 0): "D",
    (-1, 1): "Z",
    (0, 1): "X",
    (1, 1): "C",
}

BLANK = " "


def get_valid_moves() -> list[str]:
    if is_frozen(): return [" "] * 8
    x, y = _player
    labels = []
    for (dx, dy), label in NEIGHBOURSHIP.items():
        neighbour = x + dx, y + dy
        labels.append(BLANK if (neighbour in _robots or neighbour in _board) else label)
    return labels


def add_message(message: str) -> None:
    _messages.append(message)


_is_frozen = False


def is_frozen() -> bool:
    return _is_frozen


def _freeze() -> None:
    global _is_frozen
    _is_frozen = True


def move_all_robots() -> None:
    global _player_symbol
    if is_frozen(): return
    new_positions = []
    px, py = _player
    while len(_robots):
        rx, ry = _robots.pop()
        if is_frozen():
            new_position = rx, ry
        else:
            dx = 1 if rx < px else -1 if rx > px else 0
            dy = 1 if ry < py else -1 if ry > py else 0
            if _board.get((rx + dx, ry + dy)) != _WALL:
                new_position = rx + dx, ry + dy
            elif _board.get((rx + dx, ry)) != _WALL:
                new_position = rx + dx, ry
            elif _board.get((rx, ry + dy)) != _WALL:
                new_position = rx, ry + dy
            else:
                new_position = rx, ry
            if _board.get(new_position) == _CRASH_SITE:  # robot runs into a crash site and vanishes
                new_position = None
            if new_position in _robots:  # robot runs into another, creates a new crash site and both vanish
                _board[new_position] = _CRASH_SITE
                _robots.remove(new_position)
                new_position = None
            if new_position in new_positions: # robot runs into another in the middle of a move
                _board[new_position] = _CRASH_SITE
                new_positions.remove(new_position)
                new_position = None
            if new_position == _player:
                _player_symbol = _colorized(conf.get('ROBOT'), color="1;31")
                _freeze()
        if new_position:
            new_positions.append(new_position)
    _robots.extend(new_positions)
    if not _robots:
        _freeze()


def is_player_alive() -> bool:
    return _player not in _robots


def get_num_robots() -> int:
    return len(_robots)


def move_player(move: str) -> None:
    global _player
    if is_frozen(): return
    for key, value in NEIGHBOURSHIP.items():
        if move == value:
            x, y = _player
            dx, dy = key
            _player = x + dx, y + dy
            break


def move_player_random() -> None:
    global _player, _teleports
    if is_frozen(): return
    while True:
        x = random.randrange(1, _WIDTH - 1)
        y = random.randrange(1, _HEIGHT - 1)
        new_position = x, y
        if all((new_position != _player, new_position not in _robots, new_position not in _board)):
            _player = x, y
            _teleports -= 1
            break


def get_num_teleports() -> int:
    return _teleports
