import collections.abc
import itertools
import random
from typing import NamedTuple, Self

_suits = dict(diamonds=chr(0x2666), hearts=chr(0x2665), spades=chr(0x2660), clubs=chr(0x2663))
_ranks = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
_points = dict(zip(_ranks, [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]))


class Card(NamedTuple):
    suit: str
    rank: str
    points: int

    def face_up(self) -> list[str]:
        return [
            ' ___ ',
            f'|{self.rank.ljust(2)} |',
            f'| {_suits[self.suit]} |',
            f'|_{self.rank.rjust(2, "_")}|',
        ]

    @staticmethod
    def face_down() -> list[str]:
        return [
            ' ___ ',
            '|## |',
            '|###|',
            '|_##|',
        ]


class Deck(collections.abc.Sized):
    def __init__(self):
        self._cards = list(itertools.product(_suits, _ranks))
        random.shuffle(self._cards)

    def pop(self) -> Card:
        suit, rank = self._cards.pop()
        return Card(suit, rank, _points[rank])

    def __len__(self) -> int:
        return len(self._cards)


class Hand:
    _cards: list[Card]

    def __init__(self) -> None:
        self._cards = []

    def add(self, *cards: Card) -> Self:
        for card in cards:
            self._cards.append(card)
        return self

    def score(self) -> int:
        worth = num_aces = 0
        for card in self._cards:
            if card.rank == 'A':
                num_aces += 1
            worth += _points[card.rank]
        for _ in range(num_aces):
            if worth + 10 <= 21:
                worth += 10
            else:
                break
        return worth

    def as_display_str(self, *, hide_first_card: bool = False) -> str:
        start = 0
        if hide_first_card:
            rows = [[line] for line in self._cards[0].face_down()]
            start = 1
        else:
            rows = [[] for _ in range(4)]
        for card in self._cards[start:]:
            for row, line in enumerate(card.face_up()):
                rows[row].append(line)
        return '\n'.join(" ".join(line) for line in rows)

    def score_to_str(self, tag: str, *, hide: bool = False) -> str:
        return f'{tag}: {"???" if hide else self.score()}'

    def card_count(self):
        return len(self._cards)
