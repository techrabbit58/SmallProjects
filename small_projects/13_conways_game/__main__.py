import time

from . import grid


def main() -> None:
    mx, my = grid.WIDTH // 2, grid.HEIGHT // 2
    grid.init([  # starts with the "f-pentomino" instead of a random population
        grid.Cell(mx + 1, my - 1),
        grid.Cell(mx, my - 1),
        grid.Cell(mx - 1, my),
        grid.Cell(mx, my),
        grid.Cell(mx, my + 1),
    ])

    while True:

        print('\n' * 50)

        current_generation = grid.get_population()
        next_generation = []

        for y in range(grid.HEIGHT):
            for x in range(grid.WIDTH):
                cell = grid.Cell(x, y)
                print('o' if cell in current_generation else ' ', end='')
                if grid.is_survivor(cell):
                    next_generation.append(cell)
            print()
        print('Press Ctrl-C to quit.')

        grid.set_next_generation(next_generation)

        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
