import pygame

from objects import background, bird, button, ground, pipe
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

        # new custom cursor
        self.cursor = pygame.image.load("assets/ui_elements/cursor.png").convert_alpha()
        self.cursor = pygame.transform.scale_by(self.cursor, 3.5)
        pygame.mouse.set_visible(False)

        # initializes background and ground
        self.bg = background.Background(0, 0, 1.2)
        self.grd = ground.Ground(0, (config.HEIGHT - (config.HEIGHT // 6)), 1.2)

        # initializes the bird
        self.Flappy = bird.Bird(config.WIDTH / 2, config.HEIGHT / 2, 1.3)

        # menu
        self.cur_menu = MainMenu(self)

        # codition required for the loop
        self.running, self.playing = True, False


    def mouse_cursor(self):
        pos = pygame.mouse.get_pos()
        self.display.blit(self.cursor, pos)


    def draw(self):
        self.display.fill((0,0,0))

        self.bg.draw(self.display)
        
        self.Flappy.draw(self.display)
        self.grd.draw(self.display)

        self.bg.update()
        self.grd.update()
        self.Flappy.update()

        self.mouse_cursor()
        self.window.blit(self.display, (0,0))
        pygame.display.update()
                                              
    def game_loop(self):
        while self.playing:
            self.check_events()

            self.draw()

            self.clock.tick(config.FPS)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.cur_menu.run_display = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.Flappy.flap()
                self.cur_menu.run_display = False
                self.playing = True
                
        if self.Flappy.img_rect.colliderect(self.grd.img_rect):
            self.running, self.playing = False, False
