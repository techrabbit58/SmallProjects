import colorama

from . import gameloop


def main() -> None:
    game = gameloop.Game()
    game.cmdloop()


if __name__ == '__main__':
    try:
        colorama.just_fix_windows_console()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        colorama.deinit()
