from abc import ABC
from collections import deque

from .rotors import RotorStencil, Rotor, NO_NOTCHES
from .symbols import SYMBOLS
from .validators import ensure_valid_symbols


class NonReciprocal(ABC):
    wheel: Rotor

    def encrypt(self, symbol: str) -> str:
        return _scramble(symbol, self.wheel.left, self.wheel.right)

    def decrypt(self, symbol: str) -> str:
        return _scramble(symbol, self.wheel.right, self.wheel.left)


class SelfReciprocal(ABC):
    wheel: Rotor

    def translate(self, symbol: str) -> str:
        return _scramble(symbol, self.wheel.left, self.wheel.right)


class Caesar(NonReciprocal):
    def __init__(self, key: str) -> None:
        key = SYMBOLS.index(ensure_valid_symbols(key, SYMBOLS)[0])
        self.wheel = RotorStencil(SYMBOLS[key:] + SYMBOLS[:key], NO_NOTCHES).create()


class MonoalphabeticCipher(NonReciprocal):
    def __init__(self, wiring: str) -> None:
        self.wheel = RotorStencil(ensure_valid_symbols(wiring, SYMBOLS), NO_NOTCHES).create()


class Rot13(SelfReciprocal):
    wheel = RotorStencil(SYMBOLS[13:] + SYMBOLS[:13], NO_NOTCHES).create()


class Atbash(SelfReciprocal):
    wheel = RotorStencil(''.join(reversed(SYMBOLS)), NO_NOTCHES).create()


def _scramble(symbol: str, a: deque[int], b: deque[int]) -> str:
    is_lower, symbol = symbol.islower(), symbol.upper()

    if symbol not in SYMBOLS:
        return symbol

    signal = SYMBOLS.find(symbol)
    index = a.index(signal)
    out = SYMBOLS[b[index]]

    return out.lower() if is_lower else out
