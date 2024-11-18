from game import Game


g = Game()

while g.running:
    g.cur_menu.display_menu()
    g.dlc_play.run_display()
    g.game_loop()
