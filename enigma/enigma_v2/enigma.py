from typing import Self, Protocol

from .plugboard import Plugboard
from .reflectors import reflectors, Reflector
from .rotors import m_rotor_stencils, Rotor, rocket_rotor_stencils
from .symbols import SYMBOLS, as_signal, as_symbol
from .validators import (
    ensure_valid_mil_reflector, ensure_valid_ring_setting, ensure_valid_key,
    ensure_valid_jumpers, ensure_valid_m3_rotor, ensure_valid_a27_rotor
)


class Enigma(Protocol):

    def set_key(self, key: str) -> Self:
        ...

    def convert(self, symbol: str) -> str:
        ...


class EnigmaM3:
    reflector: Reflector
    wheels: list[Rotor]
    plugboard: Plugboard

    def __init__(self, reflector: str, rotor_pack: str, rings: str) -> None:
        self.reflector = reflectors[ensure_valid_mil_reflector(reflector)]
        ring_list = rings.split()
        self.wheels = [
            m_rotor_stencils[ensure_valid_m3_rotor(r)].set_ring(ensure_valid_ring_setting(ring_list[i])).create()
            for i, r in enumerate(rotor_pack.split())
        ]
        self.plugboard = Plugboard()

    def set_jumpers(self, jumpers: str) -> Self:
        self.plugboard = Plugboard(ensure_valid_jumpers(jumpers))
        return self

    def set_key(self, key: str) -> Self:
        for i, symbol in enumerate(ensure_valid_key(key)):
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


class EnigmaRocket:
    """The Enigma variant used by the german railway, as reverse engineered by Bletchley Park"""
    def __init__(self, rotor_pack: str, rings: str) -> None:
        self.entry = 'QWERTZUIOASDFGHJKPYXCVBNML'
        ring_list = rings.split()
        self.reflector = rocket_rotor_stencils['UKW'].set_ring(ensure_valid_ring_setting(ring_list[0])).create()
        self.wheels = [
            rocket_rotor_stencils[ensure_valid_a27_rotor(r)].set_ring(ensure_valid_ring_setting(ring_list[i])).create()
            for i, r in enumerate(rotor_pack.split(), 1)
        ]

    def set_key(self, key: str) -> Self:
        ensure_valid_key(key)
        self.reflector.set_key(key[0])
        for i, symbol in enumerate(key[1:]):
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
            signal = self.entry.find(symbol)
            for r in reversed(self.wheels):
                i = r.right[signal]
                signal = r.left.index(i)
            i = self.reflector.right[signal]
            signal = self.reflector.left.index(i)
            for r in self.wheels:
                i = r.left[signal]
                signal = r.right.index(i)
            return self.entry[signal]
