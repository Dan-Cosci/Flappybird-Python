import pygame

from src import config

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, image):
        pygame.sprite.Sprite.__init__(self)
        self.img = image
        self.img = pygame.transform.scale_by(self.img, scale)
        self.img_rect = self.img.get_rect(center = (x,y))

        self.is_click = False
    

    def draw(self, screen):
        screen.blit(self.img, self.img_rect)
    
    def click(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.img_rect.collidepoint(mouse_pos):
                    self.is_click = True
                    print("I is working")
            else:
                self.is_click = False
    
    def clicked(self):
        return self.is_click