from src.deck import Card

class Table:
    _cards: list[Card]

    def __init__(self):
        self._cards = list()

    def get_cards(self):
        return self._cards

    def new_card(self, card: Card):
        self._cards.append(card)