from .symbols import to_signals


class Reflector:
    """
    Reflectors can only be used in "forward" direction.
    They convert signals to another.
    This is done by storing the "wiring" order of
    signals to an array.
    If the array gets indexed with a given signal,
    the reflector object answers with the scrambled
    signal.
    Physical enigma rotors can never map an input signal
    to itself.
    This is due to the used technology and construction.
    The reflectors give the enigma machines their
    self-reciprocal encryption property.
    """
    def __init__(self, wiring: str) -> None:
        self.reflections = to_signals(wiring)
        for i, n in enumerate(self.reflections):
            if i == n:
                raise ValueError('impossible wiring: cannot connect an input to itself')

    def __getitem__(self, signal: int) -> int:
        """
        When indexed with a given signal, return another signal.
        This shall never convert a given signal to itself.
        """
        return self.reflections[signal]


reflectors: dict[str, Reflector] = {
    'A': Reflector('EJMZALYXVBWFCRQUONTSPIKHGD'),
    'B': Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
    'C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL'),
    'Bruno': Reflector('ENKQAUYWJICOPBLMDXZVFTHRGS'),
    'Cäsar': Reflector('RDOBJNTKVEHMLFCWZAXGYIPSUQ'),
}
