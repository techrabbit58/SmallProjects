from . import control


def main() -> None:
    game = control.Game()
    game.cmdloop()


try:
    main()
except KeyboardInterrupt:
    pass
