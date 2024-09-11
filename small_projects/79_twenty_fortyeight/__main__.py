import random

BLANK = 0

_strip_selectors = {
    'W': [[(col, row) for row in range(4)] for col in range(4)],
    'A': [[(col, row) for col in range(4)] for row in range(4)],
    'S': [[(col, row) for row in range(3, -1, -1)] for col in range(4)],
    'D': [[(col, row) for col in range(3, -1, -1)] for row in range(4)],
}


def ask_for_player_move() -> str:
    print('Enter your move: (WASD or Q to quit)')
    while True:
        try:
            move = input('> ').upper()
        except KeyboardInterrupt:
            print()
            return 'Q'

        if move == 'Q' or move in _strip_selectors:
            return move

        print('You must enter one of "W", "A", "S" or "D", or "Q". Please try again.')


def initialize() -> dict[tuple[int, int], int]:
    board = {(col, row): BLANK for col in range(4) for row in range(4)}

    positions = random.choices(list(board), k=2)
    for p in positions:
        board[p] = 2

    return board


def render(board: dict[tuple[int, int], int]) -> tuple[str, int]:
    labels, score = [], 0

    for row in range(4):
        line = ['|']
        for col in range(4):
            label = board[(col, row)]
            score += label
            line.append(f'{label:^5d}|' if label != 0 else '     |')
        labels.append(''.join(line))

    return '\n'.join(labels), score


def execute(board: dict[tuple[int, int], int], move: str) -> dict[tuple[int, int], int]:
    next_board = {}

    for selection in _strip_selectors[move]:
        strip = extract_nonblank(board, selection)
        append_blanks(strip)
        agglomerate(strip)
        copy(next_board, selection, strip)

    return next_board


def copy(
        board: dict[tuple[int, int], int],
        selection: list[tuple[int, int]],
        strip: list[int],
        *, length: int = 4) -> None:

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


def extract_nonblank(board: dict[tuple[int, int], int], selection: list[tuple[int, int]]):
    strip = []

    for tile in selection:
        value = board[tile]
        if value != BLANK:
            strip.append(value)

    return strip


def append_blanks(strip: list[int], *, length: int = 4) -> None:
    while len(strip) < length:
        strip.append(BLANK)


def prepare_for_next_move(board: dict[tuple[int, int], int]) -> bool:
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

        move = ask_for_player_move()

        if move == 'Q':
            print('Thank you for playing.')
            break

        game_board = execute(game_board, move)
        is_game_over = prepare_for_next_move(game_board)

        if is_game_over:
            print('{}\nScore: {}'.format(*render(game_board)))
            print('Game over.')
            break

    print('Bye!')


main()
