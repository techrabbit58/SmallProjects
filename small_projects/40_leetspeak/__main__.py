import sys

import pyperclip

from . import leetspeak


def main(prog: str) -> None:
    print(prog, end=': ')
    text = leetspeak.encode(' '.join(sys.argv[1:]), .7)
    print(text)
    pyperclip.copy(text)


if __name__ == '__main__':
    main('L33+$p34|< is Leetspeak')
