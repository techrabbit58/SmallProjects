import base64
import string

from .scramblingdevice import ScramblingDevice


def base64_encrypt(enigma: ScramblingDevice, key: str, text: str) -> str:
    enigma.set_key(key)

    result = []
    for symbol in base64.b64encode(text.encode()).decode():
        was_lowercase = symbol.islower()
        result.append(enigma.convert(symbol.upper()))
        if was_lowercase:
            result[-1] = result[-1].lower()

    return ''.join(result)


def base64_decrypt(enigma: ScramblingDevice, key: str, text: str) -> str:
    enigma.set_key(key)

    result = []
    for symbol in text:
        if symbol in string.whitespace:
            continue
        was_lowercase = symbol.islower()
        result.append(enigma.convert(symbol.upper()))
        if was_lowercase:
            result[-1] = result[-1].lower()

    return base64.b64decode(''.join(result).encode()).decode()


def in_groups(text: str, *, group_size: int = 5) -> str:
    groups = []
    single_group = []

    for symbol in text:
        if symbol == ' ':
            continue

        single_group.append(symbol)
        if len(single_group) == group_size:
            groups.append(''.join(single_group))
            single_group = []

    groups.append(''.join(single_group))

    return ' '.join(groups)
