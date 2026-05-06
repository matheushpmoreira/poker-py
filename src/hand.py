from src.deck import Card
from dataclasses import dataclass

@dataclass
class Hand:
    _cards: list[Card]

    def __init__(self):
        self._cards = list()

    def get_cards(self):
        return self._cards

    def new_hand(self, cards: list[Card]):
        self._cards = cards