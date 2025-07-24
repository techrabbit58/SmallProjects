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


def main() -> None:
    board = Board()
    board["1"] = X
    print(board)
    if board["7"] == BLANK:
        print("free")
    else:
        print("occupied")


main()
