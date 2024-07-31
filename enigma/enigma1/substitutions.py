from abc import ABC
from dataclasses import dataclass, field

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_SIZE = len(SYMBOLS)


def as_signal(symbol: str) -> int:
    return SYMBOLS.find(symbol)


def as_symbol(signal: int) -> str:
    return SYMBOLS[signal]


class SubstitutionDevice(ABC):
    left: str = SYMBOLS
    right: str
    offset: int = 0

    def forward(self, signal: int) -> int:
        symbol = self.right[(signal + self.offset) % ALPHABET_SIZE]
        return (self.left.find(symbol) + self.offset) % ALPHABET_SIZE

    def backward(self, signal: int) -> int:
        symbol = self.left[(signal - self.offset) % ALPHABET_SIZE]
        return (self.right.find(symbol) - self.offset) % ALPHABET_SIZE


class Plugboard(SubstitutionDevice):
    def __init__(self, *substitutions: str) -> None:
        wiring = list(self.left)
        for left, right in substitutions:
            a = SYMBOLS.find(left)
            b = SYMBOLS.find(right)
            aux = wiring[a]
            wiring[a] = wiring[b]
            wiring[b] = aux
        self.right = ''.join(wiring)


class Rotor(SubstitutionDevice):
    def __init__(self, wiring: str, notch: str) -> None:
        self.right = wiring.strip().upper()
        self.notch = as_signal(notch)

    def advance(self, delta: int = 1) -> bool:
        self.offset = (self.offset + delta) % ALPHABET_SIZE
        carry = self.notch == self.offset
        return carry


class Reflector(SubstitutionDevice):
    def __init__(self, wiring: str) -> None:
        self.right = wiring.strip().upper()

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

    def set_key(self, key: str) -> None:
        for r, symbol in enumerate(key, 1):
            self.rotors[r].offset = as_signal(symbol)

    def _advance(self, delta: int = 1) -> None:
        carry = self.rotors[3].advance(delta)
        if carry:
            carry = self.rotors[2].advance(delta)
        if carry:
            self.rotors[1].advance(delta)

    def translate(self, symbol: str) -> str:
        signal = as_signal(symbol)
        reflector = -1

        self._advance()

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


cfg.set_key('AAZ')
for ch in 'YEKWYHONUTWLBUKSBVVKQTBSHOQRYJMUOIADDCGZRO':
    print(cfg.translate(ch), end='')
print()
print(''.join(as_symbol(o.offset) for o in cfg.rotors[1:-1]))
