import random
from collections.abc import Iterator
from typing import NamedTuple

WIDTH, HEIGHT = 79, 20


class Cell(NamedTuple):
    x: int
    y: int


_population = {Cell(x, y) for x in range(WIDTH) for y in range(HEIGHT) if random.randint(0, 1) == 0}


def neighborship(cell: Cell) -> Iterator[Cell]:
    x, y = cell
    for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
        yield Cell(x + dx, y + dy)


def init(cells: list[Cell]) -> None:
    global _population
    _population = set(cells)


set_next_generation = init


def get_population() -> list[Cell]:
    return list(_population)


def count_neighbors(cell: Cell) -> int:
    count = 0
    for neighbor in neighborship(cell):
        if neighbor in _population:
            count += 1
    return count


def is_survivor(cell: Cell) -> bool:
    n = count_neighbors(cell)
    if cell in _population and 2 <= n <= 3:
        return True
    if cell not in _population and n == 3:
        return True
    return False
