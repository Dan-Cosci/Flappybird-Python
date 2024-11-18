import pygame
import math


class Ground(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: int, config: dict):
        pygame.sprite.Sprite.__init__(self)

        self.config = config

        self.img = pygame.image.load('assets/images/ground.png').convert_alpha()
        self.img = pygame.transform.scale_by(self.img, scale)
        self.img_rect = self.img.get_rect(topleft = (x,y))

        self.bg_width = self.img.get_width()
        self.scroll = 0
    

    def draw(self, screen):

        panel = math.ceil(self.config["WIDTH"]/ self.bg_width) + 2

        for i in range(panel):
            # self.img_rect.x  
            temp = i * self.bg_width + self.scroll - self.bg_width
            screen.blit(self.img,(temp, self.img_rect.y))


    def update(self):
        self.scroll -= self.config["GROUND_SPD"]
        # self.img_rect.x = self.scroll
        if abs(self.scroll)> self.bg_width:
            self.scroll = 0


class DLC_Ground(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: int, config: dict):
        pygame.sprite.Sprite.__init__(self)

        self.config = config

        self.img = pygame.image.load('assets/images/DLC_ground.png').convert_alpha()
        self.img = pygame.transform.scale_by(self.img, scale)
        self.img_rect = self.img.get_rect(topleft = (x,y))

        self.bg_width = self.img.get_width()
        self.scroll = 0
    

    def draw(self, screen):

        panel = math.ceil(self.config["WIDTH"]/ self.bg_width) + 2

        for i in range(panel):
            # self.img_rect.x  
            temp = i * self.bg_width + self.scroll - self.bg_width
            screen.blit(self.img,(temp, self.img_rect.y))


    def update(self):
        self.scroll -= self.config["GROUND_SPD"]
        # self.img_rect.x = self.scroll
        if abs(self.scroll)> self.bg_width:
            self.scroll = 0