from collections import deque
from typing import Self

from .symbols import ALPHABET_SIZE, to_signals, to_symbols, as_signal

NO_NOTCHES = ''


class Rotor:
    def __init__(self, wiring: list[int], notches: list[int], mark: int) -> None:
        self.left = deque(range(ALPHABET_SIZE))
        self.right = deque(wiring)
        self.notches = notches
        self.mark = mark
        self.rotate(mark)

    def rotate(self, offset: int = -1) -> Self:
        """
        Rotate the left and right signal arrays like enigam does mechanically.
        Rotation by 0 means: no change.
        Rotation by negative numbers means: the rotor steps "forward".
        Rotation by negative numbers means: the rotor steps "backards".
        The 'self.mark' tracks at which index the rotor's 'A' mark is currently located.
        """
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

    def __getitem__(self, signal: int) -> int:
        i = self.right[signal]
        return self.left.index(i)

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


def rotate(left: Rotor, middle: Rotor, right: Rotor) -> None:
    if middle.is_at_notch():
        middle.rotate()
        left.rotate()
    elif right.is_at_notch():
        middle.rotate()
    right.rotate()


# rotor wirings and turnovers for the Luftwaffe/Heer Enigma I and Kriegsmarine Enigma M3
m_rotor_stencils: dict[str, RotorStencil] = {
    'I': RotorStencil('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),  # Enigma I, Enigma M3
    'II': RotorStencil('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),  # Enigma I, Enigma M3
    'III': RotorStencil('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),  # Enigma I, Enigma M3
    'IV': RotorStencil('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),  # Enigma I, Enigma M3
    'V': RotorStencil('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),  # Enigma I, Enigma M3
    'VI': RotorStencil('JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'),  # Enigma M3
    'VII': RotorStencil('NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'),  # Enigma M3
    'VIII': RotorStencil('FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),  # Enigma M3
    'Beta': RotorStencil('LEYJVCNIXWPBQMDRTAKZGFUHOS', NO_NOTCHES),  # Enigma M4
    'Gamma': RotorStencil('FSOKANUERHMBTIYCWLQPZXVGJD', NO_NOTCHES),  # Enigma M4
}

# rotor wirings and turnovers for the Deutsche Reichsbahn Enigma (named "Rocket" at Bletchley Park)
rocket_rotor_stencils: dict[str, RotorStencil] = {
    'I': RotorStencil('JGDQOXUSCAMIFRVTPNEWKBLZYH', 'Q'),  # railway enigma "Rocket"
    'II': RotorStencil('NTZPSFBOKMWRCJDIVLAEYUXHGQ', 'E'),  # railway enigma "Rocket"
    'III': RotorStencil('JVIUBHTCDYAKEQZPOSGXNRMWFL', 'V'),  # railway enigma "Rocket"
    'UKW': RotorStencil('QYHOGNECVPUZTFDJAXWMKISRBL', NO_NOTCHES),  # railway enigma "Rocket"
}

tirpitz_rotor_stencils: dict[str, RotorStencil] = {
    'I': RotorStencil('GEKPBTAUMOCNILJDXZYFHWVQSR', 'EKQWZ'),  # Enigma T ("Tirpitz")
    'II': RotorStencil('UPHZLWEQMTDJXCAKSOIGVBYFNR', 'FLRWZ'),  # Enigma T ("Tirpitz")
    'III': RotorStencil('QUDLYRFEKONVZAXWHMGPJBSICT', 'EKQWZ'),  # Enigma T ("Tirpitz")
    'IV': RotorStencil('CIWTBKXNRESPFLYDAGVHQUOJZM', 'FLRWZ'),  # Enigma T ("Tirpitz")
    'V': RotorStencil('UAXGISNJBVERDYLFZWTPCKOHMQ', 'CFKRY'),  # Enigma T ("Tirpitz")
    'VI': RotorStencil('XFUZGALVHCNYSEWQTDMRBKPIOJ', 'EIMQX'),  # Enigma T ("Tirpitz")
    'VII': RotorStencil('BJVFTXPLNAYOZIKWGDQERUCHSM', 'CFKRY'),  # Enigma T ("Tirpitz")
    'VIII': RotorStencil('YMTPNZHWKODAJXELUQVGCBISFR', 'EIMQX'),  # Enigma T ("Tirpitz")
    'UKW': RotorStencil('GEKPBTAUMOCNILJDXZYFHWVQSR', NO_NOTCHES),  # Enigma T ("Tirpitz")
}
