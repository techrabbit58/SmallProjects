import argparse
from argparse import ArgumentTypeError


def valid_number(arg: str) -> int:
    number = int(arg)
    if number < 1 or number > 12:
        raise ArgumentTypeError('N must be a number between and including 1 and 12.')
    return number


def get_args(prog: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=prog, description="Print a multiplication table for the positive number N (1 <= N <= 12.)")
    parser.add_argument(
        'number', type=valid_number, metavar='N', help='a positive number (1 <= N <= 12)')
    parser.add_argument(
        '--mod', action='store_true', help='show remainders mod N instead of the plain products')
    return parser.parse_args()


def main(prog: str) -> None:
    args = get_args(prog)
    number = args.number
    numbers = [n for n in range(1, number + 1)]

    # print headline
    heading = ''.join(f'{n:4d}' for n in numbers)
    print(f'  |{heading}')

    # print separator
    sep = '--+' + '----' * len(numbers)
    print(sep)

    # print table
    for row in numbers:
        print(f'{row:2d}|', end='')
        for col in numbers:
            m = row * col
            print(f'{m % number if args.mod else m:4d}', end='')
        print()

    # finish
    print()


if __name__ == '__main__':
    main('Multiplication Table')
