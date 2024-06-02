import random
from argparse import ArgumentParser
from collections import Counter
from collections.abc import Callable


def int_in_inclusive_range(low: int, high: int) -> Callable[[str], int]:
    def int_range(arg: str) -> int:
        n = int(arg)
        if not (low <= n <= high):
            raise ValueError()
        return n

    return int_range


def main(prog: str):
    parser = ArgumentParser(
        prog=prog,
        description='Explore the birthday paradox statistically, with different group sizes.',
        epilog='The program conducts 100.000 experiments to find a good approximation.'
    )
    parser.add_argument(
        'groupsize',
        help='The number of people, for which to conduct the experiment (2 ... 100)',
        type=int_in_inclusive_range(low=2, high=100)
    )
    args = parser.parse_args()
    at_least_two_persons_same_birthday = 0
    for a in range(10):
        for _ in range(10_000):
            birthdays = Counter()
            for __ in range(args.groupsize):
                birthdays[random.randint(1, 365)] += 1
            count = birthdays.most_common(1)[0][1]
            if count > 1:
                at_least_two_persons_same_birthday += 1
        print(f'\033[0G{a + 1}0,000 experiments done ...', end='', flush=True)
    print()
    print(f'After 100,000 experiments regarding a group of {args.groupsize} persons:')
    print(f'{at_least_two_persons_same_birthday * 100. / 100_000:.2f}% of all experiments showed'
          f' at least two persons having birthday on the same day.')


main('birthdayparadox')
