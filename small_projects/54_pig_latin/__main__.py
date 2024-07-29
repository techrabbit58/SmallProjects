import signal
from typing import Never

import pyperclip

from . import piglatin


def ctrl_c_handler(*_) -> Never:
    print('^C')
    raise EOFError()


signal.signal(signal.SIGINT, ctrl_c_handler)


def gameloop(prog: str) -> None:
    response = None
    is_terminated = False

    while not is_terminated:
        try:
            print('Enter your message to translate. Stops on <Ctrl-C> or EOF.')
            response = input('> ').strip().removesuffix('\x1a')
        except EOFError:
            is_terminated = True

        if not response:
            continue

        translated = piglatin.to_english_piglatin(response)
        print(f'{prog}: "{translated}"\n')
        pyperclip.copy(translated)


gameloop('Pig Latin')
print('Bye!')
