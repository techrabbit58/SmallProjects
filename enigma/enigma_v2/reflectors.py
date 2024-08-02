from .basics import to_signals


class Reflector:
    def __init__(self, wiring: str) -> None:
        self.reflections = to_signals(wiring)

    def __getitem__(self, signal: int) -> int:
        return self.reflections[signal]


reflectors: dict[str, Reflector] = {
    'A': Reflector('EJMZALYXVBWFCRQUONTSPIKHGD'),
    'B': Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
    'C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL'),
}
