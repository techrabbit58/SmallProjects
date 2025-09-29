import random
from typing import TypeAlias, NamedTuple, Literal, cast

BLANK = 0


class Position(NamedTuple):
    col: int
    row: int


Board: TypeAlias = dict[Position, int]
Move: TypeAlias = Literal['W', 'A', 'S', 'D', 'Q']

_strip_selectors: dict[Move, list[list[Position]]] = {
    'W': [[Position(col, row) for row in range(4)] for col in range(4)],
    'A': [[Position(col, row) for col in range(4)] for row in range(4)],
    'S': [[Position(col, row) for row in range(3, -1, -1)] for col in range(4)],
    'D': [[Position(col, row) for col in range(3, -1, -1)] for row in range(4)],
}


def ask_for_player_move() -> Move:
    print('Enter your move: (WASD or Q to quit)')
    while True:
        try:
            move = input('> ').upper()
        except KeyboardInterrupt:
            print()
            return 'Q'

        if move == 'Q' or move in _strip_selectors:
            return cast(Move, move)

        print('You must enter one of "W", "A", "S" or "D", or "Q". Please try again.')


def initialize() -> Board:
    """
    Create a new game board and randomly place two twos.
    """
    board = {Position(col, row): BLANK for col in range(4) for row in range(4)}

    positions = random.choices(list(board), k=2)
    for p in positions:
        board[p] = 2

    return board


def render(board: Board) -> tuple[str, int]:
    """
    Create a new screen image for the TTY.
    At the same time, add up all non-blank values giving the current game score.
    Return both the screen image (a text) and the score (a number).
    """
    labels, score = [], 0

    for row in range(4):
        line = ['|']
        for col in range(4):
            label = board[Position(col, row)]
            score += label
            line.append(f'{label:^5d}|' if label != 0 else '     |')
        labels.append(''.join(line))

    return '\n'.join(labels), score


def execute(current_board: Board, move: Move) -> tuple[Board, bool]:
    """
    Perform the current move.
    Check if the move did change something.
    Return both the new board status, and an indicator that the board has changed.
    """
    next_board = {}

    for selection in _strip_selectors[move]:
        strip = extract_nonblank(current_board, selection)
        append_blanks(strip)
        agglomerate(strip)
        copy(next_board, selection, strip)

    has_changed = next_board != current_board

    return next_board, has_changed


def copy(
        board: Board,
        selection: list[Position],
        strip: list[int],
        *, length: int = 4) -> None:
    """
    Copy a streak of length "length" to the boad's appropriate selection of tile positions.
    """
    for i in range(length):
        board[selection[i]] = strip[i]


def agglomerate(strip: list[int], *, length: int = 4) -> None:
    """
    Let numbers fall 'down' towards index 0 as far as possible and combine equal neighbors.
    As a result, all numbers in the strip are unique, and all blank tiles are at the highest
    index of the strip.
    """
    highest = length - 1

    for i in range(highest):
        if strip[i] == strip[i + 1]:
            strip[i] *= 2
            for j in range(i + 1, highest):
                strip[j] = strip[j + 1]
            strip[highest] = BLANK


def extract_nonblank(board: Board, selection: list[Position]):
    """
    Gather only the numbers from the board's selected tiles, skip the blank tiles and copy the numbers
    to a new strip.
    Return the new strip.
    """
    strip = []

    for tile in selection:
        value = board[tile]
        if value != BLANK:
            strip.append(value)

    return strip


def append_blanks(strip: list[int], *, length: int = 4) -> None:
    """Bring the strip to length "length" by filling in BLANK values at the end."""
    while len(strip) < length:
        strip.append(BLANK)


def prepare_for_next_move(board: Board) -> bool:
    """
    Add one more two to the board, to a random tile.
    The game is over if the board hasn't space left after inserting the new two.
    Return the "game over" status to the caller.
    """
    free_pos, is_game_over = [], False

    for position, value in board.items():
        if value == BLANK:
            free_pos.append(position)

    if len(free_pos) == 1:
        is_game_over = True

    board[random.choice(free_pos)] = 2

    return is_game_over


def main():

    game_board = initialize()

    while True:
        print('{}\nScore: {}'.format(*render(game_board)))

        move = ask_for_player_move()  # get next move: W, A, S, D or Q

        if move == 'Q':  # user quits by intent
            print('Thank you for playing.')
            break

        game_board, has_changed = execute(game_board, move)  # update the board according to the current move
        # "has_changed" is true only if the move did realy change someting

        is_game_over = has_changed and prepare_for_next_move(game_board)  # add neww two only if something has changed

        if is_game_over:  # the game is over if - after this move - no tile is left for a new two
            print('{}\nScore: {}'.format(*render(game_board)))
            print('Game over.')
            break

    print('Bye!')


if __name__ == '__main__':
    main()
