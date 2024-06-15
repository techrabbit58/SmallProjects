import random
import time
from textwrap import dedent

import key_stroke
from colterm import term

from .dicefaces import die_face
from .parameters import MIN_DICE, MAX_DICE, QUIZ_DURATION, PENALTY, REWARD


def roll(num_dice: int) -> tuple[int, list[list[str]]]:
    total = 0
    dice_faces = []
    for _ in range(num_dice):
        number = random.randint(1, 6)
        total += number
        dice_faces.append(die_face(number))
    return total, dice_faces


def rules() -> str:
    return dedent(f"""
    The program rolls some dice and shows them to you.
    You then have {QUIZ_DURATION} seconds to count the pips.
    If you can enter the right number of pips while the time
    counts down, you receive {REWARD} more points.
    If you can not gie an answer before the time is over, your
    score will decrease by {PENALTY} points.
    """).strip()


def sleep(seconds: float = 1.0) -> None:
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass


def wait_for_any_key(kb: key_stroke.Key_Stroke) -> None:
    while not kb.kbhit():
        sleep(.1)
    term.get_key()


def main() -> None:
    kb = key_stroke.Key_Stroke()

    term.clear()
    print(rules())

    print('\nPress any key to continue.')
    wait_for_any_key(kb)

    correct_answers = incorrect_answers = score = 0

    while True:
        print('Guess the number of pips:')

        num_dice = random.randint(MIN_DICE, MAX_DICE)
        total, dice = roll(num_dice)

        countdown = QUIZ_DURATION * 10
        answer = ''
        while countdown > 0:
            term.clear()
            term.hide_cursor()

            term.fg('cyan')
            print('\n'.join('   '.join(row) for row in zip(*dice)))

            term.fg('yellow')
            print(f'Your current score is {score} points.')
            print(f'There are {num_dice} dice shown. Guess the total number of pips.')
            print(f'You have {countdown // 10} seconds left.')

            term.fg('reset')
            term.show_cursor()

            print(f'your guess> {answer}', end='', flush=True)

            if kb.kbhit():
                ch = term.get_key().lower()
                if ch in '0123456789':
                    answer += ch
                elif (ch == 'q' and answer == '') or (ch == '\n' and len(answer) > 0):
                    if answer == '':
                        answer = 'quit'
                    print()
                    break
                elif ch == '\b' and len(answer) > 0:
                    answer = answer[:-1]
            else:
                sleep(.1)
                countdown -= 1

        if answer == 'quit':
            break
        else:
            if countdown >= 10 and int(answer) == total:
                term.fg('green')
                print(f'Your answer was correct after {QUIZ_DURATION - (countdown // 10)} seconds: {answer} pips.')
                correct_answers += 1
            elif not countdown:
                term.fg('red')
                print(f'\nYour anwer is missing after {QUIZ_DURATION} seconds. You lose.')
                incorrect_answers += 1
            else:
                term.fg('red')
                print(f'Your answer {answer} was wrong. Instead, {total} would have been the correct answer.')
                incorrect_answers += 1
            score = correct_answers * REWARD - incorrect_answers * PENALTY

        term.fg('reset')
        print('Press any key to continue.')
        wait_for_any_key(kb)

    term.clear()
    print('Correct answers:   ', correct_answers)
    print('Incorrect answers: ', incorrect_answers)
    print('Final score:       ', score)
    print('Bye!')


main()
