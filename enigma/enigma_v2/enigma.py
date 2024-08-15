from typing import Self, Protocol, TypeAlias

from .plugboard import Plugboard
from .reflectors import reflectors, Reflector
from .rotors import m_rotor_stencils, Rotor, rocket_rotor_stencils, rotate, tirpitz_rotor_stencils
from .symbols import SYMBOLS
from .validators import (
    ensure_valid_ring_setting, ensure_valid_symbols, ensure_rotors_are_unique,
    ensure_valid_jumpers, ensure_valid_m3_rotor, ensure_valid_rocket_rotor,
    ensure_valid_i_rotor, ensure_valid_m4_rotor, ensure_valid_m4_reflector,
    ensure_valid_t_rotor, ensure_valid_m3_reflector, ensure_valid_i_reflector
)


class ScramblingDevice(Protocol):

    def set_key(self, key: str) -> Self:
        ...

    def convert(self, symbol: str) -> str:
        ...


class EnigmaM3:
    entry: str = ensure_valid_symbols('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    reflector: Reflector
    wheels: list[Rotor]
    plugboard: Plugboard
    ensure_valid_rotor = ensure_valid_m3_rotor
    ensure_valid_reflector = ensure_valid_m3_reflector

    def __init__(self, reflector: str, rotor_pack: str, rings: str) -> None:
        self.reflector = reflectors[self.ensure_valid_reflector(reflector)]
        ring_list = rings.split()
        self.wheels = [
            m_rotor_stencils[
                self.ensure_valid_rotor(r)
            ].set_ring(ensure_valid_ring_setting(ring_list[i])).create()
            for i, r in enumerate(ensure_rotors_are_unique(rotor_pack.split()))
        ]
        self.plugboard = Plugboard()

    def set_jumpers(self, jumpers: str) -> Self:
        self.plugboard = Plugboard(ensure_valid_jumpers(jumpers))
        return self

    def set_key(self, key: str) -> Self:
        for i, symbol in enumerate(ensure_valid_symbols(key, self.entry)):
            self.wheels[i].set_key(symbol)
        return self

    def convert(self, symbol: str, *, first_rotor: int = 0) -> str:
        if symbol not in SYMBOLS:
            return symbol
        return _scramble(self, symbol, first_rotor)


class EnigmaI(EnigmaM3):
    ensure_valid_rotor = ensure_valid_i_rotor
    ensure_valid_reflector = ensure_valid_i_reflector


class EnigmaM4(EnigmaM3):
    ensure_valid_rotor = ensure_valid_m4_rotor
    ensure_valid_reflector = ensure_valid_m4_reflector

    def convert(self, symbol: str, *, first_rotor: int = 0) -> str:
        return super().convert(symbol, first_rotor=1)  # "greek" wheel does not rotate automatically


class EnigmaRocket:
    """The Enigma variant used by the german railway, as reverse engineered by Bletchley Park"""
    plugboard = Plugboard()  # no plugboard, emulated by this zero-conversion plugboard
    entry = ensure_valid_symbols('QWERTZUIOASDFGHJKPYXCVBNML')
    ensure_valid_rotor = ensure_valid_rocket_rotor
    stencils = rocket_rotor_stencils

    def __init__(self, rotor_pack: str, rings: str) -> None:
        ring_list = rings.split()
        self.reflector = self.stencils['UKW'].set_ring(ensure_valid_ring_setting(ring_list[0])).create()
        self.wheels = [
            self.stencils[
                self.ensure_valid_rotor(r)
            ].set_ring(ensure_valid_ring_setting(ring_list[i])).create()
            for i, r in enumerate(ensure_rotors_are_unique(rotor_pack.split()), 1)
        ]

    def set_key(self, key: str) -> Self:
        ensure_valid_symbols(key, self.entry)
        self.reflector.set_key(key[0])
        for i, symbol in enumerate(key[1:]):
            self.wheels[i].set_key(symbol)
        return self

    def convert(self, symbol: str, *, first_rotor: int = 0) -> str:
        if symbol not in SYMBOLS:
            return symbol
        return _scramble(self, symbol, first_rotor)


class EnigmaT(EnigmaRocket):
    entry = ensure_valid_symbols('KZROUQHYAIGBLWVSTDXFPNMCJE')
    ensure_valid_rotor = ensure_valid_t_rotor
    stencils = tirpitz_rotor_stencils

    def convert(self, symbol: str, *, first_rotor: int = 0) -> str:
        if symbol == '/':
            self.reflector.rotate()  # reflector: do manual rotation by one on each '/' (only for Enigma T)
            return symbol
        return super().convert(symbol)


Enigma: TypeAlias = EnigmaI | EnigmaM3 | EnigmaM4 | EnigmaRocket | EnigmaT


def _scramble(enigma: Enigma, symbol: str, first_rotor) -> str:
    rotate(*enigma.wheels[first_rotor:])
    signal = enigma.entry.find(symbol)
    signal = enigma.plugboard[signal]
    for r in reversed(enigma.wheels):
        i = r.right[signal]
        signal = r.left.index(i)
    signal = enigma.reflector[signal]
    for r in enigma.wheels:
        i = r.left[signal]
        signal = r.right.index(i)
    signal = enigma.plugboard[signal]
    return enigma.entry[signal]
