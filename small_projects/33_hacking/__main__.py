"""
NOTE: This program requires the sevenletterwords.txt file. The original
file can be downloaded from https://inventwithpython.com
"""
import random
import sys
import textwrap
from functools import partial
from importlib import resources

open_local_text_file = partial(resources.open_text, __package__)


def load_sevenletterwords() -> list[str]:
    with open_local_text_file("sevenletterwords.txt") as f:
        words = [word.strip().upper() for word in f.readlines()]
    return words


def get_next_word(all_words: list[str], blocklist: list[str] = None) -> str:
    """Returns a random word from WORDS that isn't in blocklist."""
    if blocklist is None:
        blocklist = []

    while True:
        next_word = random.choice(all_words)
        if next_word not in blocklist:
            return next_word


def num_matches(*, secret_password, next_word) -> int:
    """Returns the number of matching letters in these two words."""
    matches = 0
    for i in range(len(secret_password)):
        if secret_password[i] == next_word[i]:
            matches += 1
    return matches


def get_words(all_words: list[str]) -> tuple[str, list[str]]:
    secret_password = random.choice(all_words)

    # noinspection PyListCreation
    words = [secret_password]  # Add the secret password first.

    while len(words) < 3:  # Add two words that do not match at all.
        next_word = get_next_word(all_words, blocklist=words)
        if num_matches(secret_password=secret_password, next_word=next_word) == 0:
            words.append(next_word)

    limit = 500
    while limit > 0:  # Try to add two words that have three matching characters.

        if len(words) == 5:
            break

        next_word = get_next_word(all_words, blocklist=words)
        if num_matches(secret_password=secret_password, next_word=next_word) == 3:
            words.append(next_word)

        limit -= 1

    limit = 500
    while limit > 0:  # Try to fill with words that have at least one matching character.

        if len(words) == 12:
            break

        next_word = get_next_word(all_words, blocklist=words)
        if num_matches(secret_password=secret_password, next_word=next_word) > 0:
            words.append(next_word)

        limit -= 1

    while len(words) < 12:  # Fill the list with up to 12 words, anyway.
        words.append(get_next_word(all_words, blocklist=words))

    random.shuffle(words)

    return secret_password, words


def get_computer_memory_string(words: list[str]) -> str:
    garbage = "~!@#$%^&*()_+-={}[]|;:,.<>?/"
    lines_with_words = random.sample(range(16 * 2), len(words))
    memory_address = 16 * random.randint(0, 4000)

    computer_memory = []

    next_word = 0

    for line_num in range(16):
        left_half = ""
        right_half = ""

        for j in range(16):
            left_half += random.choice(garbage)  # left column data for this line
            right_half += random.choice(garbage)  # right column data for this line

        # occasionally patch the word into the left column of memory locations line
        if line_num in lines_with_words:
            patch_location = random.randint(0, 9)
            left_half = (left_half[:patch_location]
                         + words[next_word]
                         + left_half[patch_location + 7:])
            next_word += 1

        # occasionally patch the word into the rigth column of memory locations line
        if line_num + 16 in lines_with_words:
            patch_location = random.randint(0, 9)
            right_half = (right_half[:patch_location]
                          + words[next_word]
                          + right_half[patch_location + 7:])
            next_word += 1

        computer_memory.append("0x" + hex(memory_address)[2:].zfill(4)
                               + "  " + left_half + "    "
                               + "0x" + hex(memory_address + (16 * 16))[2:].zfill(4)
                               + "  " + right_half)

        memory_address += 16

    return "\n".join(computer_memory)


class App:
    def __init__(self) -> None:
        self.secret_password, self.game_words = get_words(load_sevenletterwords())
        self.computer_memory = get_computer_memory_string(self.game_words)

    def run(self) -> None:
        self.intro()
        print(self.computer_memory + "\n")
        limit = 4
        while limit > 0:
            guess = self.ask_the_player(limit)

            if guess == self.secret_password:
                print("A C C E S S   G R A N T E D\n")
                return
            else:
                matches = num_matches(secret_password=self.secret_password, next_word=guess)
                print(f"Access denied (but {matches} out of seven characters correct).")

            limit -= 1

        print(f"\nOut of tries. The secret password was {self.secret_password}.\n")

    @staticmethod
    def intro() -> None:
        print(textwrap.dedent("""
        H a c k i n g   M i n i g a m e      by Al Sweigart (al@inventwithpython.com)
        
        Find the password in the computer's memory. You are given clues
        after each guess. For example, if the secret password is MONITOR
        but the you guessed CONTAIN, you are given the hint that two out
        of seven letters were correct, because MONITOR and CONTAIN have
        the letter O and N in their 2nd and 3rd letter.
        
        You get four guesses.
        """))

        input("Press Enter to begin ... ")

    def ask_the_player(self, tries_remaining: int) -> str:
        while True:
            print(f"Enter password ({tries_remaining} tries remaining):")
            guess = input("> ").upper()
            if guess in self.game_words:
                return guess
            else:
                print("This is not one of the possible passwords listed above.")
                print("Try again, entering one of the above listed words.")


try:
    App().run()
except KeyboardInterrupt:
    sys.exit()
