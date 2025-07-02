class App:
    def __init__(self, title: str) -> None:
        self.title = title

    def run(self) -> None:
        self.intro()
        self.keep_user_busy()
        self.finish()

    def intro(self):
        print(f"\n{self.title}")
        print("by Al Sweigart (al@inventwithpython.com)")
        print("*** Refactored Version ***\n")

    @staticmethod
    def finish():
        print("\nComputer: Thank you. Have a nice day.\n")

    @staticmethod
    def keep_user_busy() -> None:
        while True:
            print("Computer: Do you want to know how to keep a gullible person busy for hours?")
            response = input("You (Yes or No): ").strip().lower()

            if response in ("n", "no"):
                break
            if response not in ("y", "yes"):
                print("Computer: This is not a valid response. Please try again")

App("G U L L I B L E").run()
