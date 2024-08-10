from .enigma import Enigma


def casual_conversion(enigma: Enigma, key: str, text: str) -> str:
    enigma.set_key(key)

    result = []
    for symbol in text:
        was_lowercase = symbol.islower()
        result.append(enigma.convert(symbol.upper()))
        if was_lowercase:
            result[-1] = result[-1].lower()

    return ''.join(result)
