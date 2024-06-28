import itertools
from collections.abc import Generator

_helix = [
    '          ##',
    '         #{}-{}#',
    '        #{}---{}#',
    '       #{}-----{}#',
    '      #{}------{}#',
    '     #{}------{}#',
    '     #{}-----{}#',
    '      #{}---{}#',
    '      #{}-{}#',
    '       ##',
    '      #{}-{}#',
    '      #{}---{}#',
    '     #{}-----{}#',
    '     #{}------{}#',
    '      #{}------{}#',
    '       #{}-----{}#',
    '        #{}---{}#',
    '         #{}-{}#',
]


def helix() -> Generator[str, None, None]:
    yield from itertools.cycle(_helix)
