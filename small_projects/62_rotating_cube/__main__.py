import math
import os
import sys
import time
from collections.abc import Iterable
from dataclasses import dataclass

PAUSE = 0.1  # pause length (seconds)
WIDTH, HEIGHT = 80, 24
SCALEX = (WIDTH - 4) // 8
SCALEY = 2 * ((HEIGHT - 4) // 8)  # text cells are twice as tall as they are wide
TRANSLATEX = (WIDTH - 4) // 2
TRANSLATEY = (HEIGHT - 4) // 2

LINE_CHAR = chr(8226)
BLANK = " "

X_ROTATE_SPEED = 0.03
Y_ROTATE_SPEED = 0.08
Z_ROTATE_SPEED = 0.13


@dataclass
class Vector:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __iadd__(self, other: "Vector") -> "Vector":
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self


"""
       0------1
      /|     /|
     2------3 |
     | 4----|-3
     |/     |/
     6------7
"""
CUBE_CORNERS = [
    Vector(-1, -1, -1),     # 0
    Vector(1, -1, -1),      # 1
    Vector(-1, -1, 1),      # 2
    Vector(1, -1, 1),       # 3
    Vector(-1, 1, -1),      # 4
    Vector(1, 1, -1),       # 5
    Vector(-1, 1, 1),       # 6
    Vector(1, 1, 1),        # 7
]


def rotate_point(corner: Vector, rotation: Vector) -> Vector:
    rotated = Vector(
        corner.x,
        corner.y * math.cos(rotation.x) - corner.z * math.sin(rotation.x),
        corner.y * math.sin(rotation.x) + corner.z * math.cos(rotation.x)
    )
    rotated = Vector(
        rotated.z * math.sin(rotation.y) + rotated.x * math.cos(rotation.y),
        rotated.y,
        rotated.z * math.cos(rotation.y) - rotated.x * math.sin(rotation.y),
    )
    rotated = Vector(
        rotated.x * math.cos(rotation.z) - rotated.y * math.sin(rotation.z),
        rotated.x * math.sin(rotation.z) + rotated.y * math.cos(rotation.z),
        rotated.z,
    )
    return rotated


def adjust_point(point: Vector) -> tuple[int, int]:
    """Map a 3D model point to a 2D screen location (means: to a pixel position)."""
    return int(point.x * SCALEX + TRANSLATEX), int(point.y * SCALEY + TRANSLATEY)


def get_points_on_line(x1: int, y1: int, x2: int, y2: int) -> set[tuple[int, int]]:
    """
    Find all pixels of a line from point A to point B on the screen by applying
    Bresenham's algorithm.
    :param x1: The x coordinate of point A
    :param y1: The y coordinate of point A
    :param x2: The x coordinate of point B
    :param y2: The y coordinate of point B
    :return: A list of 2D points (a.k.a. pixel locations)
    """
    points: set[tuple[int, int]] = {(x1, y1), (x2, y2)}

    if (x1 == x2 and y1 == y2 + 1) or (y1 == y2 and x1 == x2 + 1):
        """Has the trivial result, if both points are direct neighbours."""
        return points

    is_steep = abs(y2 - y1) > abs(x2 - x1)  # True, if the positive or negative slope is .gt. 45 degrees
    if is_steep:  # Adjust slope because Bresenham's does not work for steep lines
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    is_reversed = x1 > x2  # True if the line goes right to left
    if is_reversed:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    delta_x = x2 - x1
    delta_y = abs(y2 - y1)
    extra_y = int(delta_x / 2)
    current_y = y2 if is_reversed else y1
    y_direction = 1 if y1 < y2 else -1
    x_range = range(x2, x1 - 1, -1) if is_reversed else range(x1, x2 + 1)

    for current_x in x_range:
        points.add((current_y, current_x) if is_steep else (current_x, current_y))
        extra_y -= delta_y
        if is_reversed and extra_y <= 0:
            current_y -= y_direction
            extra_y += delta_x
        if not is_reversed and extra_y < 0:
            current_y += y_direction
            extra_y += delta_x

    return points


def display_on_screen(cube_points: Iterable[tuple[int, int]]) -> None:
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) in cube_points:
                print(LINE_CHAR, end="", flush=False)
            else:
                print(BLANK, end="", flush=False)
        print(flush=False)
    print("Press Ctrl-C to quit.", end="", flush=True)


def main() -> None:
    rotation = Vector()
    delta = Vector(X_ROTATE_SPEED, Y_ROTATE_SPEED, Z_ROTATE_SPEED)
    rotated_corners: list[Vector | None] = [None] * 8
    edges = tuple(zip((0, 1, 3, 2, 0, 1, 2, 3, 4, 5, 7, 6), (1, 3, 2, 0, 4, 5, 6, 7, 5, 7, 6, 4)))

    try:
        while True:
            rotation += delta

            for i, corner in enumerate(CUBE_CORNERS):
                rotated_corners[i] = rotate_point(corner, rotation)

            cube_points = set()
            for a, b in edges:
                point_a = adjust_point(rotated_corners[a])
                point_b = adjust_point(rotated_corners[b])
                points_on_line = get_points_on_line(*point_a, *point_b)
                cube_points.update(points_on_line)

            display_on_screen(cube_points)

            time.sleep(PAUSE)
            os.system("cls" if sys.platform == "win32" else "clear")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
