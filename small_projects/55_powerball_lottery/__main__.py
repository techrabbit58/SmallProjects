import argparse
import random
from argparse import ArgumentTypeError
from typing import Callable


def including_int_range(info: str, lo: int, hi: int) -> Callable[[str], int]:
    def validator(s: str) -> int:
        n = int(s)
        if not lo <= n <= hi:
            raise ArgumentTypeError(f'{info} must be in the including range {lo} to {hi}')
        return n

    return validator


def get_args(prog: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=prog, description='A simulation of the american "Powerball Lottery".')

    parser.add_argument(
        '-n', metavar='NUMBER', dest='numbers',
        type=including_int_range('lucky numbers', 1, 69), nargs=5, required=True,
        help='a list of exactly five integer numbers in the including range 1 to 69')

    parser.add_argument(
        '-p', metavar='POWERBALL', dest='powerball',
        type=including_int_range('powerball numbers', 1, 26), required=True,
        help='a single integer number in the including range 1 to 26')

    parser.add_argument(
        '-t', metavar='TIMES', dest='times', default=1560,
        type=including_int_range('iterations', 1, 1_000_000),
        help='How many times do you want to play? (1 to 1 million, default 1560)')

    parser.add_argument(
        '--powerplay', action='store_true',
        help='if set, pay an additional dollar per play to upgrade your prize by 2, 3, 4, 5, or 10 times')

    return parser.parse_args()


def get_prize(number_matches: int, powerball_match: bool, powerplay_factor: int = 1) -> int:
    prize = 0
    if number_matches < 2 and powerball_match:
        prize = 4 * powerplay_factor
    elif number_matches + powerball_match == 3:
        prize = 7 * powerplay_factor
    elif number_matches + powerball_match == 4:
        prize = 100 * powerplay_factor
    elif number_matches == 4 and powerball_match:
        prize = 50_000 * powerplay_factor
    elif number_matches == 5 and not powerball_match:
        prize = 1_000_000 if powerplay_factor == 1 else 2_000_000
    return prize


def main(prog: str) -> None:
    args = get_args(prog)
    numbers = set(args.numbers)
    powerball = args.powerball
    num_plays = args.times

    lottery_drum = list(range(1, 70))

    balance = 0
    for i in range(num_plays):
        balance -= 3 if args.powerplay else 2
        random.shuffle(lottery_drum)
        winning_numbers = set(lottery_drum[0:5])
        winning_powerball = random.randint(1, 26)
        powerplay_factor = random.choice([2, 3, 4, 5, 10])

        print(f'your numbers:    {", ".join(str(n).rjust(2) for n in numbers):19} and {powerball:3}')
        print(f'winning numbers: {", ".join(str(n).rjust(2) for n in winning_numbers):19} and {winning_powerball:3}')
        print(f'powerplay:                {powerplay_factor}x {"" if args.powerplay else "(not applicable for you)"}')

        if set(numbers) == set(winning_numbers) and powerball == winning_powerball:
            print()
            print('Congratulations! You won the jackpot. Now you are a billionaire.')
            break
        else:
            prize = get_prize(
                len(winning_numbers.intersection(numbers)),
                winning_powerball == powerball,
                powerplay_factor if args.powerplay else 1)
            balance += prize
            print(
                f'Your {"profit" if balance > 0 else "loss"} after {i + 1} '
                f'game{"s" if i > 0 else ""} is ${abs(balance)}')
            if balance > 0:
                break


main('Powerball Lottery')
