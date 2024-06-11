"""
Draw diamonds of various sizes.
Original code at https://nostarch.com/big-book-small-python-projects.
"""


def outlined_diamond(size: int) -> list[str]:
    upper, lower = [], []

    for i in range(size):
        upper.append(' ' * (size - i - 1) + '/' + ' ' * (i * 2) + '\\')
        lower.append(' ' * i + '\\' + ' ' * ((size - i - 1) * 2) + '/')

    return upper + lower


def filled_diamond(size: int) -> list[str]:
    upper, lower = [], []

    for i in range(size):
        upper.append(' ' * (size - i - 1) + '/' * (i + 1) + '\\' * (i + 1))
        lower.append(' ' * i + '\\' * (size - i) + '/' * (size - i))

    return upper + lower


def main():
    # display diamonds of sizes 0 to 5
    for diamond_size in range(6):
        width = diamond_size * 2
        print(
            '\n'.join(
                f'{a:{width}s}   {b:{width}s}'
                for a, b in zip(
                    outlined_diamond(diamond_size),
                    filled_diamond(diamond_size)
                )
            )
        )


if __name__ == '__main__':
    main()
