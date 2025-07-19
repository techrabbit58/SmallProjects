import time

from colterm import term

colors = "red yellow green blue cyan purple".split()


def show_rainbow(indent: int) -> None:
    print(" " * indent, end="")
    for color in colors:
        term.fg(color)
        print("##", end="")
    print()
    time.sleep(0.02)


def advance(indent: int, is_indent_increasing: bool) -> tuple[int, bool]:
    indent += 1 if is_indent_increasing else -1
    if indent == 0 or indent == term.size().columns - 13:
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
            show_rainbow(indent)
            indent, is_indent_increasing = advance(indent, is_indent_increasing)
        except KeyboardInterrupt:
            is_terminated = True


main()
