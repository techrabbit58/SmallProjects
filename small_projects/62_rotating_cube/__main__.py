import math
from dataclasses import dataclass

PAUSE_AMOUNT = 0.1  # pause length (seconds)
WIDTH, HEIGHT = 80, 24
SCALEX = (WIDTH - 4) // 8
SCALEY = 2 * ((HEIGHT - 4) // 8)  # text cells are twice as tall as they are wide
TRANSLATEX = (WIDTH - 4) // 2
TRANSLATEY = (HEIGHT - 4) // 2

LINE_CHAR = chr(9608)

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


def main() -> None:
    rotation = Vector()
    delta = Vector(X_ROTATE_SPEED, Y_ROTATE_SPEED, Z_ROTATE_SPEED)
    rotated_corners: list[Vector | None] = [None] * 8

    try:
        while True:
            rotation += delta
            for i, corner in enumerate(CUBE_CORNERS):
                rotated_corners[i] = rotate_point(corner, rotation)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
