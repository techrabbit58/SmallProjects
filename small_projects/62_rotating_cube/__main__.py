import math
import os
import sys
import time
from collections.abc import Iterable
from dataclasses import dataclass

PAUSE_AMOUNT = 0.1  # pause length (seconds)
WIDTH, HEIGHT = 80, 24
SCALEX = (WIDTH - 4) // 8
SCALEY = 2 * ((HEIGHT - 4) // 8)  # text cells are twice as tall as they are wide
TRANSLATEX = (WIDTH - 4) // 2
TRANSLATEY = (HEIGHT - 4) // 2

LINE_CHAR = chr(9608)
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
    Vector(-1, -1, -1),
    Vector(1, -1, -1),
    Vector(-1, -1, 1),
    Vector(1, -1, 1),
    Vector(-1, 1, -1),
    Vector(1, 1, -1),
    Vector(-1, 1, 1),
    Vector(1, 1, 1),
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


def get_points_on_line(ax: int, ay: int, bx: int, by: int) -> list[tuple[int, int]]:
    """
    Find all pixels of a line from point A to point B on the screen by applying
    Bresenham's algorithm.
    :param ax: The x coordinate of point A
    :param ay: The y coordinate of point A
    :param bx: The x coordinate of point B
    :param by: The y coordinate of point B
    :return: A list of 2D points (a.k.a. pixel locations)
    """
    points: list[tuple[int, int]] = []
    
    if (ax == bx and ay == by + 1) or (ay == by and ax == bx + 1):
        """Trivial result, if both points are direct neighbours."""
        return [(ax, ay), (bx, by)]
    
    is_steep = abs(by - ay) > abs(bx - ax)  # True, if the positive or negative slope is .gt. 45 degrees
    if is_steep:  # Adjust slope because Bresenham's does not work for steep lines
        ax, ay = ay, ax
        bx, by = by, bx
        
    is_reversed = ax > bx  # True if the line goes right to left
    if is_reversed:
        ax, bx = bx, ax
        ay, by = by, ay
    
    delta_x = bx - ax
    delta_y = abs(by - ay)
    extra_y = int(delta_x / 2)
    current_y = by if is_reversed else ay
    y_direction = 1 if ay < by else -1
    x_range = range(bx, ax - 1, -1) if is_reversed else range(ax, bx + 1)
    
    for current_x in x_range:
        points.append((current_x, current_y) if is_steep else (current_y, current_x))
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
        print()
    print("Press Ctrl-C to quit.", end="", flush=True)


def main() -> None:
    rotation = Vector()
    delta = Vector(X_ROTATE_SPEED, Y_ROTATE_SPEED, Z_ROTATE_SPEED)
    rotated_corners: list[Vector | None] = [None] * 8

    try:
        while True:
            rotation += delta

            for i, corner in enumerate(CUBE_CORNERS):
                rotated_corners[i] = rotate_point(corner, rotation)

            cube_points = []
            for a, b in zip((0, 1, 3, 2, 0, 1, 2, 3, 4, 5, 7, 6), (1, 3, 2, 0, 4, 5, 6, 7, 5, 7, 6, 4)):
                ax, ay = adjust_point(rotated_corners[a])
                bx, by = adjust_point(rotated_corners[b])
                points_on_line = get_points_on_line(ax, ay, bx, by)
                cube_points.extend(points_on_line)
            cube_points = tuple(frozenset(cube_points))  # remove duplicate points

            display_on_screen(cube_points)

            time.sleep(PAUSE_AMOUNT)
            os.system("cls" if sys.platform == "win32" else "clear")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
