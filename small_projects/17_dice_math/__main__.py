import random

from .dicefaces import die_face


def main() -> None:
    dice = []
    for _ in range(5):
        dice.append(die_face(random.randint(1, 6)))
    print('\n'.join(' '.join(row) for row in zip(*dice)))


main()
