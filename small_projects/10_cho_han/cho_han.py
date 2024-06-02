"""
Cho-han bakuchi
From Wikipedia, the free encyclopedia

Cho-Han Bakuchi (or Cho Ka Han Ka, or simply Cho-Han) is a traditional Japanese gambling game using dice.

The game uses two standard six-sided dice, which are shaken in a bamboo cup or bowl by a dealer.
The cup is then overturned onto the floor. Players then place their wagers on whether the sum total
of numbers showing on the two dice will be "Cho" (even) or "Han" (odd). The dealer then removes the cup,
displaying the dice. The winners collect their money.

Depending on the situation, the dealer will sometimes act as the house, collecting all losing bets.
But more often, the players will bet against each other (this requires an equal number of players betting
on odd and even), and the house will collect a set percentage of winning bets.

The game was a mainstay of the bakuto, itinerant gamblers in old Japan, and is still played by the modern yakuza.
In a traditional Cho-Han setting, players sit on a tatami floor. The dealer sits in the formal seiza
position and is often shirtless (to prevent accusations of cheating), exposing his elaborate tattoos.
"""
import random

die_face = ['ICHI', 'NI', 'SAN', 'SHI', 'GO', 'ROKU']


def cho_han_bakuchi() -> tuple[str, int, str, int, str]:
    dice = random.choices((1, 2, 3, 4, 5, 6), k=2)
    total = sum(dice)
    return die_face[dice[0] - 1], dice[0], die_face[dice[1] - 1], dice[1], ['CHO', 'HAN'][total % 2]


if __name__ == "__main__":
    print(cho_han_bakuchi())
