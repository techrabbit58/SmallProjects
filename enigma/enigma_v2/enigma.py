from collections.abc import Callable
from typing import Self

from . import plugboard
from .basics import SYMBOLS, as_signal, as_symbol
from .reflectors import reflectors, Reflector
from .rotors import rotor_stencils, Rotor


class EnigmaM3:
    reflector: Reflector
    wheels: list[Rotor]
    plugboard: Callable[[int], int]

    def __init__(self, reflector: str, rotor_pack: str, rings: str) -> None:
        self.reflector = reflectors[reflector]
        ring_list = rings.split()
        self.wheels = [rotor_stencils[r].set_ring(ring_list[i]).create() for i, r in enumerate(rotor_pack.split())]
        self.plugboard = plugboard.populate('')

    def set_jumpers(self, jumpers: str) -> Self:
        self.plugboard = plugboard.populate(jumpers)
        return self

    def set_key(self, key: str) -> Self:
        for i, symbol in enumerate(key):
            self.wheels[i].set_key(symbol)
        return self

    def _rotate(self) -> None:
        left, middle, right = self.wheels
        if middle.is_at_notch():
            middle.rotate()
            left.rotate()
        elif right.is_at_notch():
            middle.rotate()
        right.rotate()

    def convert(self, symbol: str) -> str:
        symbol = symbol.upper()
        if symbol not in SYMBOLS:
            return symbol
        else:
            self._rotate()
            signal = as_signal(symbol)
            signal = self.plugboard(signal)
            for r in reversed(self.wheels):
                i = r.right[signal]
                signal = r.left.index(i)
            signal = self.reflector[signal]
            for r in self.wheels:
                i = r.left[signal]
                signal = r.right.index(i)
            signal = self.plugboard(signal)
            return as_symbol(signal)
