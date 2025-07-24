X, O, BLANK = "X", "O", " "
PLAYERS = X, O
SPACES = set("789456123")


class Board:
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
            raise KeyError(f"{key} is not a valid tic-tac-toe space")
        if value not in PLAYERS:
            raise ValueError(f"{value} is not a valid tic-tac-toe player")
        self._board[index] = value

    def __getitem__(self, key: str) -> str:
        index = "789456123".find(key)
        if index < 0:
            raise KeyError(f"{key} is not a valid tic-tac-toe space")
        return self._board[index]


def main() -> None:
    board = Board()
    board["7"] = O
    print(board)
    if board["7"] == BLANK:
        print("free")
    else:
        print("occupied")


main()
