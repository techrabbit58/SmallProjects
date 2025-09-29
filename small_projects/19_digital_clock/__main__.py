import time
from datetime import datetime

import sevseg
from colterm import term


def print_time(current: datetime) -> None:
    hour, minute, second = current.hour, current.minute, current.second
    term.clear()
    term.fg('green')
    term.hide_cursor()
    print()
    print(sevseg.hms_time_display(hour, minute, second))
    term.fg('yellow')
    print('\n      Press Ctrl+C to quit.')
    term.show_cursor()
    term.fg('reset')


def main() -> None:
    while True:
        try:
            print_time(datetime.now())
            time.sleep(1)

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
