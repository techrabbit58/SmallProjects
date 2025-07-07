import textwrap


def intro() -> None:
    print(textwrap.dedent("""
    Maze Runner 2D, by Al Sweigart (al@inventwithpython.com)
      *** refactored version ***
    """))


class Maze:
    def __init__(self) -> None:
        self.is_terminated_game = False
    def run(self) -> None:
        print(f"Hello, {self.__class__.__name__}!")
        self.is_terminated_game = True


def setup_dialog() -> Maze:
    maze = Maze()
    return maze


def main():
    while True:
        intro()
        maze = setup_dialog()
        if maze.is_terminated_game:
            break
        maze.run()
        if maze.is_terminated_game:
            break


main()
