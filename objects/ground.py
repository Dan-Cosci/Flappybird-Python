import pygame
import math
from src import config

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.img = pygame.image.load('assets/images/ground.png').convert_alpha()
        self.img = pygame.transform.scale_by(self.img, scale)
        self.img_rect = self.img.get_rect(topleft = (x,y))

        self.bg_width = self.img.get_width()
        self.scroll = 0
    

    def draw(self, screen):

        panel = math.ceil(config.WIDTH/ self.bg_width) + 2

        for i in range(panel):
            # self.img_rect.x  
            temp = i * self.bg_width + self.scroll - self.bg_width
            screen.blit(self.img,(temp, self.img_rect.y))


    def update(self):
        self.scroll -= config.GROUND_SPD
        # self.img_rect.x = self.scroll
        if abs(self.scroll)> self.bg_width:
            self.scroll = 0