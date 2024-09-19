import os.path
import random
import sys
import textwrap
import time
from pathlib import Path
import configparser


def intro() -> str:
    return textwrap.dedent("""
    MAGiC FORTUNE BALL
    based on content created by Al Sweigart 
    <al@inventwithpython.com>
    """)


def slow_print(text: str, delay: float = 1. / 16.) -> None:
    for ch in text:
        if ch in {'I'}:
            ch = 'i'
        print(ch, flush=True, end=' ')
        time.sleep(delay)
    print('\n')


def dramatic_pause(delay: float) -> None:
    slow_print('.' * random.randint(4, 12), delay)


def main() -> None:
    slow_print(intro())
    time.sleep(.5)

    slow_print('PLEASE ASK YOUR YES/NO QUESTION.')
    input('> ')

    cfg = configparser.ConfigParser()
    cfg.read(Path(os.path.dirname(sys.argv[0])) / 'magic_fortune_ball.ini')

    slow_print(random.choice(cfg.get('DEFAULT', 'replies').strip().split('\n')))
    dramatic_pause(0.7)

    slow_print('I HAVE AN ANSWER ...', .2)
    time.sleep(1)

    slow_print(random.choice(cfg.get('DEFAULT', 'answers').strip().split('\n')), .05)


main()
