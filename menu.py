import pygame

from src import config, service
from objects import button

class Menu():
    def __init__(self, game):
        self.game = game
        self.run_display = True


    def base_background(self):
        self.game.display.fill('black')
        self.game.bg.draw(self.game.display)
        self.game.grd.draw(self.game.display)
        self.mouse_pos = pygame.mouse.get_pos()


    def blit_screen(self):
        self.game.check_events()
        self.game.window.blit(self.game.display, (0,0))
        self.game.clock.tick(config.FPS)
        pygame.display.update()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.start = button.Button(200,200,2,pygame.image.load("assets/ui_elements/play.png").convert_alpha())
    
    def display_menu(self):
        while self.run_display:
            self.base_background()

            service.draw_text("FlappyBird", 60, config.WIDTH/ 2, service.sine(100,2500,25,(config.HEIGHT / 6)), self.game.display)
            self.start.draw(self.game.display)
            self.start.click(self.mouse_pos)
            self.game.mouse_cursor()
            
            self.blit_screen()

        