import random
import shlex
from collections.abc import Callable

import pyperclip


class Shell:
    def __init__(self, prog: str) -> None:
        self._prog = prog
        self._symbols = 'abcdefghijklmnopqrstuvwxyz'
        self._shuffled = self._keys = self._values = None

    def _get_action(self, candidate: str) -> Callable[[list[str]], bool | None]:
        candidate = f'do_{candidate.lower()}'
        for attr in dir(self):
            if attr != 'do_default' and attr.startswith(candidate):
                candidate = attr
        return getattr(self, candidate, self.do_default)

    def _show_key(self) -> None:
        print(f'The key is "{"".join(self._shuffled).upper()}".')

    def do_info(self, _: list[str]) -> None:
        """INFO\t\tShow some runtime information."""
        print(f'mode = {"ENCRYPT" if self._shuffled == self._values else "DECRYPT"}')
        print(f' key = {None if self._shuffled is None else "".join(self._shuffled).upper()}')
        print()

    def cmdloop(self) -> None:
        print('\n=====', self._prog, '=====\n')
        while True:
            try:
                response = input('Enter a valid command, or "help" to get a brief usage information.\n> ').strip()
                args = shlex.split(response)
                action = self._get_action(args[0])
                is_terminated = action([response] if action is self.do_default else args)
                if is_terminated:
                    break
            except ValueError as ex:
                print(ex)
            except KeyboardInterrupt:
                print('^C')
                break
            except (EOFError, IndexError):
                pass

    def do_random(self, _: list[str]) -> None:
        """RANDOM\t\tGenerate a random key."""
        self._shuffled = list(self._symbols)
        random.shuffle(self._shuffled)
        self._show_key()
        self.do_encrypt()

    def do_key(self, args: list[str]) -> None:
        """KEY keyword(s)\tMake a new key from the given keyword(s)."""
        raw_key = [ch.lower() for ch in ''.join(args[1:]) if ch.lower() in self._symbols]
        if not raw_key:
            print('The KEY command requires an argument!\n')
            return
        self._shuffled = []
        remaining_symbols = list(self._symbols)
        for ch in raw_key:
            if ch in self._shuffled:
                continue
            self._shuffled.append(ch)
            remaining_symbols.remove(ch)
        self._shuffled += remaining_symbols
        self._show_key()
        self.do_encrypt()

    def do_encrypt(self, _: list[str] = None) -> None:
        """ENCRYPT\t\tSwitch to encryption mode."""
        if self._shuffled is None:
            print('You must first create a key.')
            return
        self._keys, self._values = list(self._symbols), self._shuffled
        print('Now in encryption mode.\n')

    def do_decrypt(self, _: list[str] = None) -> None:
        """DECRYPT\t\tSwitch to decryption mode."""
        if self._shuffled is None:
            print('You must first create a key.')
            return
        self._keys, self._values = self._shuffled, list(self._symbols)
        print('Now in decryption mode.\n')

    @staticmethod
    def do_quit(_: list[str]) -> bool:
        """QUIT\t\tStop execution."""
        return True

    def do_help(self, _: list[str]) -> None:
        """HELP\t\tShow this usage information."""
        print()
        for attr in dir(self):
            if attr.startswith('do_'):
                print(getattr(self, attr).__doc__)
        print()

    def do_default(self, args: list[str]) -> None:
        """line\t\tEncrypt or decrypt the given line of text. Depends on current mode."""
        if self._shuffled is None:
            print('You must first create a key.')
            return

        out = []
        for inp in ' '.join(args):
            try:
                offset = self._keys.index(inp.lower())
            except ValueError:
                offset = -1

            if offset < 0:
                out.append(inp)
            elif inp.islower():
                out.append(self._values[offset])
            else:
                out.append(self._values[offset].upper())

        result = ''.join(out)
        print(f'"{result}"\n')
        pyperclip.copy(result)


if __name__ == '__main__':
    Shell('Simple Substitution Cipher').cmdloop()
    print('Bye!')
