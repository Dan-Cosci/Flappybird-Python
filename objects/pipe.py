import pygame

from src import config



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: int, config: dict, orientation: bool= False):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/images/pipe.png").convert_alpha()

        self.passed = False
        self.config = config

        # False = bottom, True = top
        if orientation:
            self.image = pygame.transform.scale_by(self.image, scale)
            self.rect = self.image.get_rect(topleft = (x,y))
        
        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.image = pygame.transform.scale_by(self.image, scale)
            self.rect = self.image.get_rect(bottomleft = (x,y))

    
    def update(self):
        self.rect.x -= self.config["GROUND_SPD"]
        if self.rect.right <= 0:
            self.kill()


    def draw(self, screen):
        screen.blit(self.image, self.rect)