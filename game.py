import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from itertools import product


class Suit(Enum):
    HEARTS = ("copas", "♥")
    SPADES = ("espadas", "♠")
    DIAMONDS = ("ouros", "♦")
    CLUBS = ("paus", "♣")

    def __init__(self, name: str, icon: str):
        self.name = name
        self.icon = icon


# class State(ABC):
#     @abstractmethod
#     def fold(self): ...
#     @abstractmethod
#     def check(self): ...
#     @abstractmethod
#     def call(self): ...
#     @abstractmethod
#     def bet(self, amount: int): ...
#     @abstractmethod
#     def raise_(self, amount: int): ...
#     @abstractmethod
#     def skip(self): ...
#
#
# class PostingState(State):
#     pass
#
#
# class DealingState(State):
#     pass
#
#
# class PreFlopState(State):
#     pass
#
#
# class FlopState(State):
#     pass
#
#
# class TurnState(State):
#     pass
#
#
# class RiverState(State):
#     pass
#
#
# class ShowdownState(State):
#     pass


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: int

    def __post_init__(self):
        assert self.rank in range(1, 14)


class Deck:
    deck: list[Card]

    def __init__(self):
        self.deck = [Card(suit, rank) for (suit, rank) in product(Suit, range(1, 14))]
        random.shuffle(self.deck)

    def pick(self, n: int) -> list[Card]:
        if len(self.deck) == 0:
            return []

        n %= len(self.deck)
        picked = self.deck[:n]
        self.deck = self.deck[n:]
        return picked


class Table:
    cards: list[Card]

    def __init__(self, cards: list[Card]):
        self.cards = cards


@dataclass
class Hand:
    cards: list[Card]


@dataclass
class Player:
    name: str
    chips: int
    hand: Hand

    # def __init__(self, name: str, chips: float, hand: Hand):


class HumanPlayer(Player):
    pass


class ComputerPlayer(Player):
    def __init__(self, chips: int, hand: Hand):
        super().__init__("CPU", chips, hand)


class Round:
    # id: int
    # Quantas fichas constam na aposta da rodada
    # bet: int
    table: Table
    winner: Player

    def calc_winner(self):
        pass


class Game:
    # id: int
    # round: Round
    # chips: int
    # score: int
    # state: State

    # Quantas fichas constam no total
    # pot: int

    human_player: HumanPlayer
    computer_player: ComputerPlayer
    # player_order: tuple[Player, ...]

    def __init__(self, human_player_name: str, chips: int):
        # self.id = 0
        # self.chips = 1000
        # self.round = None
        # self.score = 0
        chips /= 2
        deck = Deck()

        # self.state = State.INIT
        self.human_player = HumanPlayer(
            human_player_name, math.floor(chips), Hand(deck.pick(2))
        )
        self.computer_player = ComputerPlayer(math.ceil(chips), Hand(deck.pick(2)))

    # def post_blinds(self):
    #     if self.player_order[0] is self.computer_player:
    #         pot = self.computer_player.chips
