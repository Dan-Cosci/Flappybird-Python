import pygame
from src import config

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.imgs =  [
            pygame.transform.scale_by(pygame.image.load('assets/bird1.png').convert_alpha(), scale),
            pygame.transform.scale_by(pygame.image.load('assets/bird2.png').convert_alpha(), scale),
            pygame.transform.scale_by(pygame.image.load('assets/bird3.png').convert_alpha(), scale)
        ]
        self.img_index = 0
        self.cur_img = self.imgs[self.img_index]
        self.img_rect = self.cur_img.get_rect(center = (x, y))

    def draw(self, screen):
        screen.blit(self.cur_img, self.img_rect)

    def update(self):
        pass