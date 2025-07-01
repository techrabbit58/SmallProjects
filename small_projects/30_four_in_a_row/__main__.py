import itertools

BOARD_WIDTH = 7
BOARD_HEIGHT = 6


class GameBoard:
    def __init__(self, *, width: int, height: int) -> None:
        self.labels = [str(n + 1) for n in range(width)]
        self.locations = [["."] * width for _ in range(height)]
        self.next_entry = [height - 1] * width
        self.size = height * width

    def is_full(self) -> bool:
        return all(i < 0 for i in self.next_entry)

    def is_winner(self, player: str) -> bool:
        goal = "".join(player * 4)

        for row in self.locations:  # check each row if it has four in a row for the player
            if goal in "".join(row):
                return True

        for col in self.labels:  # check each column if it has four in a row for the player
            text = "".join(ch[int(col) - 1] for ch in self.locations)
            if goal in text:
                return True

        for col in range(len(self.locations[0]) - 3):  # check diagonals if player is winner
            for row in range(len(self.locations) - 3):

                # check right down first
                text = "".join([
                    self.locations[row][col],
                    self.locations[row + 1][col + 1],
                    self.locations[row + 2][col + 2],
                    self.locations[row + 3][col + 3],
                ])
                if goal == text:
                    return True

                # and then check left down
                text = "".join([
                    self.locations[row][col + 3],
                    self.locations[row + 1][col + 2],
                    self.locations[row + 2][col + 1],
                    self.locations[row + 3][col],
                ])
                if goal == text:
                    return True

        return False

    def apply(self, player: str, move: str) -> bool:
        column = int(move) - 1

        if self.next_entry[column] < 0:
            return False

        self.locations[self.next_entry[column]][column] = player
        self.next_entry[column] -= 1

        return True

    def __str__(self) -> str:
        text = [
            " ".join((" ", *self.labels, " ")),
            ".-" + "--" * len(self.labels) + "."
        ]
        for row in self.locations:
            text.append(" ".join(("|", *row, "|")))
        text.append("'-" + "--" * len(self.labels) + "'")
        return "\n".join(text)


def ask_player(player: str, valid_choices: list[str]) -> str:
    while True:
        print(f"Player {player}, enter a column number or QUIT.")
        move = input("> ").upper()
        if move in valid_choices or "QUIT".startswith(move):
            break
        else:
            print("This is not an acceptable move. Try again.")

    return move


class App:
    players = itertools.cycle("XO")

    def __init__(self, *, intro: str, game_board: GameBoard) -> None:
        self.intro = intro
        self.game_board = game_board

    def run(self) -> None:
        player = next(self.players)

        print(f"\n{self.intro}")

        while True:
            print(f"\n{self.game_board}")

            move = ask_player(player, self.game_board.labels)

            if move not in self.game_board.labels:  # must be a "QUIT"
                print(f"\nPlayer {player} quits. Game over.")
                print("Thank you for playing. Bye.\n")
                break

            if not self.game_board.apply(player, move):
                print("This move cannot be made. Try again.")
                continue

            is_full = self.game_board.is_full()
            is_finished = self.game_board.is_winner(player)

            if is_full or is_finished:
                print(f"\n{self.game_board}")

                if is_full:
                    print("\nThere is a tie.\n")
                    break

                if is_finished:
                    print(f"\nPlayer {player} has won.\n")
                    break

            player = next(self.players)


def main() -> None:
    App(
        intro="Four in a Row, by Al Sweigart (al@inventwithpython)\n"
              "          -*| refactored version |*-\n\n"
              "Two players make turns dropping tiles into one of the columns,\n"
              "trying to make four tiles in a row horizontally, vertically,\n"
              "or diagonally.",
        game_board=GameBoard(width=BOARD_WIDTH, height=BOARD_HEIGHT)
    ).run()


main()
