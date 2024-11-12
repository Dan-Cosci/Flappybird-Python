import pygame
import random

from objects import background, bird, ground, pipe
from src import config
from menu import MainMenu



# main game class
class Game():
    def __init__(self):
        
        # initializing pygame module
        pygame.init()
        self.display = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappybird")
        pygame.display.set_icon(pygame.image.load("assets/images/bird2.png").convert_alpha())

        # for the game to not start immediately
        self.start = False
        self.bird_hit = False

        # initializes background and ground
        self.bg = background.Background(0, 0, 1.2)
        self.grd = ground.Ground(0, (config.HEIGHT - (config.HEIGHT // 6)), 1.2)

        # initializes the bird
        self.Flappy = bird.Bird(config.WIDTH / 2, config.HEIGHT / 2, 1.3, self)

        # initializes the pipe
        self.pipe_group = pygame.sprite.Group()
        self.pipe_gap = 150
        self.last_pipe = pygame.time.get_ticks()
        self.pipe_freq = 2000

        # menu
        self.cur_menu = MainMenu(self)

        # codition required for the loop
        self.running, self.playing = True, False


    def draw(self):
        self.display.fill((0,0,0))

        self.bg.draw(self.display)

        self.pipe_group.draw(self.display)
        
        self.Flappy.draw(self.display)
        self.grd.draw(self.display)


        self.window.blit(self.display, (0,0))
        pygame.display.update()


    def update(self):
        
        if not(self.bird_hit):
            self.bg.update()
            self.grd.update()
            self.pipe_group.update()

        self.Flappy.update()
        
                                              
    def game_loop(self):
        while self.playing:
            self.check_events()

            self.draw()
            if self.start:
                self.update()
                self.pipe_gen()

            self.clock.tick(config.FPS)


    def pipe_gen(self):
        
        timenow = pygame.time.get_ticks()
        if timenow - self.last_pipe > self.pipe_freq:
            pipe_height = random.randint(150, 500)

            self.top_pipe = pipe.Pipe(config.WIDTH, pipe_height - self.pipe_gap / 2, 1, 0)
            self.btm_pipe = pipe.Pipe(config.WIDTH, pipe_height + self.pipe_gap / 2, 1, 1)

            self.pipe_group.add(self.btm_pipe)
            self.pipe_group.add(self.top_pipe)
            self.last_pipe = timenow


    def check_events(self):

        # for loop for pygame events only
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.cur_menu.run_display = False

            if self.cur_menu.state == "menu":

                if self.cur_menu.start_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.start_hover = True
                    self.cur_menu.quit_hover = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.cur_menu.state = "game"
                        self.playing = True
                        self.start = False
                        self.cur_menu.run_display = False

                elif self.cur_menu.quit_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.quit_hover = True
                    self.cur_menu.start_hover = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.running, self.playing = False, False
                        self.cur_menu.run_display = False 

                else:
                    self.cur_menu.mouse_hover = False
                    self.cur_menu.start_hover = False
                    self.cur_menu.quit_hover = False
            
            elif self.cur_menu.state == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start = True
                    if not(self.bird_hit):
                        self.Flappy.flap()

        # what the check function does when the game state is = "game" 
        if self.cur_menu.state == "game":        
            for tubo in self.pipe_group:
                if self.Flappy.img_rect.colliderect(tubo.rect):
                    self.bird_hit = True
                        
            if self.Flappy.img_rect.colliderect(self.grd.img_rect):
                self.playing = False
                self.cur_menu.state = "menu"
                self.cur_menu.run_display = True
                    
                self.Flappy.reset()
                self.pipe_group.empty()

                self.start = False
                self.bird_hit = False
                    