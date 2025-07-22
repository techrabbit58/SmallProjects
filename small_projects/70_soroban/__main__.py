import time

from . import visual


def main() -> None:
    n = 9_999_999_990
    while True:
        print(visual.soroban_image(n))
        n = (n + 1) % 10_000_000_000
        time.sleep(.1)


main()
