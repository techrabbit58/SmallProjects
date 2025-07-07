import textwrap
from pathlib import Path


def intro() -> None:
    print(textwrap.dedent("""
    Maze Runner 2D, by Al Sweigart (al@inventwithpython.com)
      *** refactored version ***
    """))


class Maze:
    def __init__(self) -> None:
        self.is_terminated_game = False

    def run(self) -> None:
        self.is_terminated_game = True

    def parse(self, maze_text: list[str]) -> None:
        print(maze_text)


def setup_dialog() -> Maze | None:
    while True:
        print("Enter the filename of a .maze file (or LIST or QUIT).")
        response = input("> ").strip()
        if not response:
            continue

        if "QUIT".startswith(response.upper()):
            print()
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
    print("Thank you for playing. Bye!\n")


def main():
    while True:
        intro()
        maze = setup_dialog()
        if maze is None:
            break
        maze.run()
        if maze.is_terminated_game:
            break
    finish()


main()
