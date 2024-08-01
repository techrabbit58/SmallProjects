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
    labels: str = SYMBOLS

    def forward(self, signal: int) -> int:
        symbol = self.right[signal]
        return self.left.find(symbol)

    def backward(self, signal: int) -> int:
        symbol = self.left[signal]
        return self.right.find(symbol)

    def rotate(self, _: int = None) -> None:
        raise NotImplementedError()

    def is_carry(self) -> bool:
        return False


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
    def __init__(self, wiring: str, notch: str, ring: str = 'A') -> None:
        self.right = wiring.strip().upper()
        self.labels = SYMBOLS
        self.notch = notch
        self._set_ring(SYMBOLS.find(ring) + 1)

    def _set_ring(self, ring: int) -> None:
        distance = (ALPHABET_SIZE - ring + 1) % ALPHABET_SIZE
        self.rotate(distance, with_label=False)
        adjusted_notch_position = SYMBOLS.find(self.notch) - ring + 1
        self.notch = SYMBOLS[adjusted_notch_position]

    def is_carry(self) -> bool:
        return self.notch == self.left[0]

    def rotate(self, n: int = 1, with_label: bool = True) -> None:
        self.left = self.left[n:] + self.left[:n]
        self.right = self.right[n:] + self.right[:n]
        if with_label:
            self.labels = self.labels[n:] + self.labels[:n]


class Reflector(SubstitutionDevice):
    def __init__(self, wiring: str) -> None:
        self.right = wiring.strip().upper()

    def backward(self, signal: int) -> int:
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
    rotors: list[tuple[str, str]] = field(repr=False, kw_only=True)
    reflector: str = field(repr=False, kw_only=True)
    mappings: list[SubstitutionDevice] = field(init=False)
    rings: str = field(repr=False, kw_only=True, default='AAA')

    def __post_init__(self) -> None:
        self.mappings = [
            Plugboard(*self.jumpers),
            Rotor(*self.rotors[-1], self.rings[-1]),
            Rotor(*self.rotors[-2], self.rings[-2]),
            Rotor(*self.rotors[-3], self.rings[-3]),
            Reflector(self.reflector)
        ]

    def set_key(self, key: str) -> None:
        for p, rotor in enumerate(self.mappings[1:-1], 1):
            rotor.rotate(as_signal(key[-p]))

    def _advance(self) -> None:
        if self.mappings[1].is_carry() and self.mappings[2].is_carry():
            self.mappings[1].rotate()
            self.mappings[2].rotate()
            self.mappings[3].rotate()
        elif self.mappings[2].is_carry():  # double step anomaly of middle rotor
            self.mappings[1].rotate()
            self.mappings[2].rotate()
            self.mappings[3].rotate()
        elif self.mappings[1].is_carry():
            self.mappings[1].rotate()
            self.mappings[2].rotate()
        else:
            self.mappings[1].rotate()

    def translate(self, symbol: str) -> str:
        if symbol.upper() not in SYMBOLS:
            return symbol

        was_lower = symbol.islower()

        signal = as_signal(symbol.upper())

        self._advance()

        signal = self.mappings[0].forward(signal)
        signal = self.mappings[1].forward(signal)
        signal = self.mappings[2].forward(signal)
        signal = self.mappings[3].forward(signal)

        signal = self.mappings[4].forward(signal)

        signal = self.mappings[3].backward(signal)
        signal = self.mappings[2].backward(signal)
        signal = self.mappings[1].backward(signal)
        signal = self.mappings[0].backward(signal)

        result = as_symbol(signal)

        return result.lower() if was_lower else result


def numbers_to_symbols(numbers: str) -> str:
    s = [SYMBOLS[int(n) - 1] for n in numbers.split()]
    return ''.join(s)


cfg = EnigmaConfig(
    jumpers='AV BS CG DL FU HZ IN KM OW RX'.split(),
    reflector=REFLECTOR_B,
    rotors=[ROTOR_II, ROTOR_IV, ROTOR_V],
    rings=numbers_to_symbols('02 21 12'),
)


cfg.set_key('BLA')
for sym in """EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ
REZKM LXLVE FGUEY SIOZV EQMIK UBPMM YLKLT TDEIS 
MDICA GYKUA CTCDO MOHWX MUUIA UBSTS LRNBZ SZWNR 
FXWFY SSXJZ VIJHI DISHP RKLKA YUPAD TXQSP INQMA 
TLPIF SVKDA SCTAC DPBOP VHJK-""".replace(' ', '').replace('\n', ''):
    plain = cfg.translate(sym)
    print(' ' if plain == 'X' else 'CH' if plain == 'Q' else plain, end='')
print('\n', cfg.mappings[3].labels[0], cfg.mappings[2].labels[0], cfg.mappings[1].labels[0], sep='')
