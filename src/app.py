import tkinter as tk
from tkinter import messagebox
from src.game import *

CARD_W, CARD_H = 60, 84
RANK_NAMES = {2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",
              9:"9",10:"10",11:"J",12:"Q",13:"K",14:"A"}
SUIT_ICONS = {"HEARTS":"♥","DIAMONDS":"♦","CLUBS":"♣","SPADES":"♠"}
RED_SUITS  = {"HEARTS", "DIAMONDS"}


class CardWidget(tk.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, width=CARD_W, height=CARD_H, highlightthickness=0, **kw)
        self.card       = None
        self.face_down  = True
        self.draw()

    def show_face_down(self):
        self.card = None
        self.face_down = True
        self.draw()

    def show_card(self, card):
        self.card = card
        self.face_down = False
        self.draw()

    def show_empty(self):
        self.card = None
        self.face_down = False
        self.draw()

    def draw(self):
        self.delete("all")
        w, h = CARD_W, CARD_H

        if self.face_down:
            self.create_rectangle(0, 0, w, h, fill="navy", outline="gray")
            self.create_rectangle(4, 4, w-4, h-4, fill="", outline="white")
            return

        if self.card is None:
            self.create_rectangle(0, 0, w, h, fill="", outline="gray", dash=(4, 3))
            return

        suit_key = self.card.suit.name
        icon  = SUIT_ICONS[suit_key]
        rank  = RANK_NAMES.get(self.card.rank, str(self.card.rank))
        color = "red" if suit_key in RED_SUITS else "black"

        self.create_rectangle(0, 0, w, h, fill="white", outline="gray")
        self.create_text(4, 4,   text=rank, anchor="nw", fill=color)
        self.create_text(4, 16,  text=icon, anchor="nw", fill=color)
        self.create_text(w//2, h//2, text=icon, font=("TkDefaultFont", 20), fill=color)
        self.create_text(w-4, h-4,  text=rank, anchor="se", fill=color)
        self.create_text(w-4, h-16, text=icon, anchor="se", fill=color)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player = HumanPlayer("Player", 100)
        self.game   = Game(self.player)

        self.title("PokerPY")
        self.geometry("960x640")
        self.resizable(False, False)

        self.phase = None
        self.btn_nova_rodada = None

        self.build_welcome_screen()
        self.build_game_screen()
        self.show_welcome()

    def build_welcome_screen(self):
        self.welcome_frame = tk.Frame(self)

        self.welcome_frame.rowconfigure(0, weight=1)
        self.welcome_frame.rowconfigure(1, weight=0)
        self.welcome_frame.rowconfigure(2, weight=0)
        self.welcome_frame.rowconfigure(3, weight=1)
        self.welcome_frame.columnconfigure(0, weight=1)

        tk.Label(self.welcome_frame, text="Bem-vindo ao PokerPY!").grid(row=1, column=0, pady=(0, 16))
        tk.Button(self.welcome_frame, text="Começar jogo", command=self.on_start).grid(row=2, column=0)

    def build_game_screen(self):
        self.game_frame = tk.Frame(self)

        hud = tk.Frame(self.game_frame)
        hud.pack(fill="x", padx=10, pady=6)

        left_hud = tk.Frame(hud)
        left_hud.pack(side="left")
        self.bet_label = tk.Label(left_hud, text="Aposta: —")
        self.bet_label.pack(anchor="w")
        self.pot_label = tk.Label(left_hud, text="Pot: —")
        self.pot_label.pack(anchor="w")
        self.score_label = tk.Label(left_hud, text="Score: 0")
        self.score_label.pack(anchor="w")

        self.chips_label = tk.Label(hud, text="Fichas: 100")
        self.chips_label.pack(side="right", anchor="e")

        center = tk.Frame(self.game_frame)
        center.pack(fill="both", expand=True, padx=20)

        cpu_area = tk.Frame(center)
        cpu_area.pack(pady=(4, 2))
        tk.Label(cpu_area, text="CPU").pack()
        cpu_row = tk.Frame(cpu_area)
        cpu_row.pack()
        self.cpu_cards = [CardWidget(cpu_row) for _ in range(2)]
        for w in self.cpu_cards:
            w.pack(side="left", padx=4)

        table_area = tk.Frame(center, relief="sunken", bd=2)
        table_area.pack(pady=8, fill="x", ipady=10)
        tk.Label(table_area, text="Mesa").pack()
        table_row = tk.Frame(table_area)
        table_row.pack()
        self.table_cards = [CardWidget(table_row) for _ in range(5)]
        for w in self.table_cards:
            w.pack(side="left", padx=6)

        bottom = tk.Frame(center)
        bottom.pack(fill="x", pady=(6, 2))

        player_area = tk.Frame(bottom)
        player_area.pack()
        player_row = tk.Frame(player_area)
        player_row.pack()
        self.player_cards = [CardWidget(player_row) for _ in range(2)]
        for w in self.player_cards:
            w.pack(side="left", padx=4)
        tk.Label(player_area, text="Você").pack()

        action_area = tk.Frame(bottom)
        action_area.pack(side="right")

        raise_row = tk.Frame(action_area)
        raise_row.pack(anchor="e", pady=(0, 4))
        tk.Label(raise_row, text="Valor:").pack(side="left")
        self.bet_entry = tk.Entry(raise_row, width=6)
        self.bet_entry.pack(side="left", padx=4)

        btn_row = tk.Frame(action_area)
        btn_row.pack(anchor="e")
        self.btn_aumentar = tk.Button(btn_row, text="Aumentar", command=self.on_aumentar)
        self.btn_aumentar.pack(side="left", padx=4)
        self.btn_manter = tk.Button(btn_row, text="Manter", command=self.on_manter)
        self.btn_manter.pack(side="left", padx=4)
        self.btn_correr = tk.Button(btn_row, text="Correr", command=lambda: self.end(True))
        self.btn_correr.pack(side="left", padx=4)

        self.log_label = tk.Label(self.game_frame, text="", anchor="w", relief="groove", bd=1)
        self.log_label.pack(fill="x", side="bottom", padx=10, pady=6)

    def show_welcome(self):
        self.game_frame.pack_forget()
        self.welcome_frame.pack(fill="both", expand=True)

    def show_game(self):
        self.welcome_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def set_log(self, msg):
        self.log_label.config(text=f"  ▶  {msg}")

    def update_info(self):
        self.bet_label.config(text=f"Aposta: {self.game.round.bet}")
        self.pot_label.config(text=f"Pot: {self.game.round.pot}")
        self.score_label.config(text=f"Score: {self.game.score}")
        self.chips_label.config(text=f"Fichas: {self.player.get_chips()}")

    def set_buttons(self, enabled):
        state = "normal" if enabled else "disabled"
        self.btn_aumentar.config(state=state)
        self.btn_manter.config(state=state)
        self.btn_correr.config(state=state)
        self.bet_entry.config(state=state)

    def on_start(self):
        if self.btn_nova_rodada:
            self.btn_nova_rodada.destroy()
            self.btn_nova_rodada = None

        self.game.deck  = Deck()
        self.game.table = Table()
        self.game.round = None

        try:
            self.game.start()
        except ValueError as e:
            messagebox.showinfo("Game Over", str(e))
            self.set_log("Fim de jogo. Você ficou sem fichas.")
            self.set_buttons(False)
            self.destroy()
            return

        player_hand = self.player.get_hand().get_cards()
        self.player_cards[0].show_card(player_hand[0])
        self.player_cards[1].show_card(player_hand[1])

        for w in self.cpu_cards:
            w.show_face_down()
        for w in self.table_cards:
            w.show_empty()

        self.bet_label.config(text="Aposta: —")
        self.pot_label.config(text="Pot: —")
        self.chips_label.config(text=f"Fichas: {self.player.get_chips()}")

        self.phase = "bet_inicial"
        self.set_buttons(True)
        self.set_log("Cartas distribuídas. Insira um valor e clique em Aumentar para apostar.")
        self.show_game()

    def on_aumentar(self):
        try:
            val = int(self.bet_entry.get())
        except (ValueError, TypeError):
            messagebox.showerror("Valor inválido", "Preencha o campo com um inteiro positivo")
            return
        if val <= 0 or not self.player.check_limit(val):
            messagebox.showerror("Valor inválido", "Fichas insuficientes ou valor inválido")
            return

        if self.phase == "bet_inicial":
            self.game.round.simple_bet(val)
            self.update_info()
            self.flop()
        else:
            self.game.round.betting("aumentar", val)
            self.update_info()
            self.advance_phase()

    def on_manter(self):
        if self.phase == "bet_inicial":
            messagebox.showerror("Aposta obrigatória", "Insira um valor e clique em Aumentar para apostar.")
            return
        self.game.round.betting("continuar", 0)
        self.update_info()
        self.advance_phase()

    def advance_phase(self):
        if self.phase == "flop":
            self.turn()
        elif self.phase == "turn":
            self.river()
        elif self.phase == "river":
            self.end(False)

    def flop(self):
        self.game.round.flop()
        mesa = self.game.table.get_cards()
        for i in range(3):
            self.table_cards[i].show_card(mesa[i])
        self.phase = "flop"
        self.set_buttons(True)
        self.set_log("Flop! Três cartas na mesa. Aumente, mantenha ou corra.")

    def turn(self):
        self.game.round.turn()
        mesa = self.game.table.get_cards()
        self.table_cards[3].show_card(mesa[3])
        self.phase = "turn"
        self.set_buttons(True)
        self.set_log("Turn! Quarta carta revelada. Aumente, mantenha ou corra.")

    def river(self):
        self.game.round.turn()
        mesa = self.game.table.get_cards()
        self.table_cards[4].show_card(mesa[4])
        self.phase = "river"
        self.set_buttons(True)
        self.set_log("River! Última carta. Aumente, mantenha ou corra.")

    def end(self, desistencia):
        self.set_buttons(False)

        if desistencia:
            vencedor = self.game.cpu
        else:
            vencedor = self.game.round.calc_winner()
            if vencedor is self.player:
                self.player.add_chips(self.game.round.pot)
            elif vencedor is None:
                self.player.add_chips(self.game.round.pot // 2)

        self.game.update_score()
        self.update_info()

        cpu_hand = self.game.cpu.get_hand().get_cards()
        self.cpu_cards[0].show_card(cpu_hand[0])
        self.cpu_cards[1].show_card(cpu_hand[1])

        if desistencia:
            msg = "Você desistiu. CPU vence o pot."
        elif vencedor is None:
            msg = "Empate! Pot dividido."
        elif vencedor is self.player:
            msg = f"Você venceu! +{self.game.round.pot} fichas."
        else:
            msg = "CPU venceu esta rodada."

        self.set_log(msg)

        self.btn_nova_rodada = tk.Button(self.game_frame, text="Nova rodada", command=self.on_start)
        self.btn_nova_rodada.pack(side="bottom", pady=4)