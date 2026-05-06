from src.suit import Suit
import random
from dataclasses import dataclass
from itertools import product

@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: int

    def __post_init__(self):
        assert self.rank in range(2, 14)


class Deck:
    deck: list[Card]

    def __init__(self):
        self.deck = [Card(suit, rank) for (suit, rank) in product(Suit, range(2, 14))]
        random.shuffle(self.deck)

    def pick(self, n: int) -> list[Card]:
        if len(self.deck) == 0:
            return []

        n %= len(self.deck)
        picked = self.deck[:n]
        self.deck = self.deck[n:]
        return picked