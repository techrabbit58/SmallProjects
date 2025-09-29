import random
import re
import textwrap

intro = textwrap.dedent("""
    This simulates dice rolls using the Dungeons & Dragons dice roll notation.
    Type in dice roll commands like "3d6" or "1d10+2".
    """).strip()

help_ = textwrap.dedent("""
    The dice roll command schema is:
        number_of_dice "d" number_sides_of_dice ("+"|"-") number_adjust_after_roll.
    
    Examples:
        3d6     roll three 6-sided dice
        1d10+2  roll one 10-sided dice and adjust the result by adding 2
        2d38-1  roll two 38-sided dice and subtract 1 from the result
        q[uit]  quit the program
        c[lear] reset the repeat buffer
    """).strip()


def main() -> None:
    regex = re.compile(r'(\d+)d(\d+)([+-]\d+)?')

    print(intro)

    last_answer = ''

    while True:
        answer = ''

        try:
            answer = input('> ').strip().lower()
        except KeyboardInterrupt:
            pass

        if answer and 'quit'.startswith(answer):
            break

        if answer and 'clear'.startswith(answer):
            last_answer = ''
            continue

        if not answer and last_answer:
            answer = last_answer
            print('repeated:', answer)

        result = regex.fullmatch(answer)
        if result is None:
            print(help_)
            continue

        last_answer = answer
        num_dice, dice_faces, adjust = [0 if item is None else int(item) for item in result.groups()]

        pips = []

        for _ in range(num_dice):
            pips.append(random.randint(1, dice_faces))

        if not pips:
            print('You cannot roll zero dice. The number of dice may not be zero. Try again, please.')
            last_answer = ''
            continue

        if adjust:
            pips.append(adjust)

        total = sum(pips)

        print(total, f'({", ".join(str(n) for n in (pips[:-1] if adjust else pips))}'
                     f'{f", {pips[-1]:+d}" if adjust else ""})')

    print('Bye.')


if __name__ == '__main__':
    main()
