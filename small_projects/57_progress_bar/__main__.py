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


def wipeout(bar: str) -> str:
    return '\b' * len(bar)


def main():
    print('     P r o g r e s s  B a r  S i m u l a t i o n')
    print(
        '(based on requirements and content originally created'
        '\n      by Al Swigart <al@inventwithpython.com>)\n')

    progress = 0
    total_work = 4096
    bar = ''
    dummy_text = 'https://www.example.com/download/very_large_archive.zip'
    progress_bar = new_progress_bar(dummy_text, solid='*')

    while progress < total_work:
        print(wipeout(bar), end='', flush=True)

        bar = progress_bar(progress, total_work)
        print(bar, end='', flush=True)

        time.sleep(0.1)

        progress += random.randint(10, 100)

    print('\b' * len(bar), end='', flush=True)
    bar = progress_bar(progress, total_work)
    print(bar, end='', flush=True)

    print('\n\nDone!')


main()
