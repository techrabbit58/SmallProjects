from abc import ABC
from dataclasses import dataclass, field

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def as_signal(symbol: str) -> int:
    return SYMBOLS.find(symbol)


def as_symbol(signal: int) -> str:
    return SYMBOLS[signal]


class SubstitutionDevice(ABC):
    left: str
    right: str

    def forward(self, signal: int) -> int:
        symbol = self.right[signal]
        return self.left.find(symbol)

    def backward(self, signal: int) -> int:
        symbol = self.left[signal]
        return self.right.find(symbol)


class Plugboard(SubstitutionDevice):
    def __init__(self, *substitutions: str) -> None:
        self.left = SYMBOLS
        wiring = list(self.left)
        for left, right in substitutions:
            a = SYMBOLS.find(left)
            b = SYMBOLS.find(right)
            wiring[a], wiring[b] = wiring[b], wiring[a]
        self.right = ''.join(wiring)


class Rotor(SubstitutionDevice):
    def __init__(self, wiring: str, notch: str) -> None:
        self.right = wiring.strip().upper()
        self.left = SYMBOLS
        self.notch = notch


class Reflector(SubstitutionDevice):
    def __init__(self, wiring: str) -> None:
        self.right = wiring.strip().upper()
        self.left = SYMBOLS

    def reflect(self, signal: int) -> int:
        return self.forward(signal)


ROTOR_I = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'
ROTOR_II = 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'
ROTOR_III = 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'
ROTOR_IV = 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'
ROTOR_V = 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'

REFLECTOR_A = 'EJMZALYXVBWFCRQUONTSPIKHGD'
REFLECTOR_B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
REFLECTOR_C = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'


@dataclass
class EnigmaConfig:
    jumpers: list[str] = field(repr=False, kw_only=True)
    right_rotor: tuple[str, str] = field(repr=False, kw_only=True)
    middle_rotor: tuple[str, str] = field(repr=False, kw_only=True)
    left_rotor: tuple[str, str] = field(repr=False, kw_only=True)
    reflector: str = field(repr=False)
    substitution_devices: list[SubstitutionDevice] = field(init=False)

    def __post_init__(self) -> None:
        self.rotors = [
            Plugboard(*self.jumpers),
            Rotor(*self.right_rotor),
            Rotor(*self.middle_rotor),
            Rotor(*self.left_rotor),
            Reflector(self.reflector)
        ]

    def _rotate(self, offset: int = 1) -> None:
        ...

    def translate(self, symbol: str) -> str:
        signal = as_signal(symbol)
        reflector = -1

        self._rotate()

        for subst in self.rotors[:reflector]:
            signal = subst.forward(signal)

        signal = self.rotors[reflector].forward(signal)

        for subst in reversed(self.rotors[:reflector]):
            signal = subst.backward(signal)

        return as_symbol(signal)


cfg = EnigmaConfig(
    jumpers=['AR', 'GK', 'OX'],
    right_rotor=ROTOR_III,
    middle_rotor=ROTOR_II,
    left_rotor=ROTOR_I,
    reflector=REFLECTOR_A
)


for ch in 'AAA':
    print(cfg.translate(ch))
