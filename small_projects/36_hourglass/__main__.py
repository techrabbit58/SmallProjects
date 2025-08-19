from typing import TypeAlias

from colterm import term

Grain: TypeAlias = tuple[int, int]  # A grain of sand is defined by its 2D position: (x, y)


def setup() -> list[Grain]:
    term.fg("yellow")
    term.clear()

    term.goto(0, 0)
    print("Ctrl-C to quit.", end="", flush=True)

    return list()


def loop(all_sand: list[Grain]) -> None:
    while True:
        ...


def main() -> None:
    all_sand = setup()
    loop(all_sand)


try:
    main()
finally:
    term.fg("reset")
    term.clear()
