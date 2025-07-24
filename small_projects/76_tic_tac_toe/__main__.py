import itertools
from string import Template

X, O, BLANK = "X", "O", " "
PLAYERS = X, O
SPACES = "789456123"


class Board:
    bad_key = Template("'$key' is not a valid Tic-Tac-Toe space")
    bad_value = Template("'$value' is not a valid Tic-Tac-Toe player")

    def __init__(self) -> None:
        self._board = [BLANK] * 9

    def __str__(self) -> str:
        return """
           T i c - T a c - T o e
        
           .   .
         {} | {} | {}      7   8   9
        ---+---+---
         {} | {} | {}      4   5   6
        ---+---+---
         {} | {} | {}      1   2   3
           '   '
        """.format(*self._board)

    def __setitem__(self, key: str, value: str) -> None:
        index = "789456123".find(key)
        if index < 0:
            raise KeyError(self.bad_key.substitute(key=key))
        if value not in PLAYERS:
            raise ValueError(self.bad_value.substitute(value=value))
        self._board[index] = value

    def __getitem__(self, key: str) -> str:
        index = SPACES.find(key)
        if index < 0:
            raise KeyError(self.bad_key.substitute(key=key))
        return self._board[index]

    def is_full(self) -> bool:
        return all(space != BLANK for space in self._board)

    def has_won(self, player: str) -> bool:
        return any((
            (player == self["1"] == self["2"] == self["3"]),
            (player == self["4"] == self["5"] == self["6"]),
            (player == self["7"] == self["8"] == self["9"]),
            (player == self["1"] == self["4"] == self["7"]),
            (player == self["2"] == self["5"] == self["8"]),
            (player == self["3"] == self["6"] == self["9"]),
            (player == self["1"] == self["5"] == self["9"]),
            (player == self["3"] == self["5"] == self["7"]),
        ))


def ask_player(question: str, choices: list[str]) -> str:
    choice = ""
    while not choice:
        print(question)
        answer = input("> ").strip()
        if len(answer) == 0:
            continue
        choice = answer.upper()
        if choice not in choices:
            print(f"'{answer}' is not in {list(choices)}. Try again.")
            choice = ""
            continue
    return choice


def main() -> None:
    board = Board()
    lineup = itertools.cycle((X, O))

    player = next(lineup)
    while True:
        print(board)
        answer = ask_player(
            f"What is player {player}'s move? (1-9 or Q)",
            list(SPACES) + ["Q"]
        )

        if answer == "Q":
            break

        if board[answer] != BLANK:
            print("This space is already occupied. Try another.")
            continue

        board[answer] = player

        if board.has_won(player):
            print(board)
            print(f"Player {player} has won the game.")
            break

        if board.is_full():
            print(board)
            print("This is a tie.")
            break

        player = next(lineup)

    print("Thanks for playing.")


main()
