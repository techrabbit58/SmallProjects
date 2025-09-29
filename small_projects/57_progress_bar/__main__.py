import argparse
import itertools
import random
import time
from collections.abc import Callable


def new_progress_bar(text='', *, width=40, solid=chr(9608), space=' ') -> Callable[[int, int], str]:
    def render_progress_bar(progress: int, total_work: int) -> str:
        progress = 0 if progress < 0 else progress if progress < total_work else total_work
        length = int(width * progress / total_work)

        return (f'[{solid * length}{space * (width - length)}] '
                f'{progress * 100 / total_work:4.1f}%  {progress}/{total_work}  '
                f'{text}')

    return render_progress_bar


def new_progress_spinner(text='', *, symbols='|/-\\') -> Callable[[int, int], str]:
    phase = itertools.cycle(symbols)

    def render_spinner(progress: int, total_work: int) -> str:
        progress = 0 if progress < 0 else progress if progress < total_work else total_work

        return (f'{"OK" if progress == total_work else (" " + next(phase))}  '
                f'{progress * 100 / total_work:4.1f}%  {progress}/{total_work}  '
                f'{text}')

    return render_spinner


def wipeout(bar: str) -> str:
    return '\b' * len(bar)


def main(prog: str):
    print('\n     P r o g r e s s  B a r  S i m u l a t i o n')
    print(
        '(based on requirements and content originally created'
        '\n      by Al Swigart <al@inventwithpython.com>)\n')

    parser = argparse.ArgumentParser(prog, description='Simulate a progress bar or spinner.')
    parser.add_argument('--style', choices='bar spinner'.split(), default='bar',
                        help='show a progress bar or a progress spinner (default: bar)')
    args = parser.parse_args()

    progress = 0
    total_work = 4096
    line = ''
    dummy_text = 'https://www.example.com/download/very_large_archive.zip'
    visualizer = new_progress_spinner(dummy_text) \
        if args.style == 'spinner' else new_progress_bar(dummy_text, solid='*')

    while progress < total_work:
        print(wipeout(line), end='', flush=True)

        line = visualizer(progress, total_work)
        print(line, end='', flush=True)

        time.sleep(0.1)

        progress += random.randint(10, 100)

    print('\b' * len(line), end='', flush=True)
    line = visualizer(progress, total_work)
    print(line, end='', flush=True)

    print('\n\nDone!\n')


if __name__ == '__main__':
    main('Show Progress')
