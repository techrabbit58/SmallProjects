import os
import sys
import textwrap
from cmd import Cmd

from . import world


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)


class Game(Cmd):
    prompt = "> "
    title = "H u n g r y   R o b o t s"
    intro = textwrap.dedent(f"""
    \x1b[2J{title}

    You are trapped in a maze with hungry robots. The robots are badly
    programmed and run to you even if eventually blocked by walls. You
    must trick the robots to crash into each other or into dead robots,
    but avoid to be caught by a robot. Your personal teleporter device
    lets you magically jump to arbitrary free spaces inside the maze,
    but has battery capacity only for up to {world.get_num_teleports()} jumps. You and the robots
    can always go up, down, left, right or diagonal. You can slip throgh
    open corners when going diagonally. Keep in mind, the robots can do 
    the same!

    Press Enter to begin (or QUIT).
    """).strip()

    def __init__(self) -> None:
        super().__init__()
        self.precmd = self.pre_first_command
        self.is_granted_move = True

    def preloop(self) -> None:
        clear_screen()

    def postloop(self) -> None:
        print("\nThanks for playing.\n")

    def pre_first_command(self, line: str) -> str:
        self.precmd = self.pre_regular_command
        command = line.strip().upper()
        return command if command and command.split()[0] in {"EOF", "QUIT"} else ""

    @staticmethod
    def pre_regular_command(line: str):
        command = line.strip().upper()
        if command == "Y": command = "Z"
        return command

    def postcmd(self, stop: bool, line: str) -> bool:
        if stop: return True
        is_terminated = False
        if not self.is_granted_move:
            world.move_all_robots()
            self.is_granted_move = False
        if world.is_player_alive():
            if world.get_num_robots() > 0:
                world.add_message(f"You are still alive and chased by {world.get_num_robots()} robots.")
            else:
                world.add_message("All robots have crashed into each other.")
                world.add_message("Good job!")
                is_terminated = True
        else:
            world.add_message("You are dead.")
            is_terminated = True
        clear_screen()
        print(f"{self.title}\n")
        print(world.render())
        return is_terminated

    def emptyline(self) -> None:
        self.is_granted_move = True

    def default(self, line: str) -> None:
        if line not in world.get_valid_moves():
            world.add_message(f"Impossible move: \"{line}\". Try again.")
            self.is_granted_move = True
        else:
            world.move_player(line)
            self.is_granted_move = False

    def do_S(self, _: str) -> None:
        if not world.is_frozen():
            self.is_granted_move = False

    @staticmethod
    def do_T(_: str) -> None:
        if not world.is_frozen():
            world.move_player_random()

    @staticmethod
    def do_EOF(_: str) -> bool:
        return True

    @staticmethod
    def do_QUIT(_: str) -> bool:
        return True
