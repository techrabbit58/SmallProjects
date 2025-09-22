import colorama

from . import control


def main() -> None:
    game = control.Game()
    game.cmdloop()


try:
    colorama.just_fix_windows_console()
    main()
except KeyboardInterrupt:
    pass
finally:
    colorama.deinit()
