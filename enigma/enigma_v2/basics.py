from collections.abc import Iterable

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_SIZE = len(SYMBOLS)


def as_signal(symbol: str) -> int:
    return SYMBOLS.find(symbol)


def as_symbol(signal: int) -> str:
    return SYMBOLS[signal]


def to_signals(wiring: str) -> list[int]:
    return [as_signal(s) for s in wiring]


def to_symbols(signals: Iterable[int]) -> str:
    return ''.join(as_symbol(n) for n in signals)