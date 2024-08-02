from collections import deque
from typing import Self

from .basics import ALPHABET_SIZE, to_signals, to_symbols, as_signal


class Rotor:
    def __init__(self, wiring: list[int], notches: list[int]) -> None:
        self.left = deque(range(ALPHABET_SIZE))
        self.right = deque(wiring)
        self.notches = notches

    def rotate(self, displacement: int) -> Self:
        self.left.rotate(displacement)
        self.right.rotate(displacement)
        return self

    def __str__(self) -> str:
        return f'lft={to_symbols(self.left)!r}, nch={to_symbols(self.notches)!r}\nrgt={to_symbols(self.right)!r}'


class RotorStencil:
    def __init__(self, wiring: str, notches: str) -> None:
        self.wiring = to_signals(wiring)
        self.notches = to_signals(notches)
        self.ring = '01'
        self.key = 'A'

    def set_key(self, symbol: str) -> Self:
        self.key = symbol
        return self

    def set_ring(self, position: str) -> Self:
        self.ring = position
        return self

    def create(self) -> Rotor:
        ring = int(self.ring) - 1
        offset = ring - as_signal(self.key)
        notches = [(n - ring) % ALPHABET_SIZE for n in self.notches]
        return Rotor(self.wiring, notches).rotate(offset)


rotors: dict[str, RotorStencil] = {
    'I': RotorStencil('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
    'II': RotorStencil('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
    'III': RotorStencil('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
    'IV': RotorStencil('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
    'V': RotorStencil('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
    'VI': RotorStencil('JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'),
    'VII': RotorStencil('NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'),
    'VIII': RotorStencil('FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),
}
