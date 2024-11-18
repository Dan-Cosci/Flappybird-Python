import pygame



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



class DLC_pipe(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: int, config: dict, game : object, orientation: bool= False):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.config = config["dlc_pipe"]
        
        self.image = pygame.image.load("assets/images/DLC_pipe.png").convert_alpha()

        # False = bottom, True = top
        if orientation:
            self.image = pygame.transform.scale_by(self.image, scale)
            self.rect = self.image.get_rect(midtop = (x,y))
            self.reset_rect = self.image.get_rect(midtop = (x,y))

        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.image = pygame.transform.scale_by(self.image, scale)
            self.rect = self.image.get_rect(midbottom = (x,y))
            self.reset_rect = self.image.get_rect(midbottom = (x,y))
        
        # gravity requirements
        self.g_index = self.config["PIPE_GRAV"]
        self.g_max = self.config["PIPE_MAX_G"]
        self.gravity = 0
        

    def update(self):
        # gravity logic
        if self.gravity <= self.g_max:    
            self.gravity += self.g_index
        
        self.rect.y += self.gravity


    def pipe_jump(self):
        self.gravity = 0
        self.gravity -= self.config["PIPE_JUMP"]

    
    def pipe_reset(self):
        self.rect.x, self.rect.y = self.reset_rect.x, self.reset_rect.y
        self.gravity = 0