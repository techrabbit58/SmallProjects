import random

BLANK = 0


def ask_for_player_move() -> str:
    print('Enter your move: (WASD or Q to quit)')
    while True:
        try:
            move = input('> ').upper()
        except KeyboardInterrupt:
            print()
            return 'Q'

        if move in {'W', 'A', 'S', 'D', 'Q'}:
            return move

        print('You must enter one of "W", "A", "S" or "D", or "Q". Please try again.')


def new_board() -> dict[tuple[int, int], int]:
    board = {(col, row): BLANK for col in range(4) for row in range(4)}
    positions = random.choices(list(board), k=2)
    for p in positions:
        board[p] = 2
    return board


def render_board(board: dict[tuple[int, int], int]) -> tuple[str, int]:
    labels, score = [], 0
    for row in range(4):
        line = ['|']
        for col in range(4):
            label = board[(col, row)]
            score += label
            line.append(f'{label:^5d}|' if label != 0 else '     |')
        labels.append(''.join(line))
    return '\n'.join(labels), score


def execute_the_move(board: dict[tuple[int, int], int], move: str) -> dict[tuple[int, int], int]:
    tubes = {
        'W': [[(col, row) for row in range(4)] for col in range(4)],
        'A': [[(col, row) for col in range(4)] for row in range(4)],
        'S': [[(col, row) for row in range(3, -1, -1)] for col in range(4)],
        'D': [[(col, row) for col in range(3, -1, -1)] for row in range(4)],
    }

    next_board = {}
    for positions in tubes[move]:
        streak = []
        for position in positions:
            tile = board[position]
            if tile != 0:
                streak.append(tile)
        while len(streak) < 4:
            streak.append(BLANK)
        for i in range(3):
            if streak[i] == streak[i + 1]:
                streak[i] *= 2
                for j in range(i + 1, 3):
                    streak[j] = streak[j + 1]
                streak[3] = BLANK
        for i in range(4):
            next_board[positions[i]] = streak[i]

    return next_board


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

    game_board = new_board()

    while True:
        print('{}\nScore: {}'.format(*render_board(game_board)))

        move = ask_for_player_move()

        if move == 'Q':
            print('Thank you for playing.')
            break

        game_board = execute_the_move(game_board, move)
        game_over = prepare_for_next_move(game_board)

        if game_over:
            print('{}\nScore: {}'.format(*render_board(game_board)))
            print('Game over.')
            break

    print('Bye!')


main()
