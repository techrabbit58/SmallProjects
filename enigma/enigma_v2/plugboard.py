from collections.abc import Callable

from .basics import as_signal


def populate(jumpers: str) -> Callable[[int], int]:
    plugboard = {}
    for left, right in jumpers.split():
        a, b = as_signal(left), as_signal(right)
        plugboard[a], plugboard[b] = b, a

    def get(signal: int) -> int:
        return plugboard.get(signal, signal)

    return get
