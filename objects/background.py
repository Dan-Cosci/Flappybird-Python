import pygame
from src import config

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('assets/background.png')
        self.img_rect = self.img.get_rect(topleft= (x,y))

    def draw(self, screen):
        screen.blit(self.img, self.img_rect)

    def update(self):
        pass