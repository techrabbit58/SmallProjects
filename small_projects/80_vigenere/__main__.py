import itertools
import textwrap
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial

import pyperclip


@dataclass
class Cipher:
    encrypt: Callable[[str], str] = field(kw_only=True)
    decrypt: Callable[[str], str] = field(kw_only=True)


_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def vigenere(key: list[int]) -> Cipher:

    def rotate(ch: str, distance: int) -> str:
        if ch not in _symbols:
            return ch
        offset = (_symbols.find(ch.lower()) + distance) % 26
        return _symbols[offset] if ch.islower() else _symbols[26 + offset]

    def to_crypto(ch: str, d: int) -> str:
        return rotate(ch, d)

    def to_plain(ch: str, d: int) -> str:
        return rotate(ch, 26 - d)

    def translate(text: str, func: Callable[[str, int], str]) -> str:
        offset = itertools.cycle(key)
        return ''.join(func(inp, next(offset)) if inp in _symbols else inp for inp in text)

    return Cipher(encrypt=partial(translate, func=to_crypto), decrypt=partial(translate, func=to_plain))


def usage() -> str:
    return textwrap.dedent(
        """
        k KEY     enter a new key
        e TEXT    encrypt the given text
        d TEXT    decrypt the given text
        h         print this help text
        q         stop the program
        Ctrl-C    stop the program
        """
    ).strip()


def make_key_from_text(text: str) -> list[int]:
    return [_symbols.find(ch.lower()) for ch in text if ch in _symbols]


def cmdloop(prog: str) -> None:
    print(f'===== {prog} =====')
    print("'Enter a key or a message to encrypt or decrypt using Vigenere's cipher.'")
    print('Enter "h" to get help about the available commands.')
    print('Press <Ctrl-C> to quit.')

    cipher = None

    while True:
        try:
            response = input('> ').strip().replace('\x1a', '')
            if response == '':
                continue
            if response in {'h', 'H'}:
                print(usage())
                continue
            if response in {'q', 'Q'}:
                break

            cmd, _, text = response.partition(' ')
            cmd = cmd.lower()
            text = text.strip()

            if cmd == 'k':  # assign a new key
                key = make_key_from_text(text)
                cipher = vigenere(key)
            elif cmd in {'e', 'd'} and cipher is None:
                print('Cannot encrypt or decrypt: A key must first be set.')
            elif cmd == 'e':
                print(crypted := cipher.encrypt(text))
                pyperclip.copy(crypted)
            elif cmd == 'd':
                print(plain := cipher.decrypt(text))
                pyperclip.copy(plain)
            else:
                print(f'Unknown action: "{cmd} {text}"')

        except KeyboardInterrupt:
            print()
            break

        except EOFError:
            continue

    print('Bye!')


if __name__ == '__main__':
    cmdloop('Vigenere Cipher')
