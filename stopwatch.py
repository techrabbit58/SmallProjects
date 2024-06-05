import time
from datetime import datetime, timedelta

import getkey

import sevseg
from colterm import term


def print_time(current: datetime, is_on_hold: bool) -> None:
    hour, minute, second = current.hour, current.minute, current.second
    term.clear()
    term.fg('white')
    print(' * * *  S T O P W A T C H  * * *')
    term.fg('cyan')
    term.hide_cursor()
    print(sevseg.hms_time_display(hour, minute, second))
    term.fg('yellow')
    print('           P A U S E D' if is_on_hold else '')
    print('   Press Ctrl+C or Q to stop.')
    print('Press spacebar to pause/continue.')
    term.show_cursor()
    term.fg('reset')


def main() -> None:
    current = datetime.min
    is_on_hold = False

    while True:
        print_time(current, is_on_hold)

        try:
            key = getkey.getkey(blocking=False)

            if key in {'q', 'Q'}:
                break
            if key == ' ':
                is_on_hold = not is_on_hold
                continue
            if key != '':
                continue

            time.sleep(1)

        except KeyboardInterrupt:
            break

        if not is_on_hold:
            current += timedelta(seconds=1)

    print('\nBye!\n')

if __name__ == '__main__':
    main()
