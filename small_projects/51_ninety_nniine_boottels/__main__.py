import os
import random
import sys
import time
from typing import TypeAlias

TITLE = "n i N e t y - n n i i n E   B o O t t e l s\n"

BOTTLES = 99
DRINK = "beer"
CHAR_PAUSE = 0.01
VERSE_PAUSE = 3


def clear_screen(clear: str = "cls" if sys.platform == "win32" else "clear"):
    os.system(clear)


def bottelize(number: int, drink: str) -> str:
    tens = ["", "Ten", "Twenty", "Thirty", "Fourty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"][(number // 10)]
    ones = ["", "-One", "-Two", "-Three", "-Four", "-Five", "-Six", "-Seven", "-Eight", "-Nine"][number % 10]

    if 20 <= number <= 99:
        word = f"{tens}{ones.lower()}"
    elif 11 <= number <= 19:
        word = "Eleven Twelve Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen".split()[number - 11]
    elif 2 <= number <= 10:
        word = f"{tens}{ones[1:]}"
    elif number == 1:
        word = "One"
    else:
        word = "No more"

    return f"{word} bottle{'' if number == 1 else 's'} of {drink}"


Stanza: TypeAlias = tuple[str, str, str, str]


def versify(number: int, drink: str) -> Stanza:
    this_number = bottelize(number, drink)
    next_number = bottelize(number - 1, drink)

    stanza = (
        f"{this_number} on the wall,",
        f"{this_number}.",
        f"Take {'one' if number > 1 else 'it'} down, pass it around,",
        f"{next_number} on the wall.",
    )

    return stanza


def slow_print(text: str, char_pause: float) -> None:
    for char in text:
        print(char, end="", flush=True)
        if char.isalnum():
            time.sleep(char_pause)
    print()


def erase_one_random_char(chars: list[str]) -> list[str]:
    num_chars = len(chars) - chars.count(" ")
    to_be_changed = random.randrange(num_chars)
    index = 0
    char_index = 0
    while index < num_chars:
        if chars[index].isalnum():
            if char_index == to_be_changed:
                chars[index] = " "
                break
            char_index += 1
        index += 1
    return chars


def change_case_of_one_random_character(chars: list[str]) -> list[str]:
    num_chars = len(chars) - chars.count(" ")
    to_be_changed = random.randrange(num_chars)
    index = 0
    char_index = 0
    while index < num_chars:
        if chars[index].isalnum():
            if char_index == to_be_changed:
                chars[index] = chars[index].lower() if chars[index].isupper() else chars[index].upper()
                break
            char_index += 1
        index += 1
    return chars


def transpose_one_random_character_pair(chars: list[str]) -> list[str]:
    num_chars = len(chars) - chars.count(" ")
    for p in range(len(chars) - 1):
        q = p + 1
        if chars[p].isalnum() and chars[q].isalnum() and random.randrange(num_chars):
            chars[p], chars[q] = chars[q], chars[p]
            break
    return chars


def double_one_random_character(chars: list[str]) -> list[str]:
    num_chars = len(chars) - chars.count(" ")
    to_be_changed = random.randrange(num_chars)
    index = 0
    char_index = 0
    while index < num_chars:
        if chars[index].isalnum():
            if char_index == to_be_changed:
                chars.insert(char_index, chars[index])
                break
            char_index += 1
        index += 1
    return chars


applicable_effects = [
    erase_one_random_char,
    change_case_of_one_random_character,
    transpose_one_random_character_pair,
    double_one_random_character,
]


def distort(verse: str, bottles_left: int, bottles_max: int) -> str:
    bottles_done = bottles_max - bottles_left
    chars = list(verse)
    if bottles_done:
        for _ in range(1 + (bottles_done // 2)):
            if random.randrange(bottles_done):
                effect = random.randrange(len(applicable_effects))
                chars = applicable_effects[effect](chars)
    return " ".join("".join(chars).split())


def main() -> None:
    for number in range(BOTTLES, 0, -1):
        clear_screen()
        print(TITLE)

        print(f"{'No' if number == BOTTLES else (BOTTLES - number)} bottle{'' if number == 98 else 's'} done.\n")

        stanza = versify(number, DRINK)
        for verse in stanza:
            verse = distort(verse, number, BOTTLES)
            slow_print(verse, CHAR_PAUSE)

        print()
        time.sleep(VERSE_PAUSE)

    clear_screen()
    print(TITLE)
    print("No bottles left.\n")
    stanza = versify(0, DRINK)
    for verse in stanza:
        slow_print(verse, CHAR_PAUSE)
    print()
    print("Thanks for playing.\n")


try:
    main()
except KeyboardInterrupt:
    pass
