from .symbols import as_signal


class Plugboard:
    """
    Convert a given string of symbol pairs (like: 'AF GH QX NR') to a dictionary.
    The pairs are first converted to the corresponding ordinals, and then assigned
    to a "forward/backward" pair of dictionary items.
    """
    def __init__(self, jumpers: str = '') -> None:
        self.conversions = {}
        for left, right in jumpers.split():
            a, b = as_signal(left), as_signal(right)
            self.conversions[a], self.conversions[b] = b, a

    def __getitem__(self, signal: int) -> int:
        """
        Return the given signal unchanged if there is no match.
        If there is the given signal in the plugboard dictionary,
        the function will return the corresponding output signal.
        """
        return self.conversions.get(signal, signal)
