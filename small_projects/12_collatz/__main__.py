import argparse
import textwrap


def positive_integer(number: str) -> int:
    if not number.isdecimal():
        raise TypeError()
    n = int(number)
    if n < 1:
        raise ValueError()
    return n


def get_number(prog: str) -> int:
    parser = argparse.ArgumentParser(
        prog=prog,
        description=textwrap.dedent("""
        Print the Collatz sequence when started with the given NUMBER.
        The NUMBER must be a positive integer.
        """.strip()))
    parser.add_argument(
        'number',
        metavar='NUMBER',
        help='The number to start the Collatz sequence.',
        type=positive_integer)
    return parser.parse_args().number


def main(prog: str) -> None:
    number = get_number(prog)

    while True:
        print(f'{number:10d}')

        if number == 1:
            break

        if number % 2 == 0:
            number //= 2
        else:
            number = number * 3 + 1


if __name__ == '__main__':
    main('collatz')
