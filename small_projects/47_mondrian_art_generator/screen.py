from colterm import term

BLANK = " "

width = height = None


def init() -> None:
    global width, height
    width = term.width() - 1
    height = term.height() - 2


def draw(x: int, y: int, color: str) -> None:
    term.bg(color)
    print(BLANK, end="")


def flush_line() -> None:
    print()


def clear() -> None:
    term.clear()


init()
