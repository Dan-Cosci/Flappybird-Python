import pygame
from src import config

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, game):
        pygame.sprite.Sprite.__init__(self)

        # game instance in the class
        self.game = game

        # loading the images
        self.imgs =  [
            pygame.transform.scale_by(pygame.image.load('assets/images/bird1.png').convert_alpha(), scale),
            pygame.transform.scale_by(pygame.image.load('assets/images/bird2.png').convert_alpha(), scale),
            pygame.transform.scale_by(pygame.image.load('assets/images/bird3.png').convert_alpha(), scale)
        ]

        # miscellaneous image requirements
        self.img_index = 0
        self.ani_helper = 1
        self.cur_img = self.imgs[self.img_index]
        self.img_rect = self.cur_img.get_rect(center = (x, y))
        self.reset_rect = self.cur_img.get_rect(center = (x,y))

        self.bird_dead = pygame.transform.rotate(self.cur_img, -90)

        self.counter = 0
        self.cooldown = 3

        # gravity requirements
        self.g_index = 1
        self.g_max = 15
        self.gravity = 0


    def update(self):
        
        if not(self.game.bird_hit):

            # code of the bird's animation
            self.counter += 1

            if self.counter > self.cooldown:
                self.counter = 0
                self.img_index += self.ani_helper

                if self.img_index >= len(self.imgs) - 1 or self.img_index <= 0:
                    self.ani_helper *= -1
            
            self.cur_img = self.imgs[self.img_index]
        
        else:
            self.cur_img = self.bird_dead

        # gravity logic
        if self.gravity <= self.g_max:    
            self.gravity += self.g_index
        
        self.img_rect.y += self.gravity


    def draw(self, screen):
        screen.blit(self.cur_img, self.img_rect)
    
    
    def reset(self):
        self.img_rect.x, self.img_rect.y = self.reset_rect.x, self.reset_rect.y
        self.cur_img = self.imgs[self.img_index]


    def flap(self):
        self.gravity = 0
        self.gravity -= 12
