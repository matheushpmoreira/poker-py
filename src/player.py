from src.hand import Hand
from dataclasses import dataclass

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