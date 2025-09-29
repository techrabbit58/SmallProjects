from . import interactive
from . import visual


def main() -> None:
    n = 0

    while True:
        print(visual.soroban_image(n))
        result = interactive.ask_player(
            "Enter a natural number to add or subtract from the soroban.\n"
            "Enter '0' (zero) to reset the soroban, or 'quit'."
        )

        if result is None:
            print("This is not a valid option. Try again.")
            continue

        if result[0] == 'quit':
            break

        if isinstance(result[0], int):
            n = 0 if result[0] == 0 else (10_000_000_000 + n + result[0]) % 10_000_000_000


if __name__ == '__main__':
    main()
