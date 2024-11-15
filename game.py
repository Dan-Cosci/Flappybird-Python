import pygame
import random
import time

from objects import background, bird, ground, pipe
from src import config, service
from menu import MainMenu, Restart_menu
import dlc



# main game class
class Game():
    def __init__(self):
        
        # initializing pygame and mixer module
        pygame.init()
        pygame.mixer.pre_init()
        pygame.mixer.init()

        # load display
        self.display = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappybird")
        pygame.display.set_icon(pygame.image.load("assets/images/bird2.png").convert_alpha())

        #load sounds
        self.flap_fx = pygame.mixer.Sound("assets/sound/flap.wav")
        self.point_fx = pygame.mixer.Sound("assets/sound/point.wav")
        self.death_fx = pygame.mixer.Sound("assets/sound/die.wav")
        self.hit_fx = pygame.mixer.Sound("assets/sound/hit.wav")

        # sound play only once
        self.sound_played = False

        # for the game to not start immediately
        self.start = False
        self.bird_hit = False

        # initializes the bird
        self.Flappy = bird.Bird(config.WIDTH / 2, config.HEIGHT / 2, 1.3, self)
        
        # initializes background and ground
        self.bg = background.Background(0, 0, 1.2)
        self.grd = ground.Ground(0, (config.HEIGHT - (config.HEIGHT // 6)), 1.2)


        # initializes the pipe
        self.pipe_group = pygame.sprite.Group()
        self.pipe_gap = 200
        self.last_pipe = pygame.time.get_ticks()
        self.pipe_freq = 1200

        # menus
        self.start_menu = MainMenu(self)
        self.restart_menu = Restart_menu(self)
        self.cur_menu = self.start_menu

        # DLC content
        self.dlc = False

        self.pipeybird = dlc.PipeyBird(self)
        self.freebird = dlc.FreeBird(self)
        self.dlc_play = self.pipeybird

        # initialization score
        self.score = 0
        self.passed = False

        # codition required for the loop
        self.running, self.playing = True, False


    def draw(self):
        self.display.fill((0,0,0))

        self.bg.draw(self.display)

        self.pipe_group.draw(self.display)
        
        self.Flappy.draw(self.display)
        self.grd.draw(self.display)

        self.text = service.draw_text(str(self.score), 40, config.WIDTH / 2, config.HEIGHT / 8, self.display)
        self.fps = service.draw_text(str(int(self.clock.get_fps())),20, 30, 30, self.display)

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
                self.restart_menu.run_display = False

            if self.cur_menu.state == "menu":

                # start button and actions
                if self.cur_menu.start_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.start_hover = True
                    self.cur_menu.quit_hover = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.cur_menu.state = "game"
                        self.playing = True
                        self.start = False
                        self.cur_menu.run_display = False
                        self.score = 0

                # quit button and actions
                elif self.cur_menu.quit_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.quit_hover = True
                    self.cur_menu.start_hover = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.running, self.playing = False, False
                        self.cur_menu.run_display = False
                        pygame.quit()

                else:
                    self.cur_menu.mouse_hover = False
                    self.cur_menu.start_hover = False
                    self.cur_menu.quit_hover = False
            

            elif self.cur_menu.state == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start = True
                    if not(self.bird_hit):
                        self.Flappy.flap()


            elif self.cur_menu.state == "restart":
                    
                # restart button and actions
                if self.cur_menu.restart_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.menu_hover = False
                    self.cur_menu.restart_hover = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.cur_menu.run_display = False
                        self.cur_menu.text_created = False
                        self.cur_menu.new_score = False
                        self.score = 0
                        
                        self.cur_menu = self.start_menu
                        

                        self.cur_menu.state = "game"
                        self.playing = True
                        self.start = False
                        self.cur_menu.run_display = False

                # menu button and actions
                elif self.cur_menu.menu_rect.collidepoint(self.cur_menu.mouse_pos):
                    self.cur_menu.mouse_hover = True
                    self.cur_menu.menu_hover = True
                    self.cur_menu.restart_hover = False
                
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.cur_menu.run_display = False

                        self.cur_menu = self.start_menu
                        self.cur_menu.state = "menu"
                        self.cur_menu.run_display = True


                else:
                    self.cur_menu.mouse_hover = False
                    self.cur_menu.restart_hover = False
                    self.cur_menu.menu_hover = False


        # what the check function does when the game state is = "game" 
        if self.cur_menu.state == "game":

            for tubo in self.pipe_group:
                if self.Flappy.img_rect.colliderect(tubo.rect):
                    self.bird_hit = True
                    
                    if not self.sound_played:
                        self.hit_fx.play()
                        self.sound_played = True


                if tubo.rect.left < self.Flappy.img_rect.left\
                    and tubo.rect.right > self.Flappy.img_rect.right\
                    and self.passed == False\
                    and tubo.passed == False:

                    self.passed = True

                if tubo.rect.right < self.Flappy.img_rect.left\
                    and self.passed == True\
                    and tubo.passed == False:
                    tubo.passed = True
                    self.score += 1
                    self.passed = False
                    self.point_fx.play()


            if self.Flappy.img_rect.colliderect(self.grd.img_rect):
                
                # death flag
                self.death_fx.play()       
                self.playing = False

                # reconfiguring the state of the main menu
                self.cur_menu.state = "menu"

                # changing and displaying the restart menu
                self.restart_menu.run_display = True
                self.cur_menu = self.restart_menu

                # checking if the score is new highscore
                data = service.file_load(config.FILE_NAME)
                highscore = data["score"]["highscore"]

                if self.score > highscore:
                    self.cur_menu.new_score = True
                    data["score"]["highscore"] = self.score
                
                service.file_save(config.FILE_NAME, data)

                # making quote for the restart screen screen
                self.cur_menu.text_quote = service.quote(self.score, self.cur_menu.new_score)

                # reseting game conditions
                self.Flappy.reset()
                self.pipe_group.empty()
                self.start = False
                self.bird_hit = False

                self.sound_played = False

                    
