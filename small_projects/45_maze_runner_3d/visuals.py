import io
import os
import sys
import textwrap
from dataclasses import dataclass

from . import constants as const


def clear_screen() -> None:
    clear = "cls" if sys.platform == "win32" else "clear"
    os.system(clear)


@dataclass(frozen=True, kw_only=True)
class Picture:
    pixels: dict[tuple[int, int], str]
    width: int
    height: int
    rel: tuple[int, int]

    def __str__(self) -> str:
        text = io.StringIO()
        print(const.FRAME * (self.width + 2), file=text)
        for y in range(self.height):
            print(const.FRAME, end="", file=text)
            for x in range(self.width):
                wall = self.pixels[x, y].replace(".", " ")
                print(wall, end="", file=text)
            print(const.FRAME, file=text)
        print(const.FRAME * (self.width + 2), file=text)
        return text.getvalue()

    def __iadd__(self, other: "Picture") -> "Picture":
        dx, dy = other.rel
        pixels = self.pixels.copy()
        for (x, y), symbol in other.pixels.items():
            pixels[x + dx, y + dy] = symbol
        return Picture(pixels=pixels, width=self.width, height=self.height, rel=self.rel)

    __add__ = __iadd__


def _new_picture(image: str, rel: tuple[int, int] = (0, 0)) -> Picture:
    pixels: dict[tuple[int, int], str] = {}
    height = width  = 0
    rows = textwrap.dedent(image).strip().splitlines()
    for y, row in enumerate(rows):
        height = max(height, y)
        for x, symbol in enumerate(row):
            width = max(width, x)
            pixels[x, y] = symbol
    return Picture(pixels=pixels, width=width + 1, height=height + 1, rel=rel)


ALL_OPEN = _new_picture(r"""
.................
____.........____
...|\......./|...
...||.......||...
...||__...__||...
...||.|\./|.||...
...||.|.X.|.||...
...||.|/.\|.||...
...||_/...\_||...
...||.......||...
___|/.......\|___
.................
.................
""")

CLOSED = {
    "A": _new_picture(r"""
    _____
    .....
    .....
    .....
    _____
    """, rel=(6, 4)),
    "B": _new_picture(r"""
    .\.
    ..\
    ...
    ...
    ...
    ../
    ./.
    """, rel=(4, 3)),
    "C": _new_picture(r"""
    ./.
    /..
    ...
    ...
    ...
    \..
    .\.
    """, rel=(10, 3)),
    "D": _new_picture(r"""
    ___________
    ...........
    ...........
    ...........
    ...........
    ...........
    ...........
    ...........
    ...........
    ___________
    """, rel=(3, 1)),
    "E": _new_picture(r"""
    ..\..
    ...\_
    ....|
    ....|
    ....|
    ....|
    ....|
    ....|
    ....|
    ....|
    ....|
    .../.
    ../..
    """, rel=(0, 0)),
    "F": _new_picture(r"""
    ../..
    _/...
    |....
    |....
    |....
    |....
    |....
    |....
    |....
    |....
    |....
    .\...
    ..\..
    """, rel=(12, 0)),
}

WAY_OUT_SIGN = {
    "C": _new_picture("""
    EXIT
    """, rel=(7, 9)),
    "E": _new_picture("""
    EXIT
    """, rel=(0, 11)),
    "F": _new_picture("""
    EXIT
    """, rel=(13, 11)),
}
