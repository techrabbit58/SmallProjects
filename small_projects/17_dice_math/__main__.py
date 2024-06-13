import random

from .dicefaces import die_face
from .parameters import MIN_DICE, MAX_DICE


def roll(num_dice: int) -> tuple[int, list[list[str]]]:
    total = 0
    dice_faces = []
    for _ in range(num_dice):
        number = random.randint(1, 6)
        total += number
        dice_faces.append(die_face(number))
    return total, dice_faces


def main() -> None:
    num_dice = random.randint(MIN_DICE, MAX_DICE)
    total, dice = roll(num_dice)
    print('\n'.join('   '.join(row) for row in zip(*dice)))
    print(f'These {num_dice} dice give a total of {total} pips.')


main()
