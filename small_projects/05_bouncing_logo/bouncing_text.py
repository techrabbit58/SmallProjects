import sys
from typing import Self
from colterm import term


class BouncingText:
    def __init__(self, text: str) -> None:
        self.text = text
        width = len(text)
        self.blank = ' ' * width
        self.text_width = width
        self.pos = [term.width() // 2, term.height() // 2]
        self.last_pos = self.pos.copy()
        self.color = ['reset', 'reset']
        self.bright = False
        self.dir = [1, -1]

    def fg(self, color: str, *, bright: bool = True) -> Self:
        self.color[0] = color
        self.bright = bright
        return self

    def bg(self, color: str) -> Self:
        self.color[1] = color
        return self

    def location(self, x: int, y: int) -> Self:
        self.pos = [x, y]
        return self

    def direction(self, dx: int, dy: int) -> Self:
        self.dir = [dx // abs(dx), dy // abs(dy)]
        return self

    def move(self) -> None:
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]
        if self.pos[0] <= 0 or self.pos[0] >= term.width() - self.text_width:
            self.dir[0] = -self.dir[0]
            self.pos[0] = 0 if self.pos[0] <= 0 else term.width() - self.text_width
        if self.pos[1] <= 0 or self.pos[1] >= term.height() - 1:
            self.dir[1] = -self.dir[1]
            self.pos[1] = 0 if self.pos[1] <= 0 else term.height() - 1
        term.goto(*self.last_pos)
        term.fg('reset')
        term.bg('reset')
        sys.stdout.write(self.blank)
        sys.stdout.flush()
        term.goto(*self.pos)
        term.fg(self.color[0], bright=self.bright)
        term.bg(self.color[1])
        sys.stdout.write(self.text)
        sys.stdout.flush()
        self.last_pos = self.pos.copy()
