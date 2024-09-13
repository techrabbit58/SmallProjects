import math
import shutil
import textwrap
import time


def intro(prog: str):
    return textwrap.dedent(
        f"""
        {prog}
        Find all prime numbers greater or equal to a given positive integer number (0 <= number).
        """
    ).strip()


def get_response() -> int:
    while True:
        print('Enter a non-negative number to start a new primes search (or [Q]UIT to quit):')

        try:
            response = input('> ').strip().upper()
        except KeyboardInterrupt:
            print()
            response = ''

        if response == '':
            continue

        if response in {'Q', 'QUIT'}:
            return -1

        try:
            number = int(response)
            if number < 0:
                raise ValueError()
            return number

        except ValueError:
            print(f'"{response}" cannot be processed. Please enter a non-negative integer.')


def is_prime(n: int) -> bool:
    if n < 2:
        return False

    if n == 2:
        return True

    for k in range(2, int(math.sqrt(n)) + 1):
        if n % k == 0:
            return False

    return True


def main(prog: str) -> None:
    print(intro(prog))

    while True:
        number = get_response()

        if number < 0:
            print('Bye!')
            return

        print('Press Ctrl-C to stop the prime generator.')
        print('...', end='', flush=True)
        current_column = 0
        width, _ = shutil.get_terminal_size((80, 20))
        while True:
            try:
                if is_prime(number):
                    text = f'{number}, ...'
                    if current_column + len(text) < width:
                        print(f'\b\b\b{text}', end='', flush=True)
                        current_column -= 3
                    else:
                        print(f'\b\b\b\b    \n{text}', end='', flush=True)
                        current_column = 0
                    current_column += len(text)
                    time.sleep(.1)
                number += 1
            except KeyboardInterrupt:
                print('\b\b\b\b\b     ')
                break


if __name__ == '__main__':
    main('Prime Numbers')
