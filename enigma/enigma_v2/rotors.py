from collections import deque
from typing import Self

from .basics import ALPHABET_SIZE, to_signals, to_symbols, as_signal


class Rotor:
    def __init__(self, wiring: list[int], notches: list[int], mark: int) -> None:
        self.left = deque(range(ALPHABET_SIZE))
        self.right = deque(wiring)
        self.notches = notches
        self.mark = mark
        self.rotate(mark)

    def rotate(self, offset: int = -1) -> Self:
        self.left.rotate(offset)
        self.right.rotate(offset)
        self.mark = (self.mark - offset) % ALPHABET_SIZE
        return self

    def set_key(self, key: str) -> Self:
        signal = as_signal(key)
        self.rotate(self.mark - signal)
        return self

    def is_at_notch(self) -> bool:
        return self.left[0] in self.notches

    def __str__(self) -> str:
        return f'{to_symbols(self.left)!r}\n{to_symbols(self.right)!r}\n{to_symbols(self.notches)!r}'


class RotorStencil:
    def __init__(self, wiring: str, notches: str) -> None:
        self.wiring = to_signals(wiring)
        self.notches = to_signals(notches)
        self.ring = 0

    def set_ring(self, position: str) -> Self:
        """Adjust the ring position of the stencil before creating the next new rotor instance."""
        self.ring = int(position) - 1
        return self

    def create(self) -> Rotor:
        offset = self.ring
        new_notches = [(n - self.ring) % ALPHABET_SIZE for n in self.notches]
        new_rotor = Rotor(self.wiring, new_notches, offset)
        self.ring = 0  # reset factory to ring default after each new rotor instance created
        return new_rotor


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
