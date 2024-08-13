import functools
from collections.abc import Callable

from .symbols import NUMERIC_RING_SETTINGS, SYMBOLS


m3_reflectors = 'A B C'
m4_reflectors = 'Bruno Cäsar'


def _ensure_valid_reflector(r: str, enigma: str, reflectors: list[str]) -> str:
    if r not in reflectors:
        raise ValueError(f'reflector "{r}" is not compatible with {enigma} (valid are: {", ".join(reflectors)})')
    return r


def _reflector_checker(enigma: str, reflectors: str) -> Callable[[str], str]:
    return functools.partial(_ensure_valid_reflector, enigma=enigma, reflectors=reflectors.split())


ensure_valid_i_m3_reflector = _reflector_checker('Enigma I or Enigma M3', m3_reflectors)
ensure_valid_m4_reflector = _reflector_checker('Enigma M4', m4_reflectors)


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


i_rotors = 'I II III IV V'
m3_rotors = 'I II III IV V VI VII VIII'
m4_rotors = 'I II III IV V VI VII VIII Beta Gamma'
rocket_rotors = 'I II III'


def _rotor_checker(enigma: str, rotors: str) -> Callable[[str], str]:
    return functools.partial(_ensure_valid_rotor, enigma=enigma, rotors=rotors.split())


def _ensure_valid_rotor(r: str, enigma: str, rotors: list[str]) -> str:
    if r not in rotors:
        raise ValueError(f'rotor "{r}" is not compatible with {enigma} (valid are: {", ".join(rotors)})')
    return r


ensure_valid_i_rotor = _rotor_checker('Enigma I', i_rotors)
ensure_valid_m3_rotor = _rotor_checker('Enigma M3', m3_rotors)
ensure_valid_m4_rotor = _rotor_checker('Enigma M4', m4_rotors)
ensure_valid_rocket_rotor = _rotor_checker('Enigma Rocket', rocket_rotors)


def ensure_valid_key(key: str) -> str:
    for s in key:
        if s not in SYMBOLS:
            raise ValueError(f'invalid key "{key}": only symbols "A" ... "Z" are valid key symbols')
    return key


def ensure_rotors_are_unique(rotors: list[str]) -> list[str]:
    if len(set(rotors)) != len(rotors):
        raise ValueError(f'invalid rortor set: "{rotors}" does contain duplicates')
    return rotors
