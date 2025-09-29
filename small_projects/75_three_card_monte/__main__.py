import random
import textwrap
import time

from . import cards

LEFT = 0
MIDDLE = 1
RIGHT = 2

NUM_SWAPS = 16
DELAY= 0.8  # seconds  between card swaps


def intro(rendered_cards: str) -> str:
    return textwrap.dedent("""
    Three Card Monte
    
    Find the red lady (the Queen of Hearts).
    Keep an eye on how the cards move.
    
    Here are the cards:
    {}
    Press ENTER when you are ready to begin.
    """).format(rendered_cards).strip()


PAIRS = "lm mr lr ml rm rl".split()
INDEX = dict(zip("lmr", (LEFT, MIDDLE, RIGHT)))
POSITION = dict(zip("lmr", "left middle right".split()))


def swap_two_cards(triple: list[cards.Card]) -> str:
    a, b = random.choice(PAIRS)
    triple[INDEX[a]], triple[INDEX[b]] = triple[INDEX[b]], triple[INDEX[a]]
    return f"Swapping {POSITION[a]} and {POSITION[b]}."


def ask_player(question: str, choices: list[str]) -> str:
    choice = ""
    while not choice:
        print(question)
        answer = input("> ").strip()
        if len(answer) == 0:
            continue
        choice = answer.lower()
        if choice not in choices:
            print(f"'{answer}' is not in {list(choices)}. Try again.")
            choice = ""
            continue
    return choice



def main():
    triple = cards.make_triple()
    print(intro(cards.render(triple)))
    input()

    for _ in range(NUM_SWAPS):
        print(swap_two_cards(triple))
        time.sleep(DELAY)

    for _ in range(60):  # Clear screen.
        print()

    answer = ask_player(
        "Which card is the queen of hearts? (L)eft, (M)iddle or (R)ight.",
        choices=list("lmr"),
    )

    print(cards.render(triple))
    print("You won." if triple[INDEX[answer]] == cards.QUEEN_OF_HEARTS else "You lost.")
    print("Thanks for playing.")


if __name__ == '__main__':
    main()
