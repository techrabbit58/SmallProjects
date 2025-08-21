import random
from typing import TypeAlias

from . import screen
from .config import WHITE, BLACK, MIN_X_INCREASE, MAX_X_INCREASE, MIN_Y_INCREASE, MAX_Y_INCREASE, COLORS

Point: TypeAlias = tuple[int, int]  # (x, y)

_canvas: dict[Point, str] = dict()
_number_of_segments_to_delete: int = 0


def erase() -> None:
    global _canvas, _number_of_segments_to_delete

    _canvas = {}
    for y in range(screen.height):
        for x in range(screen.width):
            _canvas[x, y] = WHITE

    _number_of_segments_to_delete = 0
    _number_of_rectangles_to_paint = 0


def generate_vertical_lines() -> None:
    global _number_of_segments_to_delete

    x = random.randint(MIN_X_INCREASE, MAX_X_INCREASE)
    while x < screen.width - MIN_X_INCREASE:
        _number_of_segments_to_delete += 1
        for y in range(screen.height):
            _canvas[x, y] = BLACK
        x += random.randint(MIN_X_INCREASE, MAX_X_INCREASE)


def generate_horizontal_lines() -> None:
    global _number_of_segments_to_delete

    y = random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)
    while y < screen.height - MIN_Y_INCREASE:
        _number_of_segments_to_delete += 1
        for x in range(screen.width):
            _canvas[x, y] = BLACK
        y += random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)


def get_number_of_segments_to_delete() -> int:
    return int(_number_of_segments_to_delete * 1.5)


def get_number_of_rectangles_to_paint() -> int:
    return _number_of_segments_to_delete - 3


def get_line_orientation(x: int, y: int) -> str:
    if _canvas[x - 1, y] == _canvas[x + 1, y] == WHITE:
        return "vertical"
    elif _canvas[x, y - 1] == _canvas[x, y + 1] == WHITE:
        return "horizontal"
    else:
        return "intersection"


def delete_some_lines() -> None:
    for _ in range(get_number_of_segments_to_delete()):
        points_to_delete = None

        while True:  # randomly select one deletable line
            start_x = random.randint(1, screen.width - 2)
            start_y = random.randint(1, screen.height - 2)

            if _canvas[start_x, start_y] == WHITE:  # not on a line
                continue

            orientation = get_line_orientation(start_x, start_y)
            if orientation == "intersection":
                continue

            points_to_delete = {(start_x, start_y)}
            can_delete_segment = True

            match orientation:  # to find all points of the segment between intersections
                case "vertical":
                    for dy in (-1, 1):
                        y = start_y
                        while 0 < y < screen.height - 1:
                            y += dy
                            if _canvas[start_x - 1, y] == _canvas[start_x + 1, y] == BLACK:  # cross intersection
                                break
                            elif ((_canvas[start_x - 1, y] == BLACK and _canvas[start_x + 1, y] == WHITE)
                                or (_canvas[start_x - 1, y] == WHITE and _canvas[start_x + 1, y] == BLACK)):
                                # T-intersection: cannot remove this segment
                                can_delete_segment = False
                                break
                            else:
                                points_to_delete.add((start_x, y))
                case "horizontal":
                    for dx in (-1, 1):
                        x = start_x
                        while 0 < x < screen.width - 1:
                            x += dx
                            if _canvas[x, start_y - 1] == _canvas[x, start_y + 1] == BLACK:  # cross intersection
                                break
                            elif ((_canvas[x, start_y - 1] == BLACK and _canvas[x, start_y + 1] == WHITE)
                                or (_canvas[x, start_y - 1] == WHITE and _canvas[x, start_y + 1] == BLACK)):
                                # T-intersection: cannot remove this segment
                                can_delete_segment = False
                                break
                            else:
                                points_to_delete.add((x, start_y))

            if can_delete_segment:
                break

        for x, y in points_to_delete:
            _canvas[x, y] = WHITE


def add_borders() -> None:
    for y in range(screen.height):
        _canvas[0, y] = BLACK
        _canvas[screen.width - 1, y] = BLACK
    for x in range(screen.width):
        _canvas[x, 0] = BLACK
        _canvas[x, screen.height - 1] = BLACK


def hit_next_rectangle_for_painting() -> Point:
    while True:
        x = random.randint(1, screen.width - 2)
        y = random.randint(1, screen.height - 2)

        if _canvas[x, y] != WHITE:  # hit a line, or this rectangle is already painted
            continue
        else:  # this is a so far unpainted rectangle
            break

    return x, y


def paint_rectangles() -> None:
    for _ in range(get_number_of_rectangles_to_paint()):
        color = random.choice(COLORS)
        points = {hit_next_rectangle_for_painting()}

        while len(points) > 0:
            x, y = points.pop()
            _canvas[x, y] = color
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if _canvas.get((x + dx, y + dy)) == WHITE:
                    points.add((x + dx, y + dy))


def draw() -> None:
    screen.clear()
    for y in range(screen.height):
        for x in range(screen.width):
            screen.draw(x, y, _canvas[x, y])
        screen.flush_line()
