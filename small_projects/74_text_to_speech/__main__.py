import argparse
from typing import cast

import pyttsx3, pyttsx3.voice


def get_cli_args(prog: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog, description='Use the text-to-speech features of the pyttsx3 library to generate audio.')
    parser.add_argument(
        'text',
        help='the text to convert to audible voice')
    return parser.parse_args()


def main(prog: str) -> None:
    args = get_cli_args(prog)
    text = args.text
    tts = pyttsx3.init()
    voices = cast(list[pyttsx3.voice.Voice], tts.getProperty('voices'))
    voice = voices[1]
    tts.setProperty('voice', voice.id)
    tts.setProperty('rate', 150)
    tts.say(text)
    tts.runAndWait()


main('Text to Speech')
