SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_SIZE = len(SYMBOLS)


def translate(c: str, a: str, b: str) -> str:
    is_lower, symbol = c.islower(), c.upper()

    if symbol not in SYMBOLS:
        return c

    index = a.find(symbol)
    out = b[index]

    return out.lower() if is_lower else out


def index_of(symbol: str) -> int:
    return SYMBOLS.find(symbol)


class CaesarWheel:
    def __init__(self, key: int):
        key = ALPHABET_SIZE - (key % len(SYMBOLS))
        self.right = SYMBOLS[key:] + SYMBOLS[:key]
        self.left = SYMBOLS

    def encrypt(self, symbol: str) -> str:
        return translate(symbol, self.right, self.left)

    def decrypt(self, symbol: str) -> str:
        return translate(symbol, self.left, self.right)


def main():
    wheel = CaesarWheel(index_of('N'))

    message = 'Meet me by the rose bushes tonight.'
    print(message)

    cryptotext = ''.join(wheel.encrypt(c) for c in message)
    print(cryptotext)

    plaintext = ''.join(wheel.decrypt(c) for c in cryptotext)
    print(plaintext)

    assert message == plaintext


main()
