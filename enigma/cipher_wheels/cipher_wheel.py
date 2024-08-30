from collections import deque

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class CipherWheel:
    def __init__(self, mapping: str) -> None:
        self.right = deque(mapping)
        self.left = deque(SYMBOLS)

    def forward(self, symbol: str) -> str:
        return _translate(symbol, self.right, self.left)

    def __getitem__(self, symbol: str) -> str:
        return self.forward(symbol)

    def backward(self, symbol: str) -> str:
        return _translate(symbol, self.left, self.right)

    def step(self, distance: int = -1) -> None:
        self.right.rotate(distance)
        self.left.rotate(distance)


def _translate(c: str, a: deque[str], b: deque[str]) -> str:
    is_lower, symbol = c.islower(), c.upper()

    if symbol not in SYMBOLS:
        return c

    index = a.index(symbol)
    out = b[index]

    return out.lower() if is_lower else out


def main():
    mapping = [
        CipherWheel(''.join(reversed(SYMBOLS))),  # atbash
        CipherWheel(SYMBOLS[13:] + SYMBOLS[:13]),  # rot13
        CipherWheel(SYMBOLS[-2:] + SYMBOLS[:-2]),  # caesar
    ]

    for algo in mapping:
        message = 'Hello, world!'
        print(message)

        cryptotext = ''.join(algo.forward(c) for c in message)
        print(cryptotext)

        plaintext = ''.join(algo.backward(c) for c in cryptotext)
        print(plaintext)

        print()


main()
