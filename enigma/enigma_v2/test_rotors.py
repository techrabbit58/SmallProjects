import pytest

from .basics import to_symbols
from .rotors import rotors

defaults = [
    ('I', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
    ('II', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
    ('III', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
    ('IV', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
    ('V', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
    ('VI', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'),
    ('VII', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'),
    ('VIII', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),
]


@pytest.mark.parametrize('rotor, left, right, notches', defaults)
def test_rotor_default_settings(rotor, left, right, notches):
    actual = rotors[rotor].create()
    assert to_symbols(actual.left) == left
    assert to_symbols(actual.right) == right
    assert to_symbols(actual.notches) == notches


@pytest.mark.parametrize('rotor, left, right, notches', defaults)
def test_rotor_overwrite_default_with_default(rotor, left, right, notches):
    actual = rotors[rotor].set_ring('01').set_key('A').create()
    assert to_symbols(actual.left) == left
    assert to_symbols(actual.right) == right
    assert to_symbols(actual.notches) == notches


@pytest.mark.parametrize('rotor, key, ring, left, right, notches', [
    ('III', 'A', '01', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
    ('III', 'B', '01', 'BCDEFGHIJKLMNOPQRSTUVWXYZA', 'DFHJLCPRTXVZNYEIWGAKMUSQOB', 'V'),
    ('III', 'B', '02', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'U'),
    ('III', 'T', '01', 'TUVWXYZABCDEFGHIJKLMNOPQRS', 'AKMUSQOBDFHJLCPRTXVZNYEIWG', 'V'),
    ('III', 'T', '02', 'STUVWXYZABCDEFGHIJKLMNOPQR', 'GAKMUSQOBDFHJLCPRTXVZNYEIW', 'U'),
    ('III', 'T', '03', 'RSTUVWXYZABCDEFGHIJKLMNOPQ', 'WGAKMUSQOBDFHJLCPRTXVZNYEI', 'T'),
    ('III', 'T', '04', 'QRSTUVWXYZABCDEFGHIJKLMNOP', 'IWGAKMUSQOBDFHJLCPRTXVZNYE', 'S'),
    ('III', 'T', '05', 'PQRSTUVWXYZABCDEFGHIJKLMNO', 'EIWGAKMUSQOBDFHJLCPRTXVZNY', 'R'),
    ('V', 'A', '01', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
    ('V', 'A', '02', 'ZABCDEFGHIJKLMNOPQRSTUVWXY', 'KVZBRGITYUPSDNHLXAWMJQOFEC', 'Y'),
    ('V', 'Z', '26', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'A'),
    ('VIII', 'A', '01', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),
    ('VIII', 'A', '02', 'ZABCDEFGHIJKLMNOPQRSTUVWXY', 'VFKQHTLXOCBJSPDZRAMEWNIUYG', 'YL'),
])
def test_rotor_key_ring_setup(rotor, key, ring, left, right, notches):
    actual = rotors[rotor].set_ring(ring).set_key(key).create()
    assert to_symbols(actual.left) == left
    assert to_symbols(actual.right) == right
    assert to_symbols(actual.notches) == notches
