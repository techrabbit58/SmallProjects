import random

import httpx

MAZE_URL = "https://invpy.com/mazes"


def get_random_maze() -> httpx.Response:
    maze = httpx.get(f"{MAZE_URL}/maze{random.choice(('65x11', '25x25'))}s{random.randint(1, 100)}.txt")
    return maze


def main() -> None:
    maze = get_random_maze()
    if maze.status_code != httpx.codes.OK:
        print(f"Download of maze {maze.url} failed with reason: {maze.reason_phrase}")
        return
    print(f"{maze.text}")


main()
