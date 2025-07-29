import argparse
import math
import shutil
import time


def get_args(title: str) -> str:
    parser = argparse.ArgumentParser(
        prog=title,
        description="Al Sweigart's Sine Message (from the \"Small Projects\" book)",
    )
    parser.add_argument(
        "message", nargs=argparse.ONE_OR_MORE,
        help="The message to display (max. 39 characters)",
    )
    message = parser.parse_args().message
    return " ".join(message)[:39]


def get_screen_width():
    width, _ = shutil.get_terminal_size()
    return width


def main(title: str) -> None:
    message = get_args(title)
    screen_width = get_screen_width()
    multiplier = (screen_width - len(message)) / 2.0

    step: float = 0

    is_terminated = False
    while not is_terminated:
        try:
            sine = -math.cos(step)
            padding = " " * int((sine + 1) * multiplier)
            print(f"{padding}{message}")
            time.sleep(0.1)
            step += math.pi / 16
        except KeyboardInterrupt:
            is_terminated = True


if __name__ == '__main__':
    main("sinemessage")
