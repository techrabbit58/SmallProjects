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
    return textwrap.dedent(f"""
    The Royal Game of Ur
    
    Two players must move seven tokens from their home to their goal.
    The players play subsequent alternating turns. A player, when on
    turn, flips four coins and can then move one token as many spaces
    as he got heads. Then the turn changes. The first player who moves 
    all his seven tokens from home to the goal, wins the game.
    
                {X_PLAYER} home      {X_PLAYER} goal
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
                {O_PLAYER} home      {O_PLAYER} goal
                
    If a player lands one token on the opponents token in the middle
    track, it sends this token back to the opponent's home. If a token
    lands on a flower space, the player gets granted one more turn.
    Tokens in the middle flower space are "safe" and cannot be landed on.
    """).strip()


@dataclass(kw_only=True, frozen=True)
class Player:
    name: str
    home: str
    track: str
    goal: str


def get_new_board(*, player_o: Player, player_x: Player) -> dict[str, int | str]:
    board: dict[str, int | str] = {player_x.home: 7, player_x.goal: 0, player_o.home: 7, player_o.goal: 0}
    for label in SPACES:
        board[label] = EMPTY
    return board


def render_game_board(board: dict[str, int | str]) -> str:
    x_home_tokens = (X_PLAYER * board[X_HOME]).ljust(7, ".")
    x_goal_tokens = (X_PLAYER * board[X_GOAL]).ljust(7, ".")
    o_home_tokens = (O_PLAYER * board[O_HOME]).ljust(7, ".")
    o_goal_tokens = (O_PLAYER * board[O_GOAL]).ljust(7, ".")
    spaces = ([x_home_tokens, x_goal_tokens] +
              [board[label] for label in SPACES] +
              [o_home_tokens, o_goal_tokens])
    return BOARD_TEMPLATE.format(*spaces)


def get_valid_moves(*, board: dict[str, int | str], flip_tally: int, player: Player, opponent: Player) -> list[str]:
    valid_moves = []

    if board[player.home] > 0 and board[player.track[flip_tally]] == EMPTY:
        valid_moves.append("home")

    for index, space in enumerate(player.track):
        if space in ("G", "H") or board[space] != player.name:
            continue
        next_index = index + flip_tally
        if next_index >= len(player.track):
            continue
        next_space = player.track[next_index]
        if next_space == "G":
            valid_moves.append(space)
            continue
        if board[next_space] in {EMPTY, opponent.name}:
            if next_space == "l" and board["l"] == opponent.name:
                continue
            valid_moves.append(space)

    return valid_moves + ["quit"]


def main() -> None:
    clear_screen()
    print(get_intro())
    input("\nPress Enter to begin...")

    player = Player(name=O_PLAYER, home=O_HOME, track=O_TRACK, goal=O_GOAL)
    opponent = Player(name=X_PLAYER, home=X_HOME, track=X_TRACK, goal=X_GOAL)
    board = get_new_board(player_o=player, player_x=opponent)

    while True:
        clear_screen()
        print(render_game_board(board))
        print(f"Ready player {player.name}.")

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
            player, opponent = opponent, player
            continue

        valid_moves = get_valid_moves(board=board, flip_tally=flip_tally, player=player, opponent=opponent)

        if len(valid_moves) <= 1:  # The only available move would be "quit"
            input("No valid moves. You loose this turn. Press Enter to continue...")
            player, opponent = opponent, player
            continue

        move = None
        while not move:
            print(f"You may jump {flip_tally} space{'s' if flip_tally > 1 else ''}."
                  f"j Select your move:")
            print(", ".join(valid_moves), end=" ")

            move = input("> ").strip().lower()
            if move not in valid_moves:
                print(f"This is not a valid move: \"{move}\"")
                move = None
                continue

        if move == "quit":
            break

        if move == "home":
            board[player.home] -= 1
            next_index = flip_tally
        else:
            board[move] = EMPTY
            next_index = player.track.index(move) + flip_tally

        moving_onto_goal = (next_index == len(player.track) - 1)
        next_space = None
        if moving_onto_goal:
            board[player.goal] += 1
            if board[player.goal] == 7:
                clear_screen()
                print(render_game_board(board))
                print(f"* * *  Player {player.name} wins.  * * *")
                break
        else:
            next_space = player.track[next_index]
            if board[next_space] == opponent.name:
                board[opponent.home] += 1
            board[next_space] = player.name

        if next_space in FLOWERS:
            input(f"{player.name} landed on a flower space and goes again. Press Enter to continue...")
            continue

        player, opponent = opponent, player

    print("Thanks for playing.\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
