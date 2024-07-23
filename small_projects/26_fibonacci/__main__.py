import shutil
import textwrap
import warnings
from collections.abc import Generator


def fibonacci_sequence(*, limit: int) -> Generator[int, None, None]:
    a, b = 0, 1
    while limit:
        yield a
        limit -= 1
        a, b = b, a + b


def get_screen_width():
    width, _ = shutil.get_terminal_size()
    return width


def get_next_response() -> int:
    k = -1

    while k < 0:
        print('How long a sequence do you wish to display next. Please enter a positive number.')
        print('Enter (Q)uit to stop.')
        response = None
        try:
            response = input('> ').strip().upper()
            if not response:
                k = -1
            elif response in {'Q', 'QUIT'}:
                k = 0
            else:
                k = int(response)
                if k <= 0:
                    raise ValueError
        except ValueError:
            print(f'Cannot accept your last response: "{response}".')
            k = -1
        except KeyboardInterrupt:
            print()
            k = 0

    return k


def warn_if_too_long(k: int) -> None:
    if k >= 10000:
        print('WARNING! Creating very large sequences can take pretty long.')
        print('You can abort using <Cntrl-C> if you get bored.')
        print('Press <Enter> to continue.')
        input()


def main(prog: str) -> None:
    print('=====', prog.upper(), '=====')

    while (k := get_next_response()) > 0:

        warn_if_too_long(k)

        print(f'{prog} up to {k} numbers:')
        numbers = []

        for n in fibonacci_sequence(limit=k):
            numbers.append(f'{n}')

        text = ', '.join(numbers), get_screen_width()
        for line in textwrap.wrap(*text):
            print(line)

    print('Bye!')


main('Fibonacci Sequence')
