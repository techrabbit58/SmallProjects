import random
import textwrap
import time
from cmd import Cmd
from typing import TypeAlias

from .interaction import intro, ask_player
from .setup import (
    PLACES,
    ENTER,
    get_end_time,
    SUSPECTS,
    ITEMS,
    CULPRIT,
    MAX_ACCUSATIONS,
    LONGEST_PLACE_NAME_LENGTH,
    COMMANDS,
)

Minutes: TypeAlias = int
Seconds: TypeAlias = int


# noinspection PyPep8Naming
class App(Cmd):
    prompt = "> "

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_place = random.choice(PLACES)
        self.visited_places = {}  # place -> (list of suspects, list of items)
        self.known_suspects_and_items = set()
        self.accused_suspects = set()  # Accused suspects won't offer clues.
        self.accusations_left = MAX_ACCUSATIONS
        self.end_time = get_end_time()

    def preloop(self) -> None:
        self.do_HELP()
        self.do_EXPLORE()
        self.prompt = self.make_prompt()
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
        if result := self.is_game_over:
            print(result)
            stop = True
        if not stop:
            self.prompt = self.make_prompt()
        return super().postcmd(stop, line)

    def make_prompt(self) -> str:
        minutes_left, seconds_left = self.remaining_period
        accusations_left = self.accusations_left
        s = "" if accusations_left == 1 else "s"
        return "\n".join((
            f"\nTime left: {minutes_left} minutes, {seconds_left} seconds",
            f"You have {accusations_left} accusation{s} left.",
            "> ",
        ))

    @property
    def is_game_over(self) -> str | None:
        """Return a (truthy) notification string if ganme is over, or (falsish) None."""
        result = []
        is_lost = False
        if self.accusations_left == 0:
            is_lost = True
            result.append("You have accused too many innocent people.")
        if self.end_time < time.time():
            is_lost = True
            result.append("You have run out of time.")
        if is_lost:
            culprit_index = SUSPECTS.index(CULPRIT)
            place = PLACES[culprit_index]
            item = ITEMS[culprit_index]
            result.append(f"The true culprit stood at the {place} with the {item}.")
            result.append("Several lives now bore the cost of misjudgment")
            result.append(f"— while {CULPRIT} walks free.")
            return "\n" + "\n".join(textwrap.wrap(" ".join(result)))
        else:
            return None

    def postloop(self) -> None:
        print("\nThank you for playing.\n")
        super().postloop()

    def emptyline(self) -> None:
        """Do nothing."""

    def default(self, line: str) -> None:
        parts = line.upper().strip().split()
        head, tail = parts[0], parts[1:]
        command = (list(filter(lambda s: s[0].startswith(head), COMMANDS)) or [["missing", "", ""]])[0]
        if command[0] == "missing":
            print(f"\nI do not know how to do that: \"{line}\"")
        else:
            print(f"\nThe command \"{command[0]}\" is not yet implemented.")

    @staticmethod
    def do_QUIT(_: str) -> bool:
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

    def do_PLACES(self, _: str) -> None:
        print("You should investigate these places carefully:\n")
        for place in sorted(PLACES):
            info = ""
            if place in self.visited_places:
                info = [p.title() for p in self.visited_places[place]]
            print(f"   {place:<{LONGEST_PLACE_NAME_LENGTH + 3}}{info}")

    def do_GOTO(self, a_place: str) -> None:
        choices = list(filter(lambda s: s.startswith(a_place), PLACES))
        match len(choices):
            case 0:
                print("I do not know where to go. Be more accurate, please.")
            case 1:
                next_place = choices[0]
                print(self.change_location(next_place))
                self.do_EXPLORE()
            case _:
                print(
                    f"Your current choice is ambigous: {' or '.join(choices)}?\n"
                    "Be more accurate, please."
                )

    def change_location(self, next_place: str) -> str:
        if next_place == self.current_place:
            notification = "\nOops! You are already there. No change."
        else:
            notification = "\nYou take a TAXI to go to the next place ..."
        self.current_place = next_place
        return notification

    def do_EXPLORE(self, _: str = None) -> None:
        print(f"\nYou are at the {self.current_place}.")
        local_suspect, local_item = self.suspect_and_item
        print(f"{local_suspect} with the {local_item} is here.")
        self.known_suspects_and_items.add(local_suspect)
        self.known_suspects_and_items.add(local_item)
        self.visited_places[self.current_place] = local_suspect.lower(), local_item.lower()

    def do_JACCUSE(self, a_suspect: str) -> None:
        self.accusations_left -= 1

    @property
    def suspect_and_item(self) -> tuple[str, str]:
        index = PLACES.index(self.current_place)
        local_suspect = SUSPECTS[index]
        local_item = ITEMS[index]
        return local_suspect, local_item

    @property
    def remaining_period(self) -> tuple[Minutes, Seconds]:
        now = time.time()
        time_left = int(self.end_time - now)
        minutes_left, seconds_left = time_left // 60, time_left % 60
        return minutes_left, seconds_left


def main() -> None:
    print(intro())
    ask_player("Press Enter when you are ready.", ENTER)
    print()
    app = App()
    app.cmdloop()


try:
    main()
except KeyboardInterrupt:
    pass
