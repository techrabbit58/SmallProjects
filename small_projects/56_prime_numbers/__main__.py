import math
import shutil
import time
from argparse import Namespace, ArgumentParser, ArgumentTypeError


def non_negative_integer(s: str) -> int:
    n = int(s)
    if n < 0:
        raise ArgumentTypeError('the number must be greater or equal zero')
    return n


def get_args(prog: str) -> Namespace:
    parser = ArgumentParser(
        prog=prog,
        description='Find all prime numbers greater or equal to a given positive integer number (0 <= number).')
    parser.add_argument(
        'number', type=non_negative_integer,
        help='the non-negative number from which to start generating primes')
    return parser.parse_args()


def is_prime(n: int) -> bool:
    if n < 2:
        return False

    if n == 2:
        return True

    for k in range(2, int(math.sqrt(n)) + 1):
        if n % k == 0:
            return False

    return True


def main(prog: str) -> None:
    args = get_args(prog)
    generate_primes(args.number)


def generate_primes(number: int) -> None:
    width, _ = shutil.get_terminal_size((80, 20))

    print('Press Ctrl-C to stop the prime generator.')
    print('...', end='', flush=True)  # the procedure starts thinking about the first prime to render ...

    current_column = 3
    while True:
        try:
            if is_prime(number):
                current_column = show_next_prime(current_column, number, width)
            number += 1
        except KeyboardInterrupt:
            print('\b\b\b\b\b     ')  # overwrite the last comma and elipsis with blanks
            break


def show_next_prime(current_column: int, number: int, width: int) -> int:
    text = f'{number}, ...'

    # write the rendered number, comma and ellipsis to the current line
    if current_column + len(text) < width:  # write number, comma, ellipsis if the number fits into the current line
        print(f'\b\b\b{text}', end='', flush=True)
        current_column -= 3
    else:  # if not, remove the ellipsis and start a new line before writing the new number
        print(f'\b\b\b\b    \n{text}', end='', flush=True)
        current_column = 0

    current_column += len(text)
    time.sleep(1./50.)  # an artificial delay

    return current_column


if __name__ == '__main__':
    main('Prime Numbers')
