from game import *

def main():
    player = HumanPlayer("Teste", 100)
    game = Game(player)
    game.start()

main()