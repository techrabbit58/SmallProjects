import colorama

from . import gameloop


def main() -> None:
    game = gameloop.Game()
    game.cmdloop()


try:
    colorama.just_fix_windows_console()
    main()
except KeyboardInterrupt:
    pass
finally:
    colorama.deinit()
