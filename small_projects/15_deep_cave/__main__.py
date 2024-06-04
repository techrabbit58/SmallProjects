import random
import time
from types import SimpleNamespace

param = SimpleNamespace(width=72, pause=0.1, air=' ', stone='#')


def main() -> None:
    print('Press Ctrl+C to quit.')
    time.sleep(2)

    left_width, gap_width = 20, 10

    while True:
        right_width = param.width - left_width - gap_width
        print(param.stone * left_width, param.air * gap_width, param.stone * right_width, sep='')

        match random.randint(1, 6):
            case 1:
                if left_width > 1:
                    left_width -= 1
                if gap_width > 3:
                    gap_width -= 1
            case 2:
                if left_width + gap_width < param.width - 2:
                    left_width += 1
                    gap_width += 1
            case _:
                pass

        try:
            time.sleep(param.pause)
        except KeyboardInterrupt:
            break


main()
