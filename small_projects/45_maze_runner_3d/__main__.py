import random
from dataclasses import dataclass

import httpx

from . import constants as const, visuals


@dataclass(frozen=True, kw_only=True)
class Maze:
    url: str
    width: int
    height: int
    start:  tuple[int, int]  # (x, y)
    end: tuple[int, int]  # (x, y)
    walls: set[tuple[int, int]]


def download_maze(size: str, number: int) -> httpx.Response:
    maze_url = const.MAZE_URL
    maze = httpx.get(f"{maze_url}/maze{size}s{number}.txt")
    return maze


def parse_maze(download: httpx.Response) -> Maze:
    walls = set()
    url = str(download.url)
    start = way_out = None
    lines = download.text.splitlines()
    height = len(lines)
    width = len(lines[0])
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol == const.WALL:
                walls.add((x, y))
            elif symbol == const.EMPTY:
                continue
            elif symbol == const.START:
                start = x, y
            elif symbol == const.WAY_OUT:
                way_out = x, y
            else:
                raise ValueError(f"Unknown symbol {symbol}")
    if start is None:
        raise ValueError("Start position not found")
    if way_out is None:
        raise ValueError("Exit position not found")
    return Maze(walls=walls, url=url, height=height, width=width, start=start, end=way_out)


def main() -> None:

    print(visuals.ALL_OPEN + visuals.CLOSED["D"] + visuals.CLOSED["B"])

    raw_maze = download_maze(random.choice(('65x11', '25x25')), random.randint(1, 100))
    if raw_maze.status_code != httpx.codes.OK:
        raise IOError(f"Download of maze {raw_maze.url} failed with reason: {raw_maze.reason_phrase}")

    maze = parse_maze(raw_maze)

    print(f"Current maze: {maze.url} ({maze.width}x{maze.height})")
    print(maze)


if __name__ == '__main__':
    main()
