from collections import deque

from .rotors import RotorStencil, Rotor, NO_NOTCHES
from .symbols import SYMBOLS
from .validators import ensure_valid_symbols


class Caesar:
    wheel: Rotor

    def __init__(self, key: str) -> None:
        key = SYMBOLS.index(ensure_valid_symbols(key, SYMBOLS)[0])
        self.wheel = RotorStencil(SYMBOLS[key:] + SYMBOLS[:key], NO_NOTCHES).create()

    def encrypt(self, symbol: str) -> str:
        return _scramble(symbol, self.wheel.left, self.wheel.right)

    def decrypt(self, symbol: str) -> str:
        return _scramble(symbol, self.wheel.right, self.wheel.left)


class Rot13:
    wheel = RotorStencil(SYMBOLS[13:] + SYMBOLS[:13], NO_NOTCHES).create()

    def translate(self, symbol: str) -> str:
        return _scramble(symbol, self.wheel.left, self.wheel.right)


class Atbash:
    wheel = RotorStencil(''.join(reversed(SYMBOLS)), NO_NOTCHES).create()

    def translate(self, symbol: str) -> str:
        return _scramble(symbol, self.wheel.left, self.wheel.right)


def _scramble(symbol: str, a: deque[int], b: deque[int]) -> str:
    is_lower, symbol = symbol.islower(), symbol.upper()

    if symbol not in SYMBOLS:
        return symbol

    signal = SYMBOLS.find(symbol)
    index = a.index(signal)
    out = SYMBOLS[b[index]]

    return out.lower() if is_lower else out
