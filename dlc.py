import pygame
import random
import time

from objects import background, bird, ground, pipe
from src import config, service
from menu import MainMenu, Restart_menu


class DLC():
    def __init__(self, game: object):
        self.game = game

        self.run_dlc = False
        self.hit = False


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
        while self.run_dlc:
            self.base_background()

            self.game.dlc_pipe_group.update()
            self.game.dlc_bird_group.update()
            
            self.blit_screen()


    def base_background(self):
        self.game.display.fill('black')
        self.game.bg.draw(self.game.display)
        
        self.game.dlc_pipe_group.draw(self.game.display)
        self.game_logic()
        self.game.dlc_bird_group.draw(self.game.display)
        

        self.game.grd.draw(self.game.display)
        self.mouse_pos = pygame.mouse.get_pos()
        
        # for debugging
        self.fps = service.draw_text(str(int(self.game.clock.get_fps())),20, 30, 30, self.game.display)
        
        self.game.bg.update()
        self.game.grd.update()


    def game_logic(self):
        
        bird_height = random.randint(125, 500)

        
        if len(self.game.dlc_bird_group) == 0:
            self.dlc_bird = bird.DLC_Bird(self.game.config["WIDTH"], bird_height, 1.3, self.game.config)
            self.game.dlc_bird_group.add(self.dlc_bird)

        elif len(self.game.dlc_bird_group) > 0:
            for birds in self.game.dlc_bird_group:
                birds.rect.y =  service.sine(75,2000, 5, birds.rect.y)
                if birds.rect.right < 50:
                    if len(self.game.dlc_bird_group) < 2:
                        self.dlc_bird = bird.DLC_Bird(self.game.config["WIDTH"], bird_height, 1.3, self.game.config)
                        self.game.dlc_bird_group.add(self.dlc_bird)


class FreeBird(DLC):
    def __init__(self, game):
        DLC.__init__(self, game)   
        pass

    def run_display(self):
        while self.run_dlc:
            self.base_background()
            
            self.blit_screen()
        
    def game_logic(self):
        pass