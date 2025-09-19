import os
import random
import shutil
import textwrap
import time
from string import Template

import httpx
from playsound3 import playsound

URL = Template("https://inventwithpython.com/sound${letter}.wav")
ASDF = "ASDF"


class SoundFile:
    def __init__(self, url: str) -> None:
        self._url = url
        self._name = os.path.dirname(__file__) + "\\" + url.split("/")[-1]
        if not os.path.exists(self._name):
            self._download()

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    def _download(self):
        response = httpx.get(self.url)
        with open(self.name, "wb") as f:
            f.write(response.read())
        print(f"Download complete: {self.url}")


def intro() -> str:
    return textwrap.dedent("""
    * * *   S o u n d   M i m i c   * * *
    
    Try to memoize a pattern of A S D and F letters (each with its own sound)
    as it gets longer and longer.
    """)


def main():
    print(intro())
    input("Press Enter to begin ...")

    files = get_sound_files()
    game_loop(files)

    print("Thank you for playing!\n")


def get_sound_files():
    return {letter: SoundFile(URL.substitute(letter=letter)) for letter in "ASDF"}


def game_loop(files):
    pattern = ""

    while True:
        clear_screen()

        pattern += next_letter()

        print("Pattern: ", end="")
        for letter in pattern:
            print(letter, end="", flush=True)
            filename = files[letter].store
            playsound(filename)

        time.sleep(1)
        clear_screen()

        answer = input("Enter the pattern:\n> ").strip().upper()

        if answer != pattern:
            print(f"Incorrect!\nThe pattern was: {pattern}")
            for letter in pattern:
                filename = files[letter].store
                playsound(filename)

            print(f"You scored {len(pattern) - 1} points.")
            break

        print("Correct!")
        time.sleep(1)


def clear_screen():
    _, height = shutil.get_terminal_size((80, 24))
    for _ in range(height + 1):
        print()


def next_letter():
    pattern = random.choice(ASDF)
    return pattern


main()
