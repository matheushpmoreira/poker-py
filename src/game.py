from src.player import *
from src.deck import Deck, Card
from src.table import Table
from itertools import combinations
from collections import Counter

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

    def simple_bet(self, value: int):
        if self.player.check_limit(value):
            self.bet = value
            self.player.discount_chips(value)
            self.pot = 2 * value

    def betting(self, option: str, val: int):
        if option == "continuar":
            pass
        elif option == "aumentar":
            if self.player.check_limit(val):
                self.player.discount_chips(val)
                self.bet += val
                self.pot += val * 2
        else:
            raise ValueError(f"Unexpected betting option: {option}")

class Game:
    round: Round
    score: int

    player: HumanPlayer
    cpu: ComputerPlayer
    table: Table

    def __init__(self, player: HumanPlayer):
        self.player = player
        self.round = None
        self.score = 0
        self.table = Table()
        self.cpu = ComputerPlayer()
        self.deck = Deck()

    def start(self):
        if self.player.get_chips() <= 0:
            raise ValueError("Jogador sem fichas. O jogo acabou.")
        
        self.round = Round(self.deck, self.player, self.cpu, self.table)
        self.round.deal() 

    def update_score(self):
        if self.player.get_chips() > self.score:
            self.score = self.player.get_chips()