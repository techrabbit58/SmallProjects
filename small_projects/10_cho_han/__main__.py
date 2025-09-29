import textwrap
from abc import ABC
from typing import TypeVar

from .cho_han import cho_han_bakuchi


def intro():
    return textwrap.dedent("""
    Cho-Han Bakuchi (or Cho Ka Han Ka, or simply Cho-Han) is a traditional Japanese gambling game using dice.
    
    The game uses two standard six-sided dice, which are shaken in a bamboo cup or bowl by a dealer (the computer.)
    The cup is then overturned onto the floor. Players then make their bets on whether the sum total
    of numbers showing on the two dice will be "Cho" (even) or "Han" (odd). The dealer then removes the cup,
    displaying the dice. The winners collect their money.
    
    Depending on the situation, the dealer will sometimes act as the house, collecting all losing bets.
    Sometimes the players will bet against each other (this requires an equal number of players betting
    on odd and even), and the house will collect a set percentage of winning bets.
    
    This program simulates you playing against another player. The other player always holds for the opposite
    of your bet, with an equal sum. If you win, the house collects five percent of your win. You start with
    5000 money. The game ends if you quit, or latest if you are broke.
    """)


T = TypeVar('T')


class Result(ABC):
    def __init__(self, value: T) -> None:
        self.value = value


class Error(Result):
    pass


class Fatal(Result):
    pass


class Ok(Result):
    pass


def get_bet(money: int) -> Result:
    bet = 0
    try:
        bet = input('Your bet, or quit? ').lower()
        if 'quit'.startswith(bet):
            return Fatal('You decided to leave the game.')

        bet = int(bet)
        if not 1 <= bet <= money:
            raise ValueError()

        return Ok(bet)

    except ValueError:
        return Error(f'Your bet must be in the range 1 to {money}. Your bet {bet} is not.')

    except KeyboardInterrupt:
        return Fatal('You suddenly jumped out of the game.')


def get_guess() -> Result:
    try:
        guess = input('What is your guess? (CHO/HAN) ').upper()
        if guess not in {'CHO', 'HAN'}:
            return Error(f'You must decide for "CHO" (even) or "HAN" (odd). Your input "{guess}" is not valid.')
        return Ok(guess)
    except KeyboardInterrupt:
        return Fatal('You unexpectedly jumped out in the middle of a guess.')


def main():
    print(intro())

    money = 5_000

    while money > 0:
        print(f'You have {money} money. How much do you bet?')

        bet, answer = 0, get_bet(money)
        if isinstance(answer, Fatal):
            print(answer.value)
            print(f"You still have {money} money. Hope we'll see you again soon.")
            print('Thank you for playing.')
            return
        elif isinstance(answer, Error):
            print(answer.value)
            print(f'Please enter a valid bet. This is a positive integer number up to {money} money.')
            continue
        else:
            bet = answer.value

        print('The dealer swirls the cup. You her the two dice falling inside.')
        print('The dealer slams the cup on the floor, with the fallen dice still covered.')
        die1, face1, die2, face2, result = cho_han_bakuchi()

        print('The dealer asks for your guess.')

        guess = get_guess()
        if isinstance(guess, Fatal):
            print(guess.value)
            print(f'Your last bet is lost. You have {money - int(bet)} money left.')
            print('Thank you for playing.')
            return
        elif isinstance(guess, Error):
            print(guess.value)
            continue

        print('The dealer now raises the cup and you can see the dice:')
        print(textwrap.indent(textwrap.dedent(f"""
            {die1:>4} - {die2:<4}
            {face1:>4} - {face2:<4}          {result}
        """), '    '))

        if guess.value == result:
            print('You win! The house collects a fee of five percent.')
            fee = (bet * 5) // 100
            money += bet - fee
        else:
            print('You lose.')
            money -= bet

    # This point gets reached if your remaining money falls to zero.
    print('You are broke. Fortunately, the money you lost was not real.')
    print('Bye.')


if __name__ == '__main__':
    main()
