import pygame

from src import config



class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, scale, orientation= 0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/images/pipe.png").convert_alpha()

        self.passed = False

        # 0 = top, 1 = buttom
        if orientation == 0:
            self.image = pygame.transform.flip(self.image, False, True)
            self.image = pygame.transform.scale_by(self.image, scale)
            self.rect = self.image.get_rect(bottomleft = (x,y))
        
        else:
            self.image = pygame.transform.scale_by(self.image, scale)
            self.rect = self.image.get_rect(topleft = (x,y))

    
    def update(self):
        self.rect.x -= config.GROUND_SPD
        if self.rect.right <= 0:
            self.kill()


    def draw(self, screen):
        screen.blit(self.image, self.rect)