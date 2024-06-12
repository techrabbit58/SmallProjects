import random
from collections.abc import Callable
from copy import deepcopy

_frame = [
    list('.-------.'),
    list('|       |'),
    list('|       |'),
    list('|       |'),
    list("'-------'"),
]


def _pips(n: int) -> Callable[[], list[tuple[int, int]]]:
    assert 1 <= n <= 6
    return [
        lambda: [(2, 4)],
        lambda: random.choice([[(1, 2), (3, 6)], [(1, 6), (3, 2)]]),
        lambda: random.choice([[(1, 2), (2, 4), (3, 6)], [(1, 6), (2, 4), (3, 2)]]),
        lambda: [(1, 2), (3, 6), (1, 6), (3, 2)],
        lambda: [(1, 2), (3, 6), (2, 4), (1, 6), (3, 2)],
        lambda: random.choice([
            [(1, 2), (1, 4), (1, 6), (3, 2), (3, 4), (3, 6)],
            [(1, 2), (2, 2), (3, 2), (1, 6), (2, 6), (3, 6)],
        ]),
    ][n - 1]


def die_face(n: int) -> list[str]:
    frame = deepcopy(_frame)
    for y, x in _pips(n)():
        frame[y][x] = 'O'
    return [''.join(row) for row in frame]
