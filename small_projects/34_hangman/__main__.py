import random
import string
import sys

BANNER = """
H A N G M A N       by Al Sweigart (al@inventwithpython)
                    *** refactored version ***
"""

CATEGORY = "Animals"

WORDS = """
aardvark platypus kangaroo spider bee elephant orca crocodile
ant baboon badger bat bear beaver camel cat clam cobra cougar 
coyote crow deer dog donkey duck eagle ferret fox frog horse
goat goose hawk lion lizard llama mole monkey moose mule newt
otter owl panda parrot pigeon python rabbit ram rat raven rhino
racoon salmon shark sheep skunk sloth snake stork swan chicken
tiger toad trout turkey turtle weasel whale wolf zebra fly
mosquito bonobo squirrel anaconda reindeer grizzly sparrow
swift starling nightingale larch swallow
""".upper().strip().split()

IMAGES = (
    [" +--+"] * 7,
    [" |  |"] * 7,
    "    |. O  |. O  |. O  |. O  |. O  |. O  |".split("."),
    "    |.    |. |  |./|  |./|\ |./|\ |./|\ |".split("."),
    "    |.    |.    |.    |.    |./   |./ \ |".split("."),
    ["    |"] * 7,
    ["====="] * 7,
)


def hangman(n: int) -> str:
    return "\n".join(s[n] for s in IMAGES)


class App:
    def __init__(self) -> None:
        self._secret_word = random.choice(WORDS)
        self.num_guesses = len(IMAGES[0])
        self.missed_letters = set()
        self.correct_letters = set()

    def run(self) -> None:
        print(BANNER)

        while True:
            print(hangman(len(self.missed_letters)))
            print(self.status)
            print(self.disguise)

            guess = self.get_a_guess()

            if guess in self._secret_word:
                self.correct_letters.add(guess)
            else:
                self.missed_letters.add(guess)

            if self.correct_letters == set(self._secret_word):
                print(f"\nYes! The secret word is: {self._secret_word}")
                print("You have won!\n")
                break

            misses = len(self.missed_letters)
            if len(self.missed_letters) == self.num_guesses - 1:
                print(hangman(misses))
                print("\nYou have run out of guesses. You loose.")
                print(f"The secret word was: {self._secret_word}\n")
                break

    @property
    def disguise(self) -> str:
        sw = [ch if ch in self.correct_letters else "_" for ch in self._secret_word]
        return f'Correct letters: {" ".join(sw)}\n'

    @property
    def status(self) -> str:
        ml = " ".join(self.missed_letters) if self.missed_letters else "No missed lettes yet."
        message = [
            f"The category is: {CATEGORY}",
            f"Missed letters: {ml}",
        ]
        return "\n".join(message)

    def get_a_guess(self) -> str:
        while True:
            print("Guess a letter.")
            guess = input("> ").strip()
            if len(guess) != 1:
                print("Please enter a SINGLE LETTER. Try again.")
            elif guess.upper() in self.correct_letters | self.missed_letters:
                print("you have already guessed that letter. Try again.")
            elif guess not in string.ascii_letters:
                print(f"Please enter an ASCII LETTER. '{guess}' is NOT ASCII. Try again.")
            else:
                return guess.upper()


try:
    App().run()
except KeyboardInterrupt:
    sys.exit()
