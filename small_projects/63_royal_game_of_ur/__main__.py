import os
import random
import sys
import textwrap
import time
from dataclasses import dataclass

X_PLAYER = "X"
O_PLAYER = "O"
EMPTY = " "

X_HOME, X_GOAL = "x_home", "x_goal"
O_HOME, O_GOAL = "o_home", "o_goal"

SPACES = "hgfetsijklmnopdcbarq"
X_TRACK = "HefghijklmnopstG"
O_TRACK = "HabcdijklmnopqrG"

FLOWERS = {"h", "t", "l", "d", "r"}

BOARD_TEMPLATE = """
                  {}           {}
                   Home              Goal
                     v                 ^
+-----+-----+-----+--v--+           +--^--+-----+
|*****|     |     |     |           |*****|     |
|* {} *<  {}  <  {}  <  {}  |           |* {} *<  {}  |
|****h|    g|    f|    e|           |****t|    s|
+--v--+-----+-----+-----+-----+-----+-----+--^--+
|     |     |     |*****|     |     |     |     |
|  {}  >  {}  >  {}  >* {} *>  {}  >  {}  >  {}  >  {}  |
|    i|    j|    k|****l|    m|    n|    o|    p|
+--^--+-----+-----+-----+-----+-----+-----+--v--+
|*****|     |     |     |           |*****|     |
|* {} *<  {}  <  {}  <  {}  |           |* {} *<  {}  |
|****d|    c|    b|    a|           |****r|    q|
+-----+-----+-----+--^--+           +--v--+-----+
                     ^                 v
                   Home              Goal
                  {}           {}
"""


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)


def get_intro() -> str:
    return textwrap.dedent("""
    The Royal Game of Ur
    
    Two players must move seven tokens from their home to their goal.
    The players play subsequent alternating turns. A player, when on
    turn, flips four coins and can then move one token as many spaces
    as he got heads. Then the turn changes. The first player who moves 
    all his seven tokens from home to the goal, wins the game.
    
                X home      X goal
                  v           ^
    +---+---+---+-v-+       +-^-+---+
    |v<<<<<<<<<<<<< |       | ^<<<< |
    |v  |   |   |   |       |   | ^ |
    +v--+---+---+---+---+---+---+-^-+
    |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>^ |
    |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>v |
    +^--+---+---+---+---+---+---+-v-+
    |^  |   |   |   |       |   | v |
    |^<<<<<<<<<<<<< |       | v<<<< |
    +---+---+---+-^-+       +-v-+---+
                  ^           v
                O home      O goal
                
    If a player lands one token on the opponents token in the middle
    track, it sends this token back to the opponent's home. If a token
    lands on a flower space, the player gets granted one more turn.
    Tokens in the middle flower space are "safe" and cannot be landed on.
    """).strip()


def get_new_board() -> dict[str, int | str]:
    board: dict[str, int | str] = {X_HOME: 7, X_GOAL: 0, O_HOME: 7, O_GOAL: 0}
    for label in SPACES:
        board[label] = EMPTY
    return board


def render_game_board(board: dict[str, int | str]) -> str:
    x_home_tokens = ("X" * board[X_HOME]).ljust(7, ".")
    x_goal_tokens = ("X" * board[X_GOAL]).ljust(7, ".")
    o_home_tokens = ("O" * board[O_HOME]).ljust(7, ".")
    o_goal_tokens = ("O" * board[O_GOAL]).ljust(7, ".")
    spaces = ([x_home_tokens, x_goal_tokens] +
              [board[label] for label in SPACES] +
              [o_home_tokens, o_goal_tokens])
    return BOARD_TEMPLATE.format(*spaces)


@dataclass(kw_only=True, frozen=True)
class Context:
    home: str
    track: str
    goal: str
    opponent: str
    opponent_home: str


def get_valid_moves(board: dict[str, int | str], player: str, flip_tally: int, context: Context) -> list[str]:
    valid_moves = []

    if board[context.home] > 0 and board[context.track[flip_tally]] == EMPTY:
        valid_moves.append("home")

    for index, space in enumerate(context.track):
        if space in ("G", "H") or board[space] != player:
            continue
        next_index = index + flip_tally
        if next_index >= len(context.track):
            continue
        next_space = context.track[next_index]
        if next_space == "G":
            valid_moves.append(space)
            continue
        if board[next_space] in (EMPTY, context.opponent):
            if next_space == "l" and board["l"] == context.opponent:
                continue
            valid_moves.append(space)

    return valid_moves + ["quit"]


def main() -> None:
    clear_screen()
    print(get_intro())
    input("\nPress Enter to begin...")

    board = get_new_board()
    player = O_PLAYER

    while True:
        if player == X_PLAYER:
            context = Context(home=X_HOME, track=X_TRACK, goal=X_GOAL, opponent=O_PLAYER, opponent_home=O_HOME)
        else:
            context = Context(home=O_HOME, track=O_TRACK, goal=O_GOAL, opponent=X_PLAYER, opponent_home=X_HOME)

        clear_screen()
        print(render_game_board(board))
        input(f"Ready player {player}. Press Enter to flip the coins...")

        flip_tally = 0
        print("Flips: ", end="", flush=True)
        for _ in range(4):
            time.sleep(.3)
            face = random.randint(0, 1)
            print("TH"[face], end=" ", flush=True)
            flip_tally += face
        print(end=" ")

        if flip_tally == 0:
            input("No heads. You loose this turn. Press Enter to continue...")
            player = context.opponent
            continue

        valid_moves = get_valid_moves(board, player, flip_tally, context)

        if not valid_moves:
            input("No valid moves. You loose this turn. Press Enter to continue...")
            player = context.opponent
            continue

        move = None
        while not move:
            print(f"You may jump {flip_tally} spaces. Select your move:")
            print(", ".join(valid_moves), end=" ")

            move = input("> ").strip().lower()
            if move not in valid_moves:
                print(f"This is not a valid move: \"{move}\"")
                move = None
                continue

        if move == "quit":
            break

        if move == "home":
            board[context.home] -= 1
            next_index = flip_tally
        else:
            board[move] = EMPTY
            next_index = context.track.index(move) + flip_tally

        moving_onto_goal = (next_index == len(context.track) - 1)
        if moving_onto_goal:
            board[context.goal] += 1
            if board[context.goal] == 7:
                clear_screen()
                print(render_game_board(board))
                print(f"Player {player} wins!")
                break
        else:
            next_space = context.track[next_index]
            if board[next_space] == context.opponent:
                board[context.opponent_home] += 1

        board[next_space] = player

        if next_space in FLOWERS:
            input(f"{player} landed on a flower space and goes again. Press Enter to continue...")
            continue

        player = context.opponent

    print("Thanks for playing.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
