import time

from colterm import term

COLOR_WIDTH = 4
COLORS = "red yellow green blue cyan purple".split()
RAINBOW_WIDTH = COLOR_WIDTH * len(COLORS)


def show(indent: int) -> None:
    print(" " * indent, end="")
    for color in COLORS:
        term.fg(color)
        print("#" * COLOR_WIDTH, end="")
    print()
    time.sleep(0.02)


def advance(indent: int, is_indent_increasing: bool) -> tuple[int, bool]:
    indent += 1 if is_indent_increasing else -1
    if indent == 0 or indent == term.size().columns - RAINBOW_WIDTH - 1:
        is_indent_increasing = not is_indent_increasing
    return indent, is_indent_increasing


def main() -> None:
    indent = 0
    is_indent_increasing = True

    print("Press Ctrl-C to stop.")
    time.sleep(3)

    is_terminated = False

    while not is_terminated:
        try:
            show(indent)
            indent, is_indent_increasing = advance(indent, is_indent_increasing)
        except KeyboardInterrupt:
            is_terminated = True


main()
