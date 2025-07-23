import random
from typing import TypeAlias

Rank: TypeAlias = str
Suit: TypeAlias = str
Card: TypeAlias = tuple[Rank, Suit]

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

QUEEN_OF_HEARTS = ("Q", HEARTS)


def render(cards: list[Card]) -> str:
    rows: list[list[str]] = [list() for _ in range(5)]

    for i, card in enumerate(cards):
        rank, suit = card
        rows[0].append(" ___  ")
        rows[1].append("|{} | ".format(rank.ljust(2)))
        rows[2].append("| {} | ".format(suit))
        rows[3].append("|_{}| ".format(rank.rjust(2, "_")))

    return "\n".join(" ".join(row) for row in rows)


RANKS = ["10"] + list("23456789JQKA")
SUITS = HEARTS, SPADES, DIAMONDS, CLUBS

def add_random_cards(cards: list[Card], *, num_cards_to_add: int) -> None:
    while num_cards_to_add:
        rank = random.choice(RANKS)
        suit = random.choice(SUITS)
        card = (rank, suit)
        if card not in cards:
            cards.append(card)
            num_cards_to_add -= 1
    random.shuffle(cards)


def make_triple() -> list[Card]:
    triple = [QUEEN_OF_HEARTS]
    add_random_cards(triple, num_cards_to_add=2)
    return triple