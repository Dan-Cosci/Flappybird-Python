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
        self.ani_helper = 1
        self.cur_img = self.imgs[self.img_index]
        self.img_rect = self.cur_img.get_rect(center = (x, y))
        
        self.counter = 0
        self.cooldown = 4


    def update(self):
        self.counter += 1

        if self.counter > self.cooldown:
            self.counter = 0
            self.img_index += self.ani_helper

            if self.img_index >= len(self.imgs) - 1 or self.img_index <= 0:
                self.ani_helper *= -1
        
        self.cur_img = self.imgs[self.img_index]


    def draw(self, screen):
        screen.blit(self.cur_img, self.img_rect)
