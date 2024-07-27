import shlex
import textwrap
from collections.abc import Callable


class Shell:
    def __init__(self, prog: str) -> None:
        self._prog = prog
        self._symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self._key = None

    def _get_action(self, candidate: str) -> Callable[[list[str]], bool | None]:
        candidate = f'do_{candidate.lower()}'
        return getattr(self, candidate, self.do_default)

    def cmdloop(self) -> None:
        print('\n=====', self._prog, '=====\n')
        while True:
            try:
                response = input('Enter a valid command, or "help" to get a brief usage information.\n> ').strip()
                args = shlex.split(response)
                action = self._get_action(args[0])
                is_terminated = action(args)
                if is_terminated:
                    break
            except ValueError as ex:
                print(ex)
            except KeyboardInterrupt:
                print('^C')
                break
            except (EOFError, IndexError):
                pass

    def do_random(self, args: list[str]) -> None:
        """RANDOM\t\tGenerate a random key."""

    def do_key(self, args: list[str]) -> None:
        """KEY keyword(s)\tMake a new key from the given keyword(s)."""
        raw_key = [ch.lower() for ch in ''.join(args[1:]) if ch in self._symbols]
        print(f'"{"".join(raw_key)}"')

    def do_encrypt(self, args: list[str]) -> None:
        """ENCRYPT\t\tSwitch to encryption mode."""

    def do_decrypt(self, args: list[str]) -> None:
        """DECRYPT\t\tSwitch to decryption mode."""

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

    @staticmethod
    def do_default(args: list[str]) -> None:
        """line\t\tEncrypt or decrypt the given line of text. Depends on current mode."""
        print(f'line of text: "{' '.join(args)}"')


Shell('Simple Substitution Cipher').cmdloop()

print('Bye!')
