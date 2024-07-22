import textwrap


def intro(prog: str):
    return textwrap.dedent(
        f"""
        {prog}
        Find all the factors of a given integer number (1 <= number).
        """
    ).strip()


def get_response() -> int:
    while True:
        print('Enter a number to factor (or [Q]UIT to quit):')

        response = input('> ').strip().upper()

        if response == '':
            continue

        if response in {'Q', 'QUIT'}:
            return -1

        try:
            number = int(response)
            if number < 1:
                raise ValueError()
            return number

        except ValueError:
            print(f'"{response}" cannot be processed. Please enter a strictly positive integer.')


def factorize(n: int) -> list[int]:
    factors = {1, n}

    for candidate in range(2, int(n ** 0.5) + 1):
        if n % candidate == 0:
            factors.update({candidate, n // candidate})

    return sorted(factors)


def main(prog: str) -> None:
    print(intro(prog))

    while True:
        number = get_response()

        if number < 0:
            print('Bye!')
            return

        factors = factorize(number)
        print(', '.join(str(n) for n in factors))


if __name__ == '__main__':
    main('Factor Finder')
