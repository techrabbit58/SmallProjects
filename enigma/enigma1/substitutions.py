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

    def forward(self, signal: int) -> int:
        symbol = self.right[signal]
        return self.left.find(symbol)

    def backward(self, signal: int) -> int:
        symbol = self.left[signal]
        return self.right.find(symbol)


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
        self.notch = notch

    def is_carry(self) -> bool:
        return self.notch == self.left[0]

    def advance(self) -> None:
        self.left = self.left[1:] + self.left[0]
        self.right = self.right[1:] + self.right[0]


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
    reflector: str = field(repr=False, kw_only=True)
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
        for r, symbol in enumerate(self.rotors[1:-1], 1):
            move = as_signal(key[-r])
            for n in range(move):
                self.rotors[r].advance()

    def _advance(self) -> None:
        if self.rotors[1].is_carry() and self.rotors[2].is_carry():
            self.rotors[1].advance()
            self.rotors[2].advance()
            self.rotors[3].advance()
        elif self.rotors[2].is_carry():  # double step anomaly of middle rotor
            self.rotors[1].advance()
            self.rotors[2].advance()
            self.rotors[3].advance()
        elif self.rotors[1].is_carry():
            self.rotors[1].advance()
            self.rotors[2].advance()
        else:
            self.rotors[1].advance()

    def translate(self, symbol: str) -> str:
        signal = as_signal(symbol)

        self._advance()

        signal = self.rotors[0].forward(signal)
        signal = self.rotors[1].forward(signal)
        signal = self.rotors[2].forward(signal)
        signal = self.rotors[3].forward(signal)

        signal = self.rotors[4].reflect(signal)

        signal = self.rotors[3].backward(signal)
        signal = self.rotors[2].backward(signal)
        signal = self.rotors[1].backward(signal)
        signal = self.rotors[0].backward(signal)

        return as_symbol(signal)


cfg = EnigmaConfig(
    jumpers=['AB', 'CD', 'EF'],
    reflector=REFLECTOR_B,
    left_rotor=ROTOR_IV,
    middle_rotor=ROTOR_II,
    right_rotor=ROTOR_I,
)


cfg.set_key('CAT')
for sym in 'TESTINGTESTINGTESTINGTESTING':
    print(cfg.translate(sym), end='')
print('\n', cfg.rotors[3].left[0], cfg.rotors[2].left[0], cfg.rotors[1].left[0], sep='')
