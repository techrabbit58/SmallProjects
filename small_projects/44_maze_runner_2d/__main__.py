import textwrap
from pathlib import Path
from typing import TypeAlias

Place: TypeAlias = tuple[int, int] | None

# game symbols and .maze file symbols
WALL = "#"
EMPTY = " "
START = "S"
EXIT = "E"
PLAYER = "@"
BLOCK = chr(9617)
DOOR = "X"

direction = {
    "W": (0, -1),
    "A": (-1, 0),
    "S": (0, 1),
    "D": (1, 0),
}


def intro() -> None:
    print(textwrap.dedent("""
    Maze Runner 2D, by Al Sweigart (al@inventwithpython.com)
      *** refactored version ***
    """))


def ask_player_for_next_move() -> str:
    while True:
        print("                          W")
        print("Enter direction or QUIT: ASD   Q")
        move = input("> ").strip().upper()
        if "QUIT".startswith(move):
            move = "Q"
            break
        if move in {"W", "A", "S", "D"}:
            break
        print(f"'{move}' is not a valid command. Try again.")
        continue
    return move


class Maze:
    def __init__(self) -> None:
        self.is_terminated_game = False
        self.width = self.height = -1
        self.player: Place = None
        self.start: Place = None
        self.exit: Place = None
        self.walls: set[Place] = set()

    def run(self) -> None:
        while True:
            self.show()
            answer = ask_player_for_next_move()
            if answer == "Q":
                self.is_terminated_game = True
                break
            print(f"{direction[answer]=}")

    def show(self) -> None:
        print()
        for y in range(self.height):
            for x in range(self.width):
                place = x, y
                symbol = BLOCK if place in self.walls else EMPTY
                if place == self.player:
                    symbol = PLAYER
                if place == self.exit:
                    symbol = DOOR
                print(symbol, end="")
            print()
        print()

    def parse(self, maze_text: list[str]) -> None:
        self.height = len(maze_text)
        self.width = len(maze_text[0])

        error = False

        for y, line in enumerate(maze_text):
            if len(line) != self.width:
                print(f"Line {y + 1} is too {'long' if len(line) > self.width else 'short'}.")
                break
            for x, symbol in enumerate(line):
                if symbol not in {WALL, EMPTY, START, EXIT}:
                    print(f"Bad symbol '{symbol}' in line {y + 1} at column {x + 1}.")
                    error = True
                    break
                if y in (0, self.height - 1) and symbol != WALL:
                    print(f"Line {y + 1} must be all walls, but column {y + 1} is not.")
                    error = True
                    break
                if x in (0, self.width - 1) and symbol != WALL:
                    print(f"Line {y + 1} must start or end with a wall. Column {x + 1} is not a wall.")
                    error = True
                    break
                if (self.start and symbol == START) or (self.exit and symbol == EXIT):
                    print(f"'{symbol}' at line {y + 1}, column {x + 1} is a duplicate.")
                    error = True
                    break
                if symbol == WALL:
                    self.walls.add((x, y))
                    continue
                if symbol == START:
                    self.start = x, y
                    continue
                if symbol == EXIT:
                    self.exit = x, y
                    continue
        else:  # The .maze file could be parsed without error.
            if not error and self.start is None:
                print("START is missing.")
            if not error and self.exit is None:
                print("EXIT is missing.")
            if not error and self.start is not None and self.exit is not None:
                self.player = self.start

        self.is_terminated_game = error


def setup_dialog() -> Maze | None:
    while True:
        print("Enter the filename of a .maze file (or LIST or QUIT).")
        response = input("> ").strip()
        if not response:
            continue

        if "QUIT".startswith(response.upper()):
            return None

        if "LIST".startswith(response.upper()):
            catalog = list(Path().glob("*.maze"))
            if len(catalog) == 0:
                print("No .maze files.")
                print()
                return None
            print("All .maze files in the current directory:\n")
            for file in catalog:
                print(f"   {file.name}")
            print()
            continue

        # At this point, the response shall be treated as a filename.
        maze_file = Path(adjust_filename(response))
        if not maze_file.exists():
            print(f"The file '{maze_file.name}' does not exist. Try again.")
            continue

        # At this point we know, the .maze file exists and can now be loaded.
        return make_maze(maze_file)


def adjust_filename(response):
    if not response.lower().endswith(".maze"):
        response += ".maze"
    return response


def make_maze(maze_file) -> Maze:
    maze = Maze()
    with maze_file.open() as fd:
        maze.parse(fd.read().strip().split("\n"))
    return maze


def finish() -> None:
    print("\nThank you for playing. Bye!\n")


def main():
    intro()

    while True:
        maze = setup_dialog()
        if maze is None:  # THe player did quit from the setup dialog.
            break
        if maze.is_terminated_game:  # The maze parser found an error in the .maze file.
            print("The .maze file has errors and cannot be processed. Try another.")
            continue
        maze.run()
        if maze.is_terminated_game:  # The player did quit from the game.
            break

    finish()


main()
