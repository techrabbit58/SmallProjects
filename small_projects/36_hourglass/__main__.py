import random
import time
from typing import TypeAlias

from colterm import term

from .config import WALL, SAND, BLANK, PAUSE, SCREEN_HEIGHT, SCREEN_WIDTH, WIDE_FALL_CHANCE
from .hourglass import HOURGLASS
from .sand import INITIAL_SAND

Grain: TypeAlias = tuple[int, int]  # A grain of sand is defined by its 2D position: (x, y)


def setup() -> None:
    term.clear()
    term.hide_cursor()

    term.goto(0, 0)
    term.fg("red")
    print("Ctrl-C to quit.", end="", flush=True)

    term.fg("cyan")
    for x, y in HOURGLASS:
        term.goto(x, y)
        print(WALL, end="", flush=True)


def draw_grain(x: int, y: int) -> None:
    term.goto(x, y)
    print(SAND, end="", flush=True)


def remove_grain(x: int, y: int) -> None:
    term.goto(x, y)
    print(BLANK, end="", flush=True)


def draw_initial_sand(all_sand: list[Grain]):
    term.fg(random.choice("yellow yellow purple yellow".split()))
    for x, y in all_sand:
        draw_grain(x, y)


def remove_sand(all_sand):
    for x, y in all_sand:
        remove_grain(x, y)


def simulate_hourglass(all_sand: list[Grain]):

    def can_fall_down(next_position: Grain) -> bool:
        no_sand_below = next_position not in all_sand
        no_wall_below = next_position not in HOURGLASS
        return all((no_sand_below, no_wall_below))

    def can_fall_left(next_position: Grain) -> bool:
        no_sand_below_left = next_position not in all_sand
        no_wall_below_left = next_position not in HOURGLASS
        left = x - 1, y
        no_wall_left = left not in HOURGLASS
        not_on_left_edge = x > 0
        return all((no_sand_below_left, no_wall_below_left, no_wall_left, not_on_left_edge))

    def can_fall_right(next_position: Grain) -> bool:
        no_sand_below_right = next_position not in all_sand
        no_wall_below_right = next_position not in HOURGLASS
        right = x + 1, y
        no_wall_right = right not in HOURGLASS
        not_on_right_edge = x < SCREEN_WIDTH - 1
        return all((no_sand_below_right, no_wall_below_right, no_wall_right, not_on_right_edge))

    def is_far_fall_chance() -> bool:
        return random.randrange(100) <= WIDE_FALL_CHANCE

    def can_fall_two_left(one: Grain, two: Grain) -> bool:
        no_sand_below_two_left = two not in all_sand
        no_wall_below_two_left = two not in HOURGLASS
        not_on_second_to_left_edge = x > 1
        return all((
            can_fall_left(one),
            no_sand_below_two_left,
            no_wall_below_two_left,
            not_on_second_to_left_edge))

    def can_fall_two_right(one: Grain, two: Grain) -> bool:
        no_sand_below_two_right = two not in all_sand
        no_wall_below_two_right = two not in HOURGLASS
        not_on_second_to_right_edge = x < SCREEN_WIDTH - 2
        return all((
            can_fall_right(one),
            no_sand_below_two_right,
            no_wall_below_two_right,
            not_on_second_to_right_edge))

    while True:
        random.shuffle(all_sand)

        sand_moved = False

        for i, (x, y) in enumerate(all_sand):
            if y == SCREEN_HEIGHT - 1:
                continue

            term.fg("yellow")
            just_below = x, y + 1
            if can_fall_down(just_below):
                remove_grain(x, y)
                draw_grain(*just_below)
                all_sand[i] = just_below
                sand_moved = True
            else:
                below_left = x - 1, y + 1
                below_right = x + 1, y + 1

                falling_direction = None

                match can_fall_left(below_left) * 10 + can_fall_right(below_right):
                    case 1:
                        falling_direction = 1
                    case 10:
                        falling_direction = -1
                    case 11:
                        falling_direction = random.choice((-1, 1))

                if is_far_fall_chance():
                    two_left = x - 2, y + 1
                    two_right = x + 2, y + 1
                    term.fg("purple")

                    match can_fall_two_left(below_left, two_left) * 10 + can_fall_two_right(below_right, two_right):
                        case 1:
                            falling_direction = 2
                        case 10:
                            falling_direction = -2
                        case 11:
                            falling_direction = random.choice((-2, 2))

                if falling_direction is not None:
                    new_grain = x + falling_direction, y + 1
                    remove_grain(x, y)
                    draw_grain(*new_grain)
                    all_sand[i] = new_grain
                    sand_moved = True

        time.sleep(PAUSE)

        if not sand_moved:
            break


def loop() -> None:
    while True:
        all_sand = list(INITIAL_SAND)
        draw_initial_sand(all_sand)
        simulate_hourglass(all_sand)
        remove_sand(all_sand)
        time.sleep(PAUSE)


def main() -> None:
    setup()
    loop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        term.fg("reset")
        term.clear()
        term.show_cursor()
