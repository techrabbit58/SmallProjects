import os
import sys
import textwrap
from cmd import Cmd

MAX_TELEPORTS = 2


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)


class App(Cmd):
    prompt = "> "
    title = "H u n g r y   R o b o t s"

    intro = textwrap.dedent(f"""
    {title}

    You are trapped in a maze with hungry robots. The robots are badly
    programmed and run to you even if eventually blocked by walls. You
    must trick the robots to crash into each other or into dead robots,
    but avoid to be caught by a robot. Your personal teleporter device
    lets you magically jump to arbitrary free spaces inside the maze,
    but has battery capacity only for up to {MAX_TELEPORTS} jumps. You
    and the robots can always go up, down, left, right or diagonal. You
    can slip throgh wall corners when going diagonally. Keep in mind,
    the robots can do the same!

    Press Enter to begin (or QUIT).
    """)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.precmd = self.pre_first_command

    def preloop(self) -> None:
        clear_screen()

    def postloop(self) -> None:
        print("\nThanks for playing.\n")

    def pre_first_command(self, line: str) -> str:
        self.precmd = self.pre_regular_command
        command = line.strip().upper()
        if command and command.split()[0] in {"EOF", "QUIT"}:
            return command
        return ""

    @staticmethod
    def pre_regular_command(line: str):
        return line.upper()

    def postcmd(self, stop: bool, line: str) -> bool:
        if stop: return True
        clear_screen()
        print(f"\n{self.title}\n")
        return False

    def emptyline(self):
        return False

    @staticmethod
    def do_EOF(_: str) -> bool:
        return True

    @staticmethod
    def do_QUIT(_: str) -> bool:
        return True


def main() -> None:
    app = App()
    app.cmdloop()


try:
    main()
except KeyboardInterrupt:
    pass
