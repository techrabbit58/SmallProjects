import random


class App:
    range = 1, 100  # inclusive range: 1, 2, 3, ..., 100
    num_guesses = 7  # Give the player some guesses.

    def __init__(self, title: str) -> None:
        self.title = title
        self.secret_number = random.randint(*self.range)
        self.guess: int | None = None

    def run(self) -> None:
        print(f"\nAl Sweigart's \"{self.title}\" Game (al@inventwithpython.com)")
        print("   *** Refactored Version ***\n")

        lo, hi = self.range
        print(f"Computer: I am thinking of a number between {lo} and {hi}.")

        for i in range(self.num_guesses):
            self.ask_for_a_guess(remaining_guesses=self.num_guesses - i)

            if self.guess < self.secret_number:
                print("Computer: Your guess is too low.")
            elif self.guess > self.secret_number:
                print("Computer: Your guess is too high.")
            else:
                print("\nComputer: Yay! You guessed my secret number. You won.")
                break
        else:
            print(f"\nComputer: Game over. The number I was thinking of was {self.secret_number}.")

        print("\nDone.\n")

    def ask_for_a_guess(self, *, remaining_guesses: int) -> None:
        print(f"Computer: You have {remaining_guesses} guesses left. Take a guess.")

        self.guess = None
        while not self.guess:
            given = input("You: ")
            guess = int(given) if given.isdecimal() else -1

            lo, hi = self.range
            if not lo <= guess <= hi:
                print(f"Computer: Please enter a number between {lo} and {hi}.")
                continue

            self.guess = guess


if __name__ == '__main__':
    App("Guess The Number").run()
