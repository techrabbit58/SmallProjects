import textwrap
from dataclasses import dataclass

from . import mazeloader
from . import visuals
from . import constants as const

GAME_NAME = "M a z e   R u n n e r   3 D"


def maze_loader_loop() -> mazeloader.Maze | None:
    maze = None
    message = None
    is_terminated = False

    while not (is_terminated or maze):  # choose another maze
        visuals.clear_screen()
        print(f"{GAME_NAME}\n")

        if message:
            print(message)
        print(textwrap.dedent("""
        Choose your next maze.

        Size:                   Identifier:
        (A) 25 x 25             choose a number
        (B) 65 x 11             between and including
                                1 and 100

        Enter something like A42 or B1 or A100 etc., or (Q)uit.
        """).strip())

        answer = input("> ").upper().strip().split(maxsplit=1)

        if not answer:
            message = None
            continue

        answer = answer[0]
        if answer in {"Q", "QUIT"}:
            return None

        if answer[0] in {"A", "B"} and answer[1:].isnumeric():
            size = ("25x25", "65x11")[ord(answer[0]) - ord("A")]
            number = int(answer[1:])
            if 1 <= number <= 100:
                raw_maze = mazeloader.download(size, number)
                maze = mazeloader.parse(raw_maze)
                is_terminated = True
        else:
            message = f"{answer} is not a valid command. Try again."

    return maze


@dataclass(kw_only=True)
class Player:
    place: tuple[int, int]  # (x, y)
    direction: str  # (N)orth, (E)ast, (S)outh, (E)ast


OFFSETS = {
    const.NORTH: (("A", (0, -2)), ("B", (-1, -1)), ("C", (0, -1)), ("D", (1, -1)), ("E", (-1, 0)), ("F", (1, 0))),
    const.SOUTH: (("A", (0, 2)), ("B", (1, 1)), ("C", (0, 1)), ("D", (-1, 1)), ("E", (1, 0)), ("F", (-1, 0))),
    const.EAST: (("A", (2, 0)), ("B", (1, -1)), ("C", (1, 0)), ("D", (1, 1)), ("E", (0, -1)), ("F", (0, 1))),
    const.WEST: (("A", (-2, 0)), ("B", (-1, 1)), ("C", (-1, 0)), ("D", (-1, -1)), ("E", (0, 1)), ("F", (0, -1))),
}


def make_picture(maze: mazeloader.Maze, player: Player) -> visuals.Picture:
    offesets = OFFSETS[player.direction]

    sections = {}
    for section, offset in offesets:
        (x, y), (dx, dy) = player.place, offset
        place = (x + dx, y + dy)
        sections[section] = const.WALL if place in maze.walls \
            else const.WAY_OUT if place == maze.end \
            else const.EMPTY

    picture = visuals.ALL_OPEN
    for section in "ABCDEF":
        if sections[section] == const.WALL:
            picture += visuals.CLOSED[section]
    for section in "CEF":
        if sections[section] == const.WAY_OUT:
            picture += visuals.CLOSED[section]

    return picture


def maze_runner_loop(maze: mazeloader.Maze) -> bool:
    player = Player(place=maze.start, direction=const.NORTH)

    while True:  # game loop
        visuals.clear_screen()
        print(f"{GAME_NAME}\n")

        print(f"Current maze: {maze.url}\n")
        picture = make_picture(maze, player)
        print(picture)

        print("Press Enter to continue or (R)estart maze or (Q)uit...")
        answer = input("> ").upper().strip().split(maxsplit=1)

        if not answer:
            continue

        answer = answer[0]
        if answer in {"Q", "QUIT"}:
            return False

        if answer in {"R", "RESTART"}:
            break

    return True


def main() -> None:
    while True:
        maze = maze_loader_loop()
        if not maze:  # player qants to quit
            break
        if not maze_runner_loop(maze):  # player wants to quit
            break


if __name__ == '__main__':
    main()
    print("\nThanks for playing.\n")
