import pygame
import random
import time

from objects import background, bird, ground, pipe
from src import service
from menu import MainMenu, Restart_menu
from dlc import PipeyBird, FreeBird



# main game class
class Game():
    def __init__(self):
        
        # initializing the config
        self.config = service.file_load("src/config.json")


        self.pipe_config = self.config["pipe_config"]
        self.bird_config = self.config["bird_config"]
        self.config = self.config["config"]

        self.fps_counter = self.config["fps_counter"]

        # initializing pygame and mixer module
        pygame.init()
        pygame.mixer.pre_init()
        pygame.mixer.init()

        # load display
        self.display = pygame.Surface((self.config["WIDTH"], self.config["HEIGHT"]))
        self.window = pygame.display.set_mode((self.config["WIDTH"], self.config["HEIGHT"]))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappybird")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png").convert_alpha())

        #load sounds
        self.flap_fx = pygame.mixer.Sound("assets/sound/flap.wav")
        self.point_fx = pygame.mixer.Sound("assets/sound/point.wav")
        self.death_fx = pygame.mixer.Sound("assets/sound/die.wav")
        self.hit_fx = pygame.mixer.Sound("assets/sound/hit.wav")
        self.swoosh_fx = pygame.mixer.Sound("assets/sound/swooshing.wav")

        # sound play only once
        self.sound_played = False

        # for the game to not start immediately
        self.start = False
        self.bird_hit = False
        self.ceiling_glitch = False

        # initializes the bird
        self.Flappy = bird.Bird(self.config["WIDTH"] / 2, self.config["HEIGHT"] / 2, 1.3, self.bird_config, self)
        
        # initializes background and ground
        self.orig_bg = background.Background(0, 0, 1.2, self.config)
        self.orig_grd = ground.Ground(0, (self.config["HEIGHT"] - (self.config["HEIGHT"] // 6)), 1.2, self.config)
        
        # DLC content
        self.dlc = False

        self.pipeybird = PipeyBird(self)
        self.freebird = FreeBird(self)
        self.dlc_play = self.pipeybird

        self.dlc_bird_group = pygame.sprite.Group()

        self.dlc_pipe_group = pygame.sprite.Group()
        self.dlc_top_p = pipe.DLC_pipe(self.config["WIDTH"] / 4, self.config["HEIGHT"] / 2 - self.pipe_config["dlc_pipe"]["PIPE_GAP"] / 2, 1.2, self.pipe_config, self)
        self.dlc_btm_p = pipe.DLC_pipe(self.config["WIDTH"] / 4, self.config["HEIGHT"] / 2 + self.pipe_config["dlc_pipe"]["PIPE_GAP"] / 2, 1.2, self.pipe_config, self, True)
        self.dlc_pipe_group.add(self.dlc_top_p)
        self.dlc_pipe_group.add(self.dlc_btm_p)

        self.dlc_bg = background.DLC_Background(0, 0, 1.4, self.config)
        self.dlc_grd = ground.DLC_Ground(0, (self.config["HEIGHT"] - (self.config["HEIGHT"] // 6)), 1.2, self.config)

        # sets the background to the default one
        self.bg = self.orig_bg
        self.grd = self.orig_grd

        # initializes the pipe
        self.pipe_group = pygame.sprite.Group()

        self.diff = ["easy", "medium", "hard"]
        self.diff_index = 0
        self.pipe_gap = self.pipe_config["pipe_gap"]
        self.pipe_freq = self.pipe_config["pipe_frequency"]

        # menus
        self.start_menu = MainMenu(self)
        self.restart_menu = Restart_menu(self)
        self.cur_menu = self.start_menu


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

        self.text = service.draw_text(str(self.score), 40, self.config["WIDTH"] / 2, self.config["HEIGHT"] / 8, self.display)
        
        if self.fps_counter:
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

            self.clock.tick(self.config["FPS"])


    def pipe_gen(self):
        
        pipe_height = random.randint(150, 500)
        if self.score > 15:
            self.diff_index = 1
        if self.score > 25:
            self.diff_index = 2

        if len(self.pipe_group) == 0:
            self.top_pipe = pipe.Pipe(self.config["WIDTH"], pipe_height - self.pipe_gap[self.diff[self.diff_index]] / 2, 1, self.config)
            self.btm_pipe = pipe.Pipe(self.config["WIDTH"], pipe_height + self.pipe_gap[self.diff[self.diff_index]] / 2, 1, self.config, True)
            self.pipe_group.add(self.btm_pipe)
            self.pipe_group.add(self.top_pipe)

        elif len(self.pipe_group) > 0:
            for pipes in self.pipe_group:
                if pipes.rect.right < self.pipe_freq[self.diff[self.diff_index]]:
                    if len(self.pipe_group) < 3:    
                        self.top_pipe = pipe.Pipe(self.config["WIDTH"], pipe_height - self.pipe_gap[self.diff[self.diff_index]] / 2, 1, self.config)
                        self.btm_pipe = pipe.Pipe(self.config["WIDTH"], pipe_height + self.pipe_gap[self.diff[self.diff_index]] / 2, 1, self.config, True)
                        self.pipe_group.add(self.btm_pipe)
                        self.pipe_group.add(self.top_pipe)


    def check_events(self):

        # for loop for pygame events only
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.cur_menu.run_display = False
                self.restart_menu.run_display = False
                self.pipeybird.run_dlc = False
                self.freebird.run_dlc = False
                pygame.quit()
            
            # regular controls
            if not self.dlc:
                if self.cur_menu.state == "menu":

                    # start button and actions
                    if self.cur_menu.start_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.start_hover = True

                        self.cur_menu.quit_hover = False
                        self.cur_menu.dlc_hover = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()
                            
                            self.cur_menu.state = "game"
                            self.playing = True
                            self.start = False
                            self.cur_menu.run_display = False
                            self.score = 0
                            self.ceiling_glitch = False

                    # dlc button and actions
                    elif self.cur_menu.dlc_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.dlc_hover = True
                        
                        self.cur_menu.quit_hover = False
                        self.cur_menu.start_hover = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()

                            self.bg = self.dlc_bg
                            self.grd = self.dlc_grd
                            self.dlc = True

                    # quit button and actions
                    elif self.cur_menu.quit_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.quit_hover = True

                        self.cur_menu.start_hover = False
                        self.cur_menu.dlc_hover = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()
                            
                            self.running, self.playing = False, False
                            self.cur_menu.run_display = False
                            pygame.quit()

                    else:
                        self.cur_menu.mouse_hover = False
                        self.cur_menu.vanilla_hover = False
                        self.cur_menu.start_hover = False
                        self.cur_menu.quit_hover = False
                        self.cur_menu.dlc_hover = False
                

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
                            self.swoosh_fx.play()
                            
                            self.cur_menu.run_display = False
                            self.cur_menu.text_created = False
                            self.cur_menu.new_score = False
                            self.score = 0
                            self.ceiling_glitch = False
                            
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
                            self.swoosh_fx.play()
                            
                            self.cur_menu.run_display = False

                            self.cur_menu = self.start_menu
                            self.cur_menu.state = "menu"
                            self.cur_menu.run_display = True


                    else:
                        self.cur_menu.mouse_hover = False
                        self.cur_menu.restart_hover = False
                        self.cur_menu.menu_hover = False

            # DLC controls
            else:

                if self.cur_menu.state == "menu":

                    # start button and actions
                    if self.cur_menu.start_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.start_hover = True

                        self.cur_menu.quit_hover = False
                        self.cur_menu.vanilla_hover = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()

                            self.restart_menu.new_score = False

                            self.cur_menu.state = "pipeybird"
                            self.dlc_play.run_dlc = True
                            self.start = False
                            self.cur_menu.run_display = False
                            self.score = 0

                            # resets pipes and empty the bird group
                            self.dlc_top_p.pipe_reset()
                            self.dlc_btm_p.pipe_reset()
                            self.dlc_bird_group.empty()


                    # dlc button and actions
                    elif self.cur_menu.vanilla_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.vanilla_hover = True
                        
                        self.cur_menu.quit_hover = False
                        self.cur_menu.start_hover = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()

                            self.bg = self.orig_bg
                            self.grd = self.orig_grd
                            self.dlc = False

                    # quit button and actions
                    elif self.cur_menu.quit_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.quit_hover = True

                        self.cur_menu.start_hover = False
                        self.cur_menu.vanilla_hover = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()

                            self.running, self.playing = False, False
                            self.cur_menu.run_display = False
                            pygame.quit()

                    else:
                        self.cur_menu.mouse_hover = False
                        self.cur_menu.dlc_hover = False
                        self.cur_menu.start_hover = False
                        self.cur_menu.quit_hover = False
                        self.cur_menu.vanilla_hover = False
                

                # game controls
                elif self.cur_menu.state == "pipeybird":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.dlc_top_p.pipe_jump()
                        self.dlc_btm_p.pipe_jump()
                        self.flap_fx.play()

                # restart menu controls
                elif self.cur_menu.state == "restart":
                        
                    # restart button and actions
                    if self.cur_menu.restart_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.menu_hover = False
                        self.cur_menu.restart_hover = True

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()
                            
                            self.cur_menu.new_score = False

                            self.cur_menu.run_display = False
                            self.cur_menu = self.start_menu
                            self.cur_menu.state = "pipeybird"
                            self.dlc_play.run_dlc = True
                            self.start = False
                            self.score = 0

                            # resets pipes and empty the bird group
                            self.dlc_top_p.pipe_reset()
                            self.dlc_btm_p.pipe_reset()
                            self.dlc_bird_group.empty()

                    # menu button and actions
                    elif self.cur_menu.menu_rect.collidepoint(self.cur_menu.mouse_pos):
                        self.cur_menu.mouse_hover = True
                        self.cur_menu.menu_hover = True
                        self.cur_menu.restart_hover = False
                    
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.swoosh_fx.play()
                            
                            self.cur_menu.run_display = False

                            self.cur_menu = self.start_menu
                            self.cur_menu.state = "menu"
                            self.cur_menu.run_display = True


                    else:
                        self.cur_menu.mouse_hover = False
                        self.cur_menu.restart_hover = False
                        self.cur_menu.menu_hover = False


        # event cheking for all the states
        if self.cur_menu.state == "game":

            for tubo in self.pipe_group:
                if self.Flappy.img_rect.colliderect(tubo.rect):
                    self.bird_hit = True
                    
                    if not self.sound_played:
                        self.hit_fx.play()
                        self.sound_played = True

                # tried to cheat
                if self.Flappy.img_rect.y <= 0:
                    self.bird_hit = True

                    self.ceiling_glitch = True
                    
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
                data = service.file_load(self.config["FILE_NAME"])
                highscore = data["score"]["highscore"]

                if self.score > highscore:
                    self.cur_menu.new_score = True
                    data["score"]["highscore"] = self.score
                
                service.file_save(self.config["FILE_NAME"], data)

                # making quote for the restart screen screen
                self.cur_menu.text_quote = service.quote(self.score, self.cur_menu.new_score)

                # reseting game conditions
                self.Flappy.reset()
                self.pipe_group.empty()

                self.diff_index = 0

                self.start = False
                self.bird_hit = False

                self.sound_played = False


        elif self.cur_menu.state == "pipeybird":
            
            for birds in self.dlc_bird_group:
                if self.dlc_pipe_group.sprites()[0].rect.left< birds.rect.left\
                    and self.dlc_pipe_group.sprites()[0].rect.right > birds.rect.right:
                    self.passed = True
                
                if self.dlc_pipe_group.sprites()[0].rect.left > birds.rect.right\
                and self.passed:
                    self.score += 1
                    self.point_fx.play()
                    self.passed = False
                    

            # colllision detection and death flag
            if pygame.sprite.groupcollide(self.dlc_bird_group, self.dlc_pipe_group, False, False)\
                or self.dlc_top_p.rect.colliderect(self.grd.img_rect)\
                    or self.dlc_btm_p.rect.y <= 0:

                # death actions
                self.dlc_play.run_dlc = False
                self.playing = False
                self.death_fx.play()


                # changing to the restart menu
                self.cur_menu = "menu"
                self.restart_menu.run_display = True
                self.cur_menu = self.restart_menu

                # checking if the score is new highscore
                data = service.file_load(self.config["FILE_NAME"])
                highscore = data["score"]["DLC_1_High"]

                if self.score > highscore:
                    self.cur_menu.new_score = True
                    data["score"]["DLC_1_High"] = self.score
                
                service.file_save(self.config["FILE_NAME"], data)

                # making quote for the restart screen screen
                self.cur_menu.text_quote = service.quote(self.score, self.cur_menu.new_score)

                
                # resets pipes and empty the bird group
                self.passed = False
                self.ceiling_glitch = False
                
                self.dlc_top_p.pipe_reset()
                self.dlc_btm_p.pipe_reset()
                self.dlc_bird_group.empty()


                    
