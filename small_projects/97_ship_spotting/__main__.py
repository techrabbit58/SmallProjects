import os
import random
import re
import sys

OCEAN_SIZE_X = 5
OCEAN_SIZE_Y = 5
QUIT = -1, -1
WATER = "~"
SHIP = "S"
MISSED = "."
MAX_GUESSES = 10


def clear_screen() -> None:
    clear = "cls" if sys.platform == "win32" else "clear"
    os.system(clear)


def read_location() -> tuple[int, int]:
    while True:
        line = input("Enter location (x, y) or (Q)uit: ")
        if line.strip().lower() == "q":
            return QUIT
        else:
            answer = re.fullmatch(r"^ *(\d+), *(\d+) *$", line)
            try:
                x, y = map(int, answer.groups())
                break
            except AttributeError:
                print("Invalid location. You must enter a pair of positive integer numbers. Try again.")
    return x - 1, y - 1


def water_to_string(water: list[list[str]]) -> str:
    return "\n".join(" ".join(w for w in wave) for wave in water)


def main() -> None:
    water = [[WATER] * OCEAN_SIZE_X for _ in range(OCEAN_SIZE_Y)]
    ship = random.randrange(OCEAN_SIZE_X), random.randrange(OCEAN_SIZE_Y)

    is_cancelled = is_won = False
    num_guesses = MAX_GUESSES

    while True:
        clear_screen()
        print("Guess where the ship hides.")
        print(f"You have {num_guesses} guesses left.")
        print(water_to_string(water))
        location = read_location()
        if location == QUIT:
            is_cancelled = True
            break
        x, y = location
        if location == ship:
            is_won = True
            break
        else:
            if 0 <= x < OCEAN_SIZE_X and 0 <= y < OCEAN_SIZE_Y:
                water[y][x] = MISSED
                num_guesses -= 1
                if num_guesses <= 0:
                    break

    if is_cancelled:
        print("The game has been cancelled.")
        return

    water[ship[1]][ship[0]] = SHIP
    guesses = MAX_GUESSES - num_guesses + 1

    clear_screen()
    if is_won:
        print(f"\nYou won after {guesses} guesses!")
    else:
        print("\nYou lost!")
    print(water_to_string(water))


if __name__ == '__main__':
    main()
