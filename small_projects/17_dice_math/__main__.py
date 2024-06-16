import random
import time
from textwrap import dedent
from typing import TypeAlias

import key_stroke
from colterm import term

from .dicefaces import die_face, FACE_WIDTH, FACE_HEIGHT
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


DiceFace: TypeAlias = list[str]
Canvas: TypeAlias = dict[tuple[int, int], str]


def can_place_face_at(origin_x: int, origin_y: int, canvas: Canvas) -> bool:
    for x, y in {
        (origin_x, origin_y),
        (origin_x + FACE_WIDTH, origin_y),
        (origin_x + FACE_WIDTH, origin_y + FACE_HEIGHT),
        (origin_x, origin_y + FACE_HEIGHT)
    }:
        if (y, x) in canvas:
            return False
    return True


def place_dice_faces(canvas_width: int, canvas_height: int, dice_faces: list[DiceFace]) -> Canvas:
    canvas = {}

    for face in dice_faces:
        while True:
            origin_x = random.randint(0, canvas_width - FACE_WIDTH - 1)
            origin_y = random.randint(1, canvas_height - FACE_HEIGHT - 4)
            if can_place_face_at(origin_x, origin_y, canvas):
                for dx in range(FACE_WIDTH):
                    for dy in range(FACE_HEIGHT):
                        canvas[(origin_y + dy, origin_x + dx)] = face[dy][dx]
                break

    return canvas


def main() -> None:
    kb = key_stroke.Key_Stroke()

    term.clear()
    print(rules())

    print('\nPress any key to continue.')
    wait_for_any_key(kb)

    correct_answers = incorrect_answers = score = 0

    while True:
        num_dice = random.randint(MIN_DICE, MAX_DICE)
        total, dice = roll(num_dice)

        canvas = place_dice_faces(term.width(), term.height(), dice)

        countdown = QUIZ_DURATION * 10
        answer = ''
        while countdown > 0:
            term.clear()
            term.hide_cursor()

            print('Guess the number of pips:')

            term.fg('cyan')
            # print('\n'.join('   '.join(row) for row in zip(*dice)))
            for (y, x), ch in canvas.items():
                term.goto(x, y)
                print(ch, flush=True, end='')

            term.fg('yellow')
            term.goto(0, term.height() - 4)
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
