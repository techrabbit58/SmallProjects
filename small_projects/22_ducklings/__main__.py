import random
import shutil
import sys
import time

from .duckling import Duckling

DUCKLING_WIDTH = 5
PAUSE = .2  # seconds
DENSITY = .1  # percent


def main():
    screen_width = shutil.get_terminal_size()[0] - 1
    lanes: list[Duckling | None] = [None] * (screen_width // DUCKLING_WIDTH)

    while True:
        for lane, duckling in enumerate(lanes):
            if duckling is None and random.random() <= DENSITY:
                lanes[lane] = Duckling()

            duckling = lanes[lane]

            if duckling is None:
                print(' ' * DUCKLING_WIDTH, end='')
                continue

            print(duckling.next_part(), end='')
            if duckling.next_part is None:
                lanes[lane] = None

        print()
        time.sleep(PAUSE)


try:
    main()
except KeyboardInterrupt:
    sys.exit()
