import pytest

from .basics import to_symbols, as_symbol, ALPHABET_SIZE
from .rotors import rotor_stencils

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
    actual = rotor_stencils[rotor].create()
    assert to_symbols(actual.left) == left
    assert to_symbols(actual.right) == right
    assert to_symbols(actual.notches) == notches


@pytest.mark.parametrize('rotor, left, right, notches', defaults)
def test_rotor_overwrite_default_with_default(rotor, left, right, notches):
    actual = rotor_stencils[rotor].set_ring('01').create().set_key('A')
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
    actual = rotor_stencils[rotor].set_ring(ring).create()
    actual.set_key(key)
    assert to_symbols(actual.left) == left
    assert to_symbols(actual.right) == right
    assert to_symbols(actual.notches) == notches


@pytest.mark.parametrize('rotor, key, expect_notch, expect_left, expect_right', [
    ('V', 'A', False, 'B', 'Z'),
    ('V', 'B', False, 'C', 'B'),
    ('V', 'Y', True, 'Z', 'K'),
    ('V', 'Z', False, 'A', 'V'),
    ('III', 'T', False, 'U', 'K'),
    ('III', 'U', True, 'V', 'M'),
    ('III', 'V', False, 'W', 'U'),
    ('VII', 'Y', True, 'Z', 'T'),
    ('VII', 'L', True, 'M', 'B'),
])
def test_rotor_can_step_forward(rotor, key, expect_notch, expect_left, expect_right):
    actual = rotor_stencils[rotor].create().set_key(key).rotate()
    assert actual.is_at_notch() == expect_notch
    assert as_symbol(actual.left[0]) == expect_left
    assert as_symbol(actual.right[0]) == expect_right


def test_same_rotor_different_keys():
    actual = rotor_stencils['VIII'].set_ring('05').create()

    actual.set_key('X')
    assert as_symbol(actual.left[0]) == 'T'

    actual.set_key('B')
    assert as_symbol(actual.left[0]) == 'X'


def test_same_rotor_different_key_many_steps():
    actual = rotor_stencils['III'].set_ring('05').create()

    actual.set_key('X')

    for _ in range(ALPHABET_SIZE + 5):
        actual.rotate()

    assert as_symbol(actual.left[0]) == 'Y'

    actual.set_key('B')

    for _ in range(ALPHABET_SIZE + 7):
        actual.rotate()

    assert as_symbol(actual.left[0]) == 'E'
