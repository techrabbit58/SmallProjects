from argparse import ArgumentParser
from collections.abc import Callable
from string import Template


def positive_int(*, limit: int) -> Callable[[str], int]:

    def parameter(arg: str) -> int:
        if not arg.isdecimal():
            raise TypeError()
        value = int(arg)
        if value < limit:
            raise ValueError()
        return value

    return parameter


def new_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="numeralsys",
        description="Numeral Systems Counters (Credit: Al Sweigart, al@inventwithpython.com)",
    )
    parser.add_argument(
        "-s", "--start", metavar="NUM", default=0, type=positive_int(limit=0),
        help="specifies the starting number (default=0)",
    )
    parser.add_argument(
        "-n", "--count", metavar="NUM", default=10, type=positive_int(limit=1),
        help="specifies how many numbers to display (default=10)",
    )
    return parser


def main() -> None:
    parser = new_argument_parser()
    args = parser.parse_args()
    line = Template("DEC: $dec    HEX: $hex    BIN: $bin")

    start = args.start
    end = start + args.count

    for number in range(start, end):
        print(line.substitute(dec=number, hex=hex(number)[2:], bin=bin(number)[2:]))


main()
