import os
from string import Template

import httpx
from playsound3 import playsound

URL = Template("https://inventwithpython.com/sound${letter}.wav")


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


def main():
    files = {letter: SoundFile(URL.substitute(letter=letter)) for letter in "ASDF"}

    for letter in "ASDFFFSSAD":
        filename = files[letter].name
        playsound(filename)


main()
