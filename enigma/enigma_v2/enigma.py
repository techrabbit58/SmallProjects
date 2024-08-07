from typing import Self

from .plugboard import Plugboard
from .reflectors import reflectors, Reflector
from .rotors import m3_rotor_stencils, Rotor
from .symbols import SYMBOLS, as_signal, as_symbol
from .validators import (
    ensure_valid_mil_reflector, ensure_valid_ring_setting,
    ensure_valid_jumpers, ensure_valid_m3_rotor
)


class EnigmaM3:
    reflector: Reflector
    wheels: list[Rotor]
    plugboard: Plugboard

    def __init__(self, reflector: str, rotor_pack: str, rings: str) -> None:
        self.reflector = reflectors[ensure_valid_mil_reflector(reflector)]
        ring_list = rings.split()
        self.wheels = [
            m3_rotor_stencils[ensure_valid_m3_rotor(r)].set_ring(ensure_valid_ring_setting(ring_list[i])).create()
            for i, r in enumerate(rotor_pack.split())
        ]
        self.plugboard = Plugboard()

    def set_jumpers(self, jumpers: str) -> Self:
        self.plugboard = Plugboard(ensure_valid_jumpers(jumpers))
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
        if symbol not in SYMBOLS:
            return symbol
        else:
            self._rotate()
            signal = as_signal(symbol)
            signal = self.plugboard[signal]
            for r in reversed(self.wheels):
                i = r.right[signal]
                signal = r.left.index(i)
            signal = self.reflector[signal]
            for r in self.wheels:
                i = r.left[signal]
                signal = r.right.index(i)
            signal = self.plugboard[signal]
            return as_symbol(signal)
