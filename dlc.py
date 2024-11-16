import pygame
import random
import time

from objects import background, bird, ground, pipe
from src import config, service
from menu import MainMenu, Restart_menu



class DLC():
    def __init__(self,  game):
        self.game = game


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