import time

from . import visual
from . import arithmetic


def main() -> None:
    n = 9_999_999_990
    while True:
        print(visual.soroban_image(n))
        print(arithmetic.VALUES)
        n = (n + 1) % 10_000_000_000
        time.sleep(.1)


main()
