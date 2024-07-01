import random
import sys
import time
from typing import TypeAlias

Duckling: TypeAlias = list[str]

DUCKLING_HEIGHT = 3
DUCKLING_WIDTH = 6

PAUSE = 1 // 12  # seconds
DENSITY = 10  # percent


def get_one_duckling(n: int) -> Duckling:
    assert 0 <= n < 6
    ducklings = [
        '>" ) =^^)  (``=  ("= >")   ("=',
        '(  >)(  ^)(v  ) (^ ) ( >) (v )',
        ' ^ ^  ^ ^  ^ ^   ^^   ^^   ^^ ',
    ]
    return [ducklings[i][n * 5:(n + 1) * 5] for i in range(3)]


Canvas: TypeAlias = dict[tuple[int, int], str]


def can_place_duckling_at(origin_x: int, origin_y: int, canvas: Canvas) -> bool:
    for x, y in {
        (origin_x, origin_y),
        (origin_x + DUCKLING_WIDTH, origin_y),
        (origin_x + DUCKLING_WIDTH, origin_y + DUCKLING_HEIGHT),
        (origin_x, origin_y + DUCKLING_HEIGHT)
    }:
        if (y, x) in canvas:
            return False
    return True


def place_ducklings(canvas_width: int, canvas_height: int, ducklings: list[Duckling]) -> Canvas:
    canvas = {}

    for duckling in ducklings:
        while True:
            origin_x = random.randint(0, canvas_width - DUCKLING_HEIGHT - 1)
            origin_y = random.randint(0, canvas_height - DUCKLING_HEIGHT)
            if can_place_duckling_at(origin_x, origin_y, canvas):
                for dx in range(DUCKLING_WIDTH):
                    for dy in range(DUCKLING_HEIGHT):
                        canvas[(origin_y + dy, origin_x + dx)] = duckling[dy][dx]
                break

    return canvas


def main():
    for n in range(6):
        print('\n'.join(get_one_duckling(n)))
        time.sleep(3)


try:
    main()
except KeyboardInterrupt:
    sys.exit()
