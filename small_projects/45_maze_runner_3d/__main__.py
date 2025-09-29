import textwrap

from . import mazeloader
from . import visuals

GAME_NAME = "M a z e   R u n n e r   3 D"


def main() -> None:

    maze = None

    while True:
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
                return

            if answer[0] in {"A", "B"} and answer[1:].isnumeric():
                size = ("25x25", "65x11")[ord(answer[0]) - ord("A")]
                number = int(answer[1:])
                if 1 <= number <= 100:
                    raw_maze = mazeloader.download(size, number)
                    maze = mazeloader.parse(raw_maze)
                    is_terminated = True
            else:
                message = f"{answer} is not a valid command. Try again."

        while True:  # game loop
            visuals.clear_screen()
            print(f"{GAME_NAME}\n")

            print(f"Current maze: {maze.url}")
            print("Press Enter to continue, or (Q)uit...")
            answer = input("> ").upper().strip().split(maxsplit=1)

            if not answer:
                maze = None
                break

            answer = answer[0]
            if answer in {"Q", "QUIT"}:
                return


if __name__ == '__main__':
    main()
    print("\nThanks for playing.\n")
