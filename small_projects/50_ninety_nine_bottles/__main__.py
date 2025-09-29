import sys
import textwrap
import time
from string import Template

lyrics = Template(textwrap.dedent("""
$pre $pre_bottles of milk on the wall,
$pre $pre_bottles of milk,
Take one down, pass it around,
$post $post_bottles of milk on the wall!
""").lstrip())

PAUSE = 1


def intro():
    print(textwrap.dedent("""
    Ninety-Nine Bottles of Milk on the Wall
    (after Al Sweigart, al@inventwithpython.com)
        Press Ctrl-C to quit.
    """))


def slow_print(text: str) -> None:
    for line in text.splitlines():
        print(line)
        time.sleep(PAUSE)
    print()


def main() -> None:
    intro()
    bottles = 99

    while bottles:
        slow_print(lyrics.substitute(
            pre=bottles,
            post=bottles - 1 if bottles > 1 else "No more",
            pre_bottles="bottles" if bottles > 1 else "bottle",
            post_bottles="bottle" if bottles == 2 else "bottles",
        ))
        bottles -= 1
        time.sleep(PAUSE)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit()
