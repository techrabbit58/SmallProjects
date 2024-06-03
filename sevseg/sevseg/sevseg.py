"""
The 7-segment display module encoding of symbols.
The symbols are composed of characters with this segment order:
       __ <- a
 f -> |__| <- b (The middle segment is 'g'.)
 e -> |__|. <- c (Right to the 'c' segment is the decimal point.)
       d

The resulting symbols are represented by a 2D array, five characters, wide
three characters high.
"""
from datetime import datetime

SYMBOLS = '0123456789- '
PARTS = [list(cp) for cp in ('     ', ' __  ', '   | ', '|  | ', '|__| ', '|__  ', ' __| ')]
CODES = [
    (1, 3, 4), (0, 2, 2), (1, 6, 5), (1, 6, 6), (0, 4, 2),
    (1, 5, 6), (0, 5, 4), (1, 2, 2), (1, 4, 4), (1, 4, 2),
    (0, 1, 0), (0, 0, 0)
]
COLON = '  ', '\u2022 ', '\u2022 '


def to_sevenseg(number: int | float, *, width: int = 0) -> str:
    return '\n'.join(get_sevenseg_matrix(number, width=width))


def hms_time_display(hour: int, minute: int, second: int) -> str:
    hh = get_sevenseg_matrix(hour % 24, width=2)
    mm = get_sevenseg_matrix(minute % 60, width=2)
    ss = get_sevenseg_matrix(second % 60, width=2)
    display = list(zip(hh, COLON, mm, COLON, ss))
    return '\n'.join(''.join(row) for row in display)


def get_sevenseg_matrix(number: int | float, *, width: int = 0) -> list[str]:
    matrix = [[] for _ in range(3)]

    for pos, symbol in enumerate(f'{number:0{width}}'):
        if symbol == '.':
            matrix[2][-1] = '.'
            continue
        cp = SYMBOLS.find(symbol)
        for row, i in enumerate(CODES[cp]):
            matrix[row] += PARTS[i]

    return [''.join(row) for row in matrix]
