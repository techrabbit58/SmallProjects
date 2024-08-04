import pytest

from .plugboard import Plugboard
from .symbols import as_signal, as_symbol


@pytest.mark.parametrize('actual, expected', ['BB', 'AM', 'MA', 'XX', 'SP', 'WZ', 'QQ', 'TU'])
def test_plugboard(actual, expected):
    pb = Plugboard('AM FI NV PS TU WZ')
    assert as_symbol(pb[as_signal(actual)]) == expected
