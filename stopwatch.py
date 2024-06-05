import sys
import time
from datetime import datetime, timedelta

import sevseg
from colterm import term


def print_time(current: datetime) -> None:
    hour, minute, second = current.hour, current.minute, current.second
    term.clear()
    term.fg('white')
    print(' * * *  S T O P W A T C H  * * *')
    term.fg('cyan')
    term.hide_cursor()
    print(sevseg.hms_time_display(hour, minute, second))
    term.fg('yellow')
    print('\n      Press Ctrl+C to stop.')
    term.show_cursor()
    term.fg('reset')


def main() -> None:
    current = datetime.min
    key = None

    while True:
        print_time(current)

        try:
            time.sleep(1)

        except KeyboardInterrupt:
            print('\nBye!\n')
            sys.exit()

        current += timedelta(seconds=1)


if __name__ == '__main__':
    main()
