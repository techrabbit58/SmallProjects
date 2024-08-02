import pytest

from .reflectors import reflectors
from .basics import as_symbol, as_signal


@pytest.mark.parametrize('choice, actual, expected', [
    ('A', 'A', 'E'),
    ('A', 'M', 'C'),
    ('B', 'Q', 'E'),
    ('B', 'X', 'J'),
    ('C', 'E', 'I'),
    ('C', 'F', 'A'),
])
def test_reflector(choice, actual, expected):
    reflector = reflectors[choice]
    assert as_symbol(reflector[as_signal(actual)]) == expected
