import tkinter as tk
from game import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player = HumanPlayer("Teste", 100)
        self.game = Game(self.player)

        self.title("PokerPY")
        self.geometry("960x960")

        tk.Label(self, text="Bem-vindo ao PokerPY!").pack(padx=5, pady=5)
        tk.Button(self, text="Começar jogo?", command=self.start).pack(padx=5, pady=5)

    def start(self):
        self.game.start()

        player_cards = []
        for c in self.player.get_hand().get_cards():
            player_cards.append([c.rank, c.suit.icon])

        tk.Label(self, text=player_cards).pack(padx=5, pady=5)
        
        tk.Label(self, text="Insira sua aposta: ").pack()
        bet = tk.Entry(self)
        bet.pack()
        tk.Button(self, text="Confirmar", command=lambda: self.flop(int(bet.get()))).pack()

    def flop(self, bet: int):
        self.game.round.simple_bet(bet)
        self.game.round.flop()

        table_cards = []
        for c in self.game.table.get_cards():
            table_cards.append([c.rank, c.suit.icon])
        
        tk.Label(self, text=table_cards).pack(padx=5, pady=5)

        bet = tk.Entry(self)
        bet.pack()
        tk.Button(self, text="Aumentar", command=lambda: self.turn("aumentar", int(bet.get()))).pack()
        tk.Button(self, text="Manter", command= lambda: self.turn("continuar", 0)).pack()
        tk.Button(self, text="Correr", command=lambda: self.turn("correr", 0)).pack()

    def turn(self, op: str, bet: int):
        self.game.round.betting(op, bet)
        self.game.round.turn()

        table_cards = []
        for c in self.game.table.get_cards():
            table_cards.append([c.rank, c.suit.icon])
        
        tk.Label(self, text=table_cards).pack(padx=5, pady=5)

        bet = tk.Entry(self)
        bet.pack()
        tk.Button(self, text="Aumentar", command=lambda: self.river("aumentar", int(bet.get()))).pack()
        tk.Button(self, text="Manter", command= lambda: self.river("continuar", 0)).pack()
        tk.Button(self, text="Correr", command=lambda: self.river("correr", 0)).pack()

    def river(self, op: str, bet: int):
        self.game.round.betting(op, bet)
        self.game.round.turn()

        table_cards = []
        for c in self.game.table.get_cards():
            table_cards.append([c.rank, c.suit.icon])
        
        tk.Label(self, text=table_cards).pack(padx=5, pady=5)

        cpu_cards = []
        for c in self.game.cpu.get_hand().get_cards():
            cpu_cards.append([c.rank, c.suit.icon])

        tk.Label(self, text=cpu_cards).pack()
        vencedor = self.game.round.calc_winner()
        tk.Label(self, text=f"O vencedor é: {vencedor.get_name()}").pack()