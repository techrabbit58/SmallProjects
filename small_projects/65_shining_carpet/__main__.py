import random

TILES = [
    [
        r"_ \ \ \_/ __",
        r" \ \ \___/ _",
        r"\ \ \_____/ ",
        r"/ / / ___ \_",
        r"_/ / / _ \__",
        r"__/ / / \___",
    ],
    [
        r"___|",
        r"_|__",
    ],
    [
        r"((  )",
        r" ))( ",
    ],
    [
        r" / __ \ \__/",
        r"/ /  \ \____",
        r"\ \__/ / __ ",
        r" \____/ /  " + chr(92),
    ],
    [
        r"  \__ ",
        r"__/  " + chr(92),
        r"  \   ",
        r"__/   ",
        r"  \__/",
        r"  /   ",
    ],
    [
        r"/ ___ \ ^ ",
        r" /   \ VVV",
        r"|() ()|   ",
        r" \ ^ / ___",
        r"\ VVV /   ",
        r")|   |() (",
    ],
    [
        r".-----. |mmm| ",
        r"| o o | '---' ",
        r"\  ^  /.-----.",
        r" |mmm| | o o |",
        r" '---' \  ^  /",
    ],
]

CARPET_WIDTH = 72
CARPET_HEIGHT = 24


def main() -> None:
    choice = random.randrange(len(TILES))
    tile = TILES[choice]
    height = int(1 + CARPET_HEIGHT / len(tile))
    width = int(1 + CARPET_WIDTH / len(tile[0]))
    lines = [(line * width)[:CARPET_WIDTH] for line in tile]

    for _ in range(height):
        for line in lines:
            print(line)


if __name__ == '__main__':
    main()
