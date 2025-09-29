import random
import sys

from .boxes import two_boxes


def main():
    has_carrot = random.choice(['left', 'right'])
    left_box = ['RED', 'carrot' if has_carrot == 'left' else 'empty']
    right_box = ['GOLD', 'carrot' if has_carrot == 'right' else 'empty']

    print('Here are two boxes. The right is yours. The computer owns the left box.')
    print("There is a carrot in only one box. There is no visible clue if the carrot")
    print("is in your box or in the computer's box. You must try to win the carrot.")

    print(two_boxes(' '.join((left_box[0], 'closed')), ' '.join((right_box[0], 'closed'))))

    print('The computer already had a chance to open its box and look into it.')

    clue = random.choice(('is', 'is not'))
    print(f'The computer now says: There {clue} a carrot in my box. (The computer is sometimes a liar.)')

    print('You are now allowed to swap boxes with the computer.')

    def in_the_loop() -> bool:
        nonlocal left_box, right_box
        response = input('Would you like to swap? Please enter "yes" or "no": ').lower()
        if 'yes'.startswith(response):
            left_box, right_box = right_box, left_box
            print('You changed boxes with the computer.')
        elif 'no'.startswith('no'):
            print('You did not want to change.')
        else:
            print(f'You must enter "yes" or "no". You entered: "{response}".')
            return True

    try:
        while in_the_loop():
            pass
    except KeyboardInterrupt:
        sys.exit()

    print('The boxes are now open, so that everybody can see what is inside.')
    print(two_boxes(' '.join(left_box), ' '.join(right_box)))

    print(f"{'Congratulations! You' if right_box[1] == 'carrot' else 'Sorry! The computer'} won.")
    print('Please restart the program to play again.')


if __name__ == '__main__':
    main()
