import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: float, config: dict, game: object):
        pygame.sprite.Sprite.__init__(self)

        self.config = config

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
        self.g_index = self.config["BIRD_GRAV"]
        self.g_max = self.config["BIRD_MAX_G"]
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
        self.gravity -= self.config["BIRD_JUMP"]
        self.game.flap_fx.play()



class DLC_Bird(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: int, config: dict):
        pygame.sprite.Sprite.__init__(self)

        self.passed = False
        self.config = config

        self.imgs =  [
            pygame.transform.flip(pygame.transform.scale_by(pygame.image.load('assets/images/DLC_bird1.png').convert_alpha(), scale), True, False),
            pygame.transform.flip(pygame.transform.scale_by(pygame.image.load('assets/images/DLC_bird2.png').convert_alpha(), scale), True, False),
            pygame.transform.flip(pygame.transform.scale_by(pygame.image.load('assets/images/DLC_bird3.png').convert_alpha(), scale), True, False)
        ]

        self.index = 0
        self.ani_helper = 1 

        self.counter = 0
        self.cooldown = 3

        self.image = self.imgs[self.index]
        self.rect = self.image.get_rect(center = (x,y))

    
    def update(self):
        self.counter += 1

        if self.counter > self.cooldown:
            self.counter = 0
            self.index += self.ani_helper

            if self.index >= len(self.imgs) - 1 or self.index <= 0:
                self.ani_helper *= -1
        
        self.image = self.imgs[self.index]
        
        self.rect.x -= self.config["dlc_config"]["BIRD_SPD"]
        if self.rect.right <= 0:
            self.kill()


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        