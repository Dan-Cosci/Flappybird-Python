import pygame
import random
import time

from objects import background, bird, ground, pipe
from src import config, service
from menu import MainMenu, Restart_menu



class DLC():
    def __init__(self,  game):
        self.game = game

    def base_background(self):
        self.game.display.fill('black')
        self.game.bg.draw(self.game.display)
        self.game.grd.draw(self.game.display)
        self.mouse_pos = pygame.mouse.get_pos()
        
        # for debugging
        self.fps = service.draw_text(str(int(self.game.clock.get_fps())),20, 30, 30, self.game.display)
        
        self.game.bg.update()
        self.game.grd.update()


    def blit_screen(self):
        self.game.check_events()
        self.game.window.blit(self.game.display, (0,0))
        self.game.clock.tick(config.FPS)
        
        
        pygame.display.update()


class PipeyBird(DLC):
    def __init__(self, game):
        DLC.__init__(self, game)   

    def run_display(self):
        pass
        
    def game_logic(self):
        pass


class FreeBird(DLC):
    def __init__(self, game):
        DLC.__init__(self, game)   
        pass

    def run_display(self):
        pass
        
    def game_logic(self):
        pass