import random
import time
from cmd import Cmd
from typing import TypeAlias

from .interaction import intro, ask_player
from .setup import PLACES, ENTER, get_end_time

Minutes: TypeAlias = int
Seconds: TypeAlias = int

COMMANDS = [
    command.strip().upper().split(", ") for command in """
    HELP, , Know the opportunities
    QUIT, , Give up
    GOTO, a place, Visit another crime scene
    ITEM, an item, Ask the local suspect for a clue about an item
    SUSPECT, a suspect, Ask the local suspect for a clue about another suspect
    CULPRIT, , Ask the local suspect if she knows the culprit
    PLACES, , Review your observations at all possible crime scenes
    EXPLORE, , Review the current place's facts
    ACCUSE, a suspect, You accuse a possible culprit. Are you sure?
    """.strip().split("\n")
]


# noinspection PyPep8Naming
class App(Cmd):
    prompt = "> "

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_place = random.choice(PLACES)
        self.end_time = get_end_time()

    def preloop(self) -> None:
        self.do_HELP()
        self.do_EXPLORE()
        minutes_left, seconds_left = get_remaining_period(self.end_time)
        print(f"\nTime left: {minutes_left} minutes, {seconds_left} seconds")
        super().preloop()

    def precmd(self, line: str) -> str:
        parts = line.upper().strip().split()
        if not parts:
            return line
        head, tail = parts[0], parts[1:]
        command = (list(filter(lambda s: s[0].startswith(head), COMMANDS)) or [["missing", "", ""]])[0]
        if command[0] == "missing":
            return line
        response = f"{command[0]} {' '.join(tail)}"
        return super().precmd(response)

    def postcmd(self, stop: bool, line: str) -> bool:
        if not stop:
            minutes_left, seconds_left = get_remaining_period(self.end_time)
            print(f"\nTime left: {minutes_left} minutes, {seconds_left} seconds")
        return super().postcmd(stop, line)

    def emptyline(self) -> None:
        """Do nothing."""

    @staticmethod
    def do_QUIT(_: str) -> bool:
        print("\nThank you for playing.\n")
        return True

    @staticmethod
    def do_EOF(_: str) -> bool:
        return True

    @staticmethod
    def do_HELP(_: str = None) -> None:
        print("You can use these commands:\n")
        actions = []
        field_length = 0
        for keyword, arg, advice in COMMANDS:
            actions.append((f"{keyword} {arg.lower()}", advice))
            field_length = max(field_length, len(actions[-1][0]))
        for action, advice in actions:
            print(f"   {action:<{field_length + 3}}{advice.capitalize()}")

    @staticmethod
    def do_PLACES(_: str) -> None:
        print("You should investigate these places carefully:\n")
        for place in sorted(PLACES):
            print(f"   {place}")

    def do_GOTO(self, a_place: str) -> None:
        choices = list(filter(lambda s: s.startswith(a_place), PLACES))
        if len(choices) == 0:
            print("I do not know where to go. Be more accurate, please.")
            return
        if len(choices) > 1:
            print(f"Your current choice is ambigous: {' or '.join(choices)}?")
            return
        next_place = choices[0]
        if next_place == self.current_place:
            print("\nOops! You are already there. No change.")
        else:
            print("\nYou take a TAXI to go to the next place ...")
        self.current_place = next_place
        self.do_EXPLORE()

    def do_EXPLORE(self, _: str = None) -> None:
        print(f"\nYou are at the {self.current_place}.")


def main() -> None:
    print(intro())
    ask_player("Press Enter when you are ready.", ENTER)
    print()
    app = App()
    app.cmdloop()


def get_remaining_period(end_time: float) -> tuple[Minutes, Seconds]:
    now = time.time()
    time_left = int(end_time - now)
    minutes_left, seconds_left = time_left // 60, time_left % 60
    return minutes_left, seconds_left


try:
    main()
except KeyboardInterrupt:
    pass
