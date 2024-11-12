import pygame

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

        # initializes background and ground
        self.bg = background.Background(0, 0, 1.2)
        self.grd = ground.Ground(0, (config.HEIGHT - (config.HEIGHT // 6)), 1.2)

        # initializes the bird
        self.Flappy = bird.Bird(config.WIDTH / 2, config.HEIGHT / 2, 1.3)

        # menu
        self.cur_menu = MainMenu(self)

        # codition required for the loop
        self.running, self.playing = True, False


    def draw(self):
        self.display.fill((0,0,0))

        self.bg.draw(self.display)
        
        self.Flappy.draw(self.display)
        self.grd.draw(self.display)


        self.window.blit(self.display, (0,0))
        pygame.display.update()


    def update(self):
        self.bg.update()
        self.grd.update()
        self.Flappy.update()
        
                                              
    def game_loop(self):
        while self.playing:
            self.check_events()

            self.draw()
            if self.start:
                self.update()

            self.clock.tick(config.FPS)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.cur_menu.run_display = False

            if self.cur_menu.state == "menu":

                if self.cur_menu.start_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.start_hover = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.cur_menu.state = "game"
                        self.playing = True
                        self.start = False
                        self.cur_menu.run_display = False

                elif self.cur_menu.quit_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.quit_hover = True

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
                    self.Flappy.flap()
                
                
        if self.Flappy.img_rect.colliderect(self.grd.img_rect):
            self.playing = False
            self.cur_menu.state = "menu"
            self.cur_menu.run_display = True
            self.Flappy.reset()
            self.start = False