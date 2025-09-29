import argparse
import sys
import time
from datetime import datetime, timedelta

import sevseg
from colterm import term


def positive_integer(number: str) -> int:
    if not number.isdecimal():
        raise TypeError()
    n = int(number)
    if n <= 0:
        raise ValueError()
    return n


def get_seconds_left(prog: str) -> int:
    parser = argparse.ArgumentParser(
        prog=prog, description='Count down from a certain initial number of seconds')
    parser.add_argument(
        'seconds_left', metavar='NUM_SECONDS_LEFT', nargs='?',
        help='the initial number of seconds left', type=positive_integer, default=30)
    args = parser.parse_args()
    return args.seconds_left


def print_time_left(current: datetime) -> None:
    hour, minute, second = current.hour, current.minute, current.second
    term.clear()
    term.fg('red')
    term.hide_cursor()
    print(sevseg.hms_time_display(hour, minute, second))
    term.fg('yellow')
    print('Press Ctrl+C to quit before zero.')
    term.show_cursor()
    term.fg('reset')


def main(prog: str) -> None:
    current = datetime.min + timedelta(seconds=get_seconds_left(prog))

    while True:
        try:
            print_time_left(current)
            if current == datetime.min:
                break
            time.sleep(1)
            current -= timedelta(seconds=1)

        except KeyboardInterrupt:
            print('\nCountdown has been cancelled.\n')
            sys.exit()

    print('\n* * * *  B O O M  * * * *\n')


if __name__ == '__main__':
    main('countdown')
