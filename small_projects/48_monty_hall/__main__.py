from colterm import term


def main() -> None:
    term.clear()
    term.fg('white')
    print("Let's make a deal!")
    term.fg('reset')


if __name__ == '__main__':
    main()
