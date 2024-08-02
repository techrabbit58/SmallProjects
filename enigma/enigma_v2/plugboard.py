from collections.abc import Callable

from .basics import as_signal


def populate(jumpers: str) -> Callable[[int], int]:
    """
    Convert a given string of symbol pairs (like: 'AF GH QX NR') to a dictionary.
    The pairs are first converted to the corresponding ordinals, and then assigned
    to a "forward/backward" pair of dictionary items.
    The function returns a callable that allows to map a given signal left to right
    and right to left. The Callable does simply return its argument unchanged.
    Callers of the function may give the resulting Callable a local name.
    The resulting Callable can betaken as the customized plugboard function of an
    actual Enigma I or M3 configuration.
    """
    plugboard = {}

    for left, right in jumpers.split():
        a, b = as_signal(left), as_signal(right)
        plugboard[a], plugboard[b] = b, a

    def get(signal: int) -> int:
        """
        Return the given signal unchanged if there is no match.
        If there is the given signal in the plugboard dictionary,
        the function will return the corresponding output signal.
        """
        return plugboard.get(signal, signal)

    return get
