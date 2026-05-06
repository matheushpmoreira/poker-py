from enum import Enum

class Suit(Enum):
    HEARTS = ("copas", "♥")
    SPADES = ("espadas", "♠")
    DIAMONDS = ("ouros", "♦")
    CLUBS = ("paus", "♣")

    def __init__(self, name: str, icon: str):
        self.display_name = name
        self.icon = icon