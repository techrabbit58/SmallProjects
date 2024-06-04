ALPHABET = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def encrypt(key: str, message: str) -> str:
    return _codec(_straight_key(key), message)


def decrypt(key: str, message: str) -> str:
    return _codec(_inverted_key(key), message)


def rot13(message: str) -> str:
    return encrypt('N', message)


def _inverted_key(key: str) -> int:
    return len(ALPHABET) - ALPHABET.index(key[0].upper())


def _straight_key(key: str) -> int:
    return ALPHABET.index(key[0].upper())


def _codec(key: int, message: str) -> str:
    code = []
    for ch in message.upper():
        if ch in ALPHABET:
            pos = ALPHABET.index(ch)
            ch = ALPHABET[(pos + key) % len(ALPHABET)]
        code.append(ch)
    return ''.join(code)


if __name__ == '__main__':
    cipher = 'E'
    plain = 'Ask for me tomorrow, and you shall find me a grave man.'
    print('    plain:', plain)
    print('encrypted:', encrypted := rot13(plain))
    print('decrypted:', rot13(encrypted))
