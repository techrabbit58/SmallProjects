import random

import httpx

from . import constants as const, visuals


def download_random_maze() -> httpx.Response:
    maze_url = const.MAZE_URL
    maze = httpx.get(f"{maze_url}/maze{random.choice(('65x11', '25x25'))}s{random.randint(1, 100)}.txt")
    return maze


def main() -> None:
    # maze = download_random_maze()
    # if maze.status_code != httpx.codes.OK:
    #     print(f"Download of maze {maze.url} failed with reason: {maze.reason_phrase}")
    #     return
    # print(f"{maze.text}")
    picture = visuals.ALL_OPEN
    for ovl in list("CEF"):
        visuals.paste(overlay=visuals.CLOSED[ovl], base=picture)
    print(picture)


main()
