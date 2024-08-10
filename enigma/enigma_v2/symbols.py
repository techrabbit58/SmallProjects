from collections.abc import Iterable

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_SIZE = len(SYMBOLS)
NUMERIC_RING_SETTINGS = {f'{i:02d}' for i, _ in enumerate(SYMBOLS, 1)}


def as_signal(symbol: str) -> int:
    """Translate a single symbol to its ordinal number (here called 'signal')."""
    return SYMBOLS.find(symbol)


def as_symbol(signal: int) -> str:
    """Translate an ordinal number to the corresponding symbol."""
    return SYMBOLS[signal]


def to_signals(wiring: str) -> list[int]:
    """Translate a whole string of symbols to a list of the corresponding ordinals."""
    return [as_signal(s) for s in wiring]


def to_symbols(signals: Iterable[int]) -> str:
    """Translate a whole list of ordinals back to a string of the corresponding symbols."""
    return ''.join(as_symbol(n) for n in signals)


def number_string_to_symbols(numbers: str) -> str:
    return ''.join(as_symbol(int(digits) - 1) for digits in numbers.split())


def symbols_to_number_string(symbols: str) -> str:
    return ' '.join(f'{as_signal(symbol) + 1:02d}' for symbol in symbols)
