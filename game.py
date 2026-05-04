import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from itertools import product, combinations
from collections import Counter

class Suit(Enum):
    HEARTS = ("copas", "♥")
    SPADES = ("espadas", "♠")
    DIAMONDS = ("ouros", "♦")
    CLUBS = ("paus", "♣")

    def __init__(self, name: str, icon: str):
        self.display_name = name
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


class Table:
    _cards: list[Card]

    def __init__(self):
        self._cards = list()

    def get_cards(self):
        return self._cards

    def new_card(self, card: Card):
        self._cards.append(card)


@dataclass
class Hand:
    _cards: list[Card]

    def __init__(self):
        self._cards = list()

    def get_cards(self):
        return self._cards

    def new_hand(self, cards: list[Card]):
        self._cards = cards

@dataclass
class Player:
    _name: str
    _hand: Hand

    def __init__(self, name: str):
        self._name = name
        self._hand = Hand()

    def get_name(self):
        return self._name
    
    def get_hand(self):
        return self._hand
    

class HumanPlayer(Player):
    chips: int

    def __init__(self, name: str, chips: int):
        super().__init__(name)
        self._chips = chips

    def get_chips(self):
        return self._chips
    
    def set_chips(self, chips):
        self._chips = chips

    def discount_chips(self, chips):
        self._chips -= chips

    def add_chips(self, chips):
        self._chips += chips

    def check_limit(self, chips: int):
        if chips > self._chips:
            return False
        return True


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__("CPU")


class Round:
    bet: int
    pot: int
    deck: Deck
    player: HumanPlayer
    cpu: ComputerPlayer
    table: Table

    def __init__ (self, deck: Deck, player: HumanPlayer, cpu: ComputerPlayer, table: Table):
        self.bet = 0
        self.pot = 0
        self.deck = deck
        self.player = player
        self.cpu = cpu
        self.table = table

    def evaluate_hand(self, cards: list[Card]) -> tuple:
        ranks = sorted([c.rank for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        counts = Counter(ranks)
        freq = sorted(counts.values(), reverse=True)  # ex: [2,2,1] = dois pares

        is_flush = len(set(suits)) == 1
        # Trata Ás-baixo: A-2-3-4-5
        unique = sorted(set(ranks))
        is_straight = (unique == list(range(unique[0], unique[0] + 5)))

        # Os ranks agrupados por frequência (ex: trinca primeiro, depois kickers)
        groups = sorted(counts.keys(), key=lambda r: (counts[r], r), reverse=True)

        if is_straight and is_flush:
            if ranks[0] == 13:  # Royal Flush
                return (9, ranks)
            return (8, groups)
        if freq == [4, 1]:   return (7, groups)
        if freq == [3, 2]:   return (6, groups)
        if is_flush:         return (5, groups)
        if is_straight:      return (4, groups)
        if freq == [3,1,1]:  return (3, groups)
        if freq == [2,2,1]:  return (2, groups)
        if freq == [2,1,1,1]:return (1, groups)
        return (0, groups)  # High card

    def best_hand(self, cards: list[Card]) -> tuple:
        return max(self.evaluate_hand(list(combo)) for combo in combinations(cards, 5))

    def calc_winner(self) -> Player:
        all_cards_human = self.player.get_hand().get_cards() + self.table.get_cards()
        all_cards_cpu = self.cpu.get_hand().get_cards() + self.table.get_cards()

        score_h = self.best_hand(all_cards_human)
        score_c = self.best_hand(all_cards_cpu)

        if score_h > score_c: return self.player
        if score_c > score_h: return self.cpu
        return None  # Empate — split pot

    def deal(self):
        self.player.get_hand().new_hand(self.deck.pick(2))
        self.cpu.get_hand().new_hand(self.deck.pick(2))

    def flop(self):
        for i in range(3):
            self.table.new_card(self.deck.pick(1)[0])

    def turn(self):
        self.table.new_card(self.deck.pick(1)[0])

    def simple_bet(self):
        bet = int(input("Aposta inicial?\n"))
        if self.player.check_limit(bet):
            self.bet = bet
            self.player.discount_chips(bet)
            self.pot = 2 * bet
        
    def betting(self):
        ''' Tem que ver como vai ser implementado a interface para fazer isso aqui, mas a princípio
        são 3 opções, continuar, aumentar ou correr, e aí dá pra ver de implementar a lógica de escolha da CPU'''
        pass

class Game:
    round: Round
    score: int
    # state: State

    player: HumanPlayer
    cpu: ComputerPlayer
    table: Table
    # player_order: tuple[Player, ...]

    def __init__(self, player: HumanPlayer):
        self.player = player
        self.round = None
        self.score = 0
        self.table = Table()
        self.cpu = ComputerPlayer()
        self.deck = Deck()

    '''
        # self.state = State.INIT
        self.human_player = HumanPlayer(
            human_player_name, math.floor(chips), Hand(deck.pick(2))
        )
        self.computer_player = ComputerPlayer(math.ceil(chips), Hand(deck.pick(2)))
    '''

    # def post_blinds(self):
    #     if self.player_order[0] is self.computer_player:
    #         pot = self.computer_player.chips

    def start(self):
        self.round = Round(self.deck, self.player, self.cpu, self.table)
        self.round.deal()
        self.round.simple_bet()
        self.round.flop()

        print("Aposta de: ", self.round.bet)
        print("Valendo: ", self.round.pot)
        print("Cartas do player: ", self.player.get_hand().get_cards())
        print("Cartas da casa: ", self.cpu.get_hand().get_cards())
        print("Cartas na mesa: ", self.table.get_cards())

        self.round.turn()
        print("Mesa agora: ", self.table.get_cards())
        self.round.turn()
        print("Mesa final: ", self.table.get_cards())

        vencedor = self.round.calc_winner()
        print("O vencedor desta rodada é: ", vencedor)