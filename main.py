from game import Game


g = Game()

while g.running:
    g.cur_menu.display_menu()
    g.game_loop()
