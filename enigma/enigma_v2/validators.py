from .reflectors import reflectors
from .rotors import m_rotor_stencils, rocket_rotor_stencils
from .symbols import NUMERIC_RING_SETTINGS, SYMBOLS


def ensure_valid_mil_reflector(r: str) -> str:
    if r not in reflectors:
        raise ValueError(f'reflector "{r}" is not compatible with Enigma I or Enigma M3 (valid are: "A", "B", "C")')
    return r


def ensure_valid_ring_setting(s: str) -> str:
    if s not in NUMERIC_RING_SETTINGS:
        raise ValueError(f'"{s}" is not a valid ring setting (valid are: 01 ... 26)')
    return s


def ensure_valid_jumpers(j: str) -> str:
    used = set()
    for a, b in j.split():
        if a not in SYMBOLS and b not in SYMBOLS:
            raise ValueError(f'"{a}{b}" is not a pluggable symbol pair')
        if a == b:
            raise ValueError(f'"{a}{b}" symbols can not be jumpered to themselves')
        if a in used or b in used:
            raise ValueError(f'symbols can only be plugged once (duplicate jumper: "{a}{b}")')
        used.update({a, b})
    return j


def ensure_valid_m3_rotor(r: str) -> str:
    if r not in m_rotor_stencils:
        raise ValueError(f'rotor "{r}" is not compatible with Enigma I or Enigma M3 (valid are: "I" ... "VIII")')
    return r


def ensure_valid_a27_rotor(r: str) -> str:
    if r not in rocket_rotor_stencils:
        raise ValueError(f'rotor "{r}" is not compatible with Enigma I or Enigma M3 (valid are: "I" ... "VIII")')
    return r


def ensure_valid_key(key: str) -> str:
    for s in key:
        if s not in SYMBOLS:
            raise ValueError(f'invalid key "{key}": only symbols "A" ... "Z" are valid key symbols')
    return key
