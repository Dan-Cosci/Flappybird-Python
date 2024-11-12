import pygame

from src import config



class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, scale, orientation= 0):
        pygame.sprite.Sprite.__init__(self)

        self.img = pygame.image.load("assets/images/pipe.png").convert_alpha()

        # 0 = top, 1 = buttom
        if orientation == 0:
            self.img = pygame.transform.flip(self.img, False, True)
            self.img = pygame.transform.scale_by(self.img, scale)
            self.img_rect = self.img.get_rect(bottomleft = (x,y))
        else:
            self.img = pygame.transform.scale_by(self.img, scale)
            self.img_rect = self.img.get_rect(topleft = (x,y))

    
    def draw(self, screen):
        screen.blit(self.img, self.img_rect)