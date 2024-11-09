import pygame
from src import config

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('assets/background.png').convert_alpha()
        self.img = pygame.transform.scale_by(self.img, scale)
        self.img_rect = self.img.get_rect(topleft= (x,y))

        self.img_rect2 = self.img.get_rect(topleft= (self.img.get_width(),y))

        self.img_list = []

    def draw(self, screen):
        screen.blit(self.img, self.img_rect)
        screen.blit(self.img, self.img_rect2)

    def update(self):
        self.img_rect.x -= config.BG_SPD
        self.img_rect2.x -= config.BG_SPD
        
        if self.img_rect.right == 0:
            self.img_rect.x = self.img_rect2.right

        if self.img_rect2.right == 0:
            self.img_rect2.x = self.img_rect.right 