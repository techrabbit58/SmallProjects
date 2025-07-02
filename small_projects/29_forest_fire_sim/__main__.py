"""
Forset Fire Sim, by Al Sweigart (al@inventwithpython.com)
After "The Big Book of Small Python Projects" (Al Sweigart)
No Starch Press, San Francisco CA, 2021, pp. 132 ff.
"""
import random
import sys
import time
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import TypeAlias


def main():
    print("Hello, world!")


try:
    main()
except KeyboardInterrupt:
    sys.exit()
"""
Forset Fire Sim, by Al Sweigart (al@inventwithpython.com)
After "The Big Book of Small Python Projects" (Al Sweigart)
No Starch Press, San Francisco CA, 2021, pp. 132 ff.
"""
import sys

from colterm import term

WIDTH, HEIGHT = term.size()
TREE, FIRE, EMPTY = "AW "

INITIAL_TREE_DENSITY = 0.2
GROW_CHANCE = 0.01
FIRE_CHANCE = 0.01

PAUSE_LENGTH = 0.5

Location: TypeAlias = tuple[int, int]


@dataclass
class Forest:
    height: int = HEIGHT - 1
    width: int = WIDTH - 1
    trees: dict[Location, str] = field(default_factory=dict)


def make_forest() -> Forest:
    forest = Forest()
    for x in range(forest.width):
        for y in range(forest.height):
            forest.trees[x, y] = TREE if random.random() * 100 < INITIAL_TREE_DENSITY else EMPTY
    return forest


def render_forest(forest: Forest):

    term.goto(0, 0)
    for y in range(forest.height):
        for x in range(forest.width):
            symbol = forest.trees[x, y]
            term.fg({TREE: "green", FIRE: "red", EMPTY: "black"}[symbol])
            print(symbol, end="", flush=True)

    term.goto(0, HEIGHT - 1)
    term.fg("white")
    print("*** Forest Fire Sim ***"
          f" Grow Chance: {GROW_CHANCE * 100:.1f}%, Fire Chance: {FIRE_CHANCE * 100:.1f}%"
          " (Press Ctrl+C to quit.)", end="", flush=True)


def neighborship(x: int, y: int) -> Generator[Location]:
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x + 1, y
    yield x + 1, y + 1
    yield x, y + 1
    yield x - 1, y + 1
    yield x - 1, y


def main():
    forest = make_forest()

    term.clear()

    while True:
        render_forest(forest)

        next_step = Forest()
        for x in range(forest.width):
            for y in range(forest.height):
                if (x, y) in next_step.trees:  # Do not visit a location twice.
                    continue

                symbol = forest.trees[x, y]
                if (symbol == EMPTY) and (random.random() <= GROW_CHANCE):
                    next_step.trees[x, y] = TREE
                elif (symbol == TREE) and (random.random() <= FIRE_CHANCE):
                    next_step.trees[x, y] = FIRE
                elif symbol == FIRE:
                    for x1, y1 in neighborship(x, y):
                        if forest.trees.get((x1, y1)) == TREE:  # Ignite this neighbor.
                            next_step.trees[x1, y1] = FIRE
                    next_step.trees[x, y] = EMPTY  # The tree is burnt down, now.
                else:
                    next_step.trees[x, y] = symbol

        forest = next_step

        time.sleep(PAUSE_LENGTH)


try:
    main()
except KeyboardInterrupt:
    sys.exit()
