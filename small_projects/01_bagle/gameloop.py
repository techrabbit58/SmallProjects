import random
from collections import Counter

import pyfiglet

LIMITS = (100, 999)
MAX_GUESSES = 10

LOOSE = '\033[31;1m'
WIN = '\033[32;1m'
INTRO = '\033[36;1m'
DEFAULT = '\033[0m'


def _is_acceptable(guess: str) -> bool:
    smallest, biggest = LIMITS
    return guess.isnumeric() and smallest <= int(guess) <= biggest


def _show_help() -> None:
    print(f"""Guess a secret number between {LIMITS[0]} and {LIMITS[1]}.
The game will confirm if a digit is in the secret number with 'Fair'.
'Hit' means it is also in the correct position. The game does not reveal which
digit is part of the secret number or in the correct position. If the guess 
is completely wrong, the game will tell you 'Nil'.

Enter a number from the inclusive range {LIMITS} to make your next guess.
Enter 'n' to stop the current game and start a new one.
Enter 'g' to summarize your guesses on screen. 
Enter 'q' if you want to quit the game.
Enter '?' to show this help text.
    """)


def _generate_secret_number() -> str:
    smallest, biggest = LIMITS
    return str(random.randint(smallest, biggest))


def _judge(guess: str, secret: str) -> str:
    result = []
    remaining = []
    counts = Counter(secret)
    for pos, digit in enumerate(guess):
        if secret[pos] == digit:
            result.append('Hit')
            counts[digit] -= 1
        else:
            remaining.append(digit)
    for digit in remaining:
        if counts[digit] > 0:
            counts[digit] -= 1
            result.append('Fair')
    if result.count('Hit') == 3:
        return 'Full Match'
    return 'Nil' if len(result) == 0 else ', '.join(result)


def _show_intro() -> None:
    print(f'\n{INTRO}{pyfiglet.Figlet("standard").renderText("Nil Fair Hit").normalize_surrounding_newlines()}{DEFAULT}')
    _show_help()


def _show_outcome(secret: str, conviction: str, font: str, color: str = '\033[0m') -> None:
    print(f'The secret number was {secret}.')
    print(f'{color}{pyfiglet.Figlet(font).renderText(conviction).normalize_surrounding_newlines()}{DEFAULT}')


def _is_command(cmd: str, guess: str) -> bool:
    return guess.lower() == cmd


def _show_history(history: list[tuple[int, str, str]]) -> None:
    if len(history) == 0:
        print('Make your first guess.')
    else:
        print('\nYour guesses:\n')
        for n, g, o in history:
            print(f'{n:3d}: {g} -> {o}')


def gameloop():

    def reset() -> tuple[int, list, str]:
        return 1, [], _generate_secret_number()

    _show_intro()
    num_guesses, history, secret = reset()
    while True:
        if num_guesses > MAX_GUESSES:
            _show_outcome(secret, 'You loose!', 'sblood', LOOSE)
            num_guesses, history, secret = reset()
        guess = input(f'({MAX_GUESSES - num_guesses + 1} guesses left) ').lower().strip()
        if len(guess) == 0:
            continue
        elif _is_command('q', guess):
            break
        elif _is_command('?', guess):
            print()
            _show_help()
        elif _is_command('n', guess):
            _show_outcome(secret, 'new game', 'soft', INTRO)
            num_guesses, history, secret = reset()
        elif _is_command('g', guess):
            _show_history(history)
        elif not _is_acceptable(guess):
            print(f'You must choose a positive number from the including range {LIMITS}.')
            continue
        else:
            result = _judge(secret, guess)
            print(f'Your result with guess #{num_guesses}: {result}')
            if result == 'Full Match':
                _show_outcome(secret, 'You win!', 'basic', WIN)
                num_guesses, history, secret = reset()
            else:
                history.append((MAX_GUESSES - num_guesses + 1, guess, result))
                num_guesses += 1
