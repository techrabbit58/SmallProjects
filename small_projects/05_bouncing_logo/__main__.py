import itertools
import random
import sys
import time

from colterm import term
from .bouncing_text import BouncingText


def main():
    try:
        term.clear()
        term.hide_cursor()

        color = itertools.cycle(['blue', 'green', 'red', 'cyan', 'yellow', 'magenta', 'white'])
        logos = []
        k = 5
        for _ in range(k):
            logos.append(BouncingText('DVD').fg(next(color)).location(
                random.randint(1, term.width() - 5), random.randint(1, term.height() - 1)
            ).direction(
                *random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])
            ))

        while True:
            for logo in logos:
                logo.move()
                time.sleep(1 / (k * (12. + k / 10.)))

    except KeyboardInterrupt:
        term.show_cursor()
        term.clear()
        sys.exit()


if __name__ == '__main__':
    main()
