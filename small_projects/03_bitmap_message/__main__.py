import argparse
from itertools import cycle

from . import _bitmapworld


def main(prog: str):
    parser = argparse.ArgumentParser(
        prog=prog, description='Modify and display the "bitmapped" message.')
    parser.add_argument('message', help='the message to be displayed', nargs='+')
    args = parser.parse_args()
    characters = cycle(' '.join(args.message))
    bitmap = [list(row) for row in _bitmapworld.BITMAP]
    for row in bitmap:
        for i, ch in enumerate(row):
            if ch != ' ':
                row[i] = next(characters)
            else:
                next(characters)
        print(''.join(row))


main('bitmapmessage')
