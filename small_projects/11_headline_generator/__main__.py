import argparse
import random
from collections.abc import Callable

from . import generators


def positive_integer(number: str) -> int:
    i = int(number)
    if i < 1:
        raise ValueError()
    return i


def parse_args(prog: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=prog, description='Generate a certain number of clickbait headlines.')
    parser.add_argument(
        '-n', '--num-headlines',
        dest='num_headlines', required=True, type=positive_integer,
        help='the number of headlines to generate')
    return parser.parse_args()


generate: list[Callable[[], str]] = [
    generators.are_millenials_killing,
    generators.what_you_dont_know,
    generators.big_companies_hate_her,
    generators.you_wont_believe,
    generators.dont_want_you_to_know,
    generators.gift_idea,
    generators.reasons_why,
    generators.job_automated_headline,
]


def main(prog: str) -> None:
    args = parse_args(prog)
    for _ in range(args.num_headlines):
        headline = random.choice(generate)()
        print(headline)


main('clickbait')
