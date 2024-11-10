import pygame

from src import config

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, image):
        pygame.sprite.Sprite.__init__(self)
        self.img = image
        self.img = pygame.transform.scale_by(self.img, scale)
        self.img_rect = self.img.get_rect(center = (x,y))
    

    def draw(self, screen):
        screen.blit(self.img, self.img_rect)

    def update(self):
        pass

    def click(self):
        pass