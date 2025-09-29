import random
import textwrap
import time


def intro(prog: str) -> str:
    return textwrap.dedent(
        f"""
        {prog.upper()}
        
        Test your reaction time!
        
        If you see "DRAW!", you have 0.3 seconds to press <Enter>.
        You lose if you miss the 0.3 seconds.
        You also lose if you press <Enter> before you have seen "DRAW!".
        """
    ).strip()


def wait_for_enter(prompt: str) -> None:
    input(prompt)


def check_reaction_time(elapsed: float) -> str:
    if elapsed < .05:
        return 'You pressed enter before "DRAW!" appeared. You lose.'
    elif elapsed > .3:
        return f'You were too slow ({round(elapsed, 4)} seconds). You lose.'
    else:
        return f'You took {round(elapsed, 4)} seconds. This is impressive.'


def main(prog: str) -> None:
    print(intro(prog))
    wait_for_enter('\nPress <Enter> to begin.')

    while True:
        print('\nBe ready for the test ...')
        time.sleep(random.randint(20, 50) / 10.)

        print('DRAW!')
        draw_time = time.time()
        wait_for_enter('')
        print(check_reaction_time(time.time() - draw_time))

        print('Enter "(Q)uit" to stop, or press <Enter> to try again.')
        response = input('> ').strip().upper()

        if response in {'Q', 'QUIT'}:
            break

    print('Bye!')


if __name__ == '__main__':
    main('Fast Draw')
