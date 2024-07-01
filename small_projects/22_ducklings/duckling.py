import enum
import random


class Direction(enum.Enum):
    LEFT = 101
    RIGHT = 102


class Body(enum.Enum):
    CHUBBY = 11
    VERY_CHUBBY = 12


class Beak(enum.Enum):
    OPEN = ('>', '<')
    CLOSED = ('=', '=')

    def __init__(self, left_beak: str, right_beak: str) -> None:
        self.left = left_beak
        self.right = right_beak


class Wing(enum.Enum):
    OUT = ('>', '<')
    DOWN = ('v', 'v')
    UP = ('^', '^')

    def __init__(self, left_wing: str, right_wing: str) -> None:
        self.left = left_wing
        self.right = right_wing


class Eyes(enum.Enum):
    BEADY = ('"', '"')
    WIDE = ("''", "''")
    HAPPY = ('^^', '^^')
    ALOOF = ('´´', '``')

    def __init__(self, left_eyes: str, right_eyes: str) -> None:
        self.left = left_eyes
        self.right = right_eyes


class Duckling:
    def __init__(self) -> None:
        self.direction = random.choice(list(Direction))
        self.body = random.choice(list(Body))
        self.beak = random.choice(list(Beak))
        self.wing = random.choice(list(Wing))
        self.eyes = Eyes.BEADY if self.body == Body.CHUBBY else random.choice(list(Eyes))
        self.next_part = self.get_head

    def get_head(self) -> str:
        line = []

        if self.direction is Direction.LEFT:
            line.append(self.beak.left)
            line.append(self.eyes.left)
            if self.eyes is Eyes.BEADY and self.body is Body.VERY_CHUBBY:
                line.append(' ')
            line.append(') ')

        if self.direction is Direction.RIGHT:
            line.append(' (')
            if self.eyes is Eyes.BEADY and self.body is Body.VERY_CHUBBY:
                line.append(' ')
            line.append(self.eyes.right)
            line.append(self.beak.right)

        if self.body is Body.CHUBBY:
            line.append(' ')

        self.next_part = self.get_body
        return ''.join(line)

    def get_body(self) -> str:
        line = ['(']

        if self.direction is Direction.LEFT:
            line.append(' ' if self.body is Body.CHUBBY else '  ')
            line.append(self.wing.left)

        if self.direction is Direction.RIGHT:
            line.append(self.wing.right)
            line.append(' ' if self.body is Body.CHUBBY else '  ')

        line.append(')' if self.body is Body.VERY_CHUBBY else ') ')

        self.next_part = self.get_feet
        return ''.join(line)

    def get_feet(self) -> str:
        self.next_part = None
        return ' ^ ^ ' if self.body is Body.VERY_CHUBBY else ' ^^  '


if __name__ == '__main__':
    duckling = Duckling()
    while duckling.next_part is not None:
        print(f'_{duckling.next_part()}_')
