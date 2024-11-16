import pygame

from src import config, service

class Menu():
    def __init__(self, game):
        self.game = game
        self.state = "menu"
        self.run_display = True


    def base_background(self):
        self.game.display.fill('black')
        self.game.bg.draw(self.game.display)
        self.game.grd.draw(self.game.display)
        self.mouse_pos = pygame.mouse.get_pos()
        
        # for debugging
        self.fps = service.draw_text(str(int(self.game.clock.get_fps())),20, 30, 30, self.game.display)
        
        self.game.bg.update()
        self.game.grd.update()


    def blit_screen(self):
        self.game.check_events()
        self.game.window.blit(self.game.display, (0,0))
        self.game.clock.tick(config.FPS)
        
        
        pygame.display.update()



class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
        self.mouse_hover = False

        # start button image
        self.play = pygame.image.load("assets/ui_elements/play.png").convert_alpha()
        self.play2 = pygame.transform.scale_by(self.play, 1.25)
        self.play = pygame.transform.scale_by(self.play, 1.2)
        self.start_rect = self.play.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2))
        self.start_rect2 = self.play2.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2))
        
        self.start_hover = False


        # DLC button
        self.dlc = pygame.image.load("assets/ui_elements/dlc.png").convert_alpha()
        self.dlc2 = pygame.transform.scale_by(self.dlc, 1.25)
        self.dlc = pygame.transform.scale_by(self.dlc, 1.2)
        self.dlc_rect = self.dlc.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 45))
        self.dlc_rect2 = self.dlc2.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 45))
        
        self.dlc_hover = False


        # vanilla button
        self.vanilla = pygame.image.load("assets/ui_elements/vanilla.png").convert_alpha()
        self.vanilla2 = pygame.transform.scale_by(self.vanilla, 1.25)
        self.vanilla = pygame.transform.scale_by(self.vanilla, 1.20)
        self.vanilla_rect2 = self.vanilla2.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 45))
        self.vanilla_rect = self.vanilla.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 45))

        self.vanilla_hover = False


        # quit button
        self.quit_button = pygame.image.load("assets/ui_elements/quit.png").convert_alpha()
        self.quit_button2 = pygame.transform.scale_by(self.quit_button, 1.25)
        self.quit_button = pygame.transform.scale_by(self.quit_button, 1.2)
        self.quit_rect2 = self.quit_button2.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 90))
        self.quit_rect = self.quit_button.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 90))

        self.quit_hover = False



    def display_menu(self):
        while self.run_display:
            self.base_background()

            service.draw_text("FlappyBird", 60, config.WIDTH/ 2, service.sine(100,2500,10,(config.HEIGHT / 6)), self.game.display)
            self.play_button()
            self.blit_screen()


    def play_button(self):
        
        # base menu buttons
        self.game.display.blit(self.play, self.start_rect)

        if self.game.dlc:
            self.game.display.blit(self.vanilla, self.vanilla_rect)
        else:
            self.game.display.blit(self.dlc, self.dlc_rect)

        self.game.display.blit(self.quit_button, self.quit_rect)

        # animation for the menu buttons
        if self.mouse_hover:
            if self.start_hover:
                self.game.display.blit(self.play2, self.start_rect2)
            if self.quit_hover:
                self.game.display.blit(self.quit_button2, self.quit_rect2)

            if self.dlc_hover:
                self.game.display.blit(self.dlc2, self.dlc_rect2)
            if self.vanilla_hover:
                self.game.display.blit(self.vanilla2, self.vanilla_rect2)



class Restart_menu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        file_name = "src/data.json"
        self.file = service.file_load(file_name)

        self.state = "restart"
        self.run_display = False

        self.mouse_hover = False

        self.text_quote = ""

        self.new_score = False


        # scoreboard base background
        self.image = pygame.image.load("assets/ui_elements/bg_score.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1.3)
        self.img_rect = self.image.get_rect(center = (config.WIDTH/2, config.HEIGHT/2 - 100))


        # restart image button
        self.restart_button = pygame.image.load("assets/ui_elements/restart.png").convert_alpha()
        self.restart_button2 = pygame.transform.scale_by(self.restart_button, 1.25)
        self.restart_button = pygame.transform.scale_by(self.restart_button, 1.2)
        self.restart_rect2 = self.restart_button2.get_rect(center = (20 + config.WIDTH / 4, (config.HEIGHT / 2) + 75))
        self.restart_rect = self.restart_button.get_rect(center = (20 + config.WIDTH / 4, (config.HEIGHT / 2) + 75))


        self.restart_hover = False

        # menu image button
        self.menu_button = pygame.image.load("assets/ui_elements/menu.png").convert_alpha()
        self.menu_button2 = pygame.transform.scale_by(self.menu_button, 1.25)
        self.menu_button = pygame.transform.scale_by(self.menu_button, 1.2)
        self.menu_rect = self.menu_button.get_rect(center = (config.WIDTH - (config.WIDTH / 4) - 20, (config.HEIGHT / 2) + 75))
        self.menu_rect2 = self.menu_button2.get_rect(center = (config.WIDTH - (config.WIDTH / 4) - 20, (config.HEIGHT / 2) + 75)) 

        self.menu_hover = False

        
        
    def display_menu(self):
        while self.run_display:
            self.base_background()

            self.score()

            self.play_button()

            self.blit_screen()


    def play_button(self):
            
            # base menu button
            self.game.display.blit(self.restart_button, self.restart_rect)
            self.game.display.blit(self.menu_button, self.menu_rect)

            if self.mouse_hover:
                if self.menu_hover:
                    self.game.display.blit(self.menu_button2, self.menu_rect2)
                if self.restart_hover:
                    self.game.display.blit(self.restart_button2, self.restart_rect2)
    

    def score(self):
        self.game.display.blit(self.image, self.img_rect)

        # if new highscore
        if self.new_score:
            service.draw_text("NEW HIGHSCORE", 30, config.WIDTH / 2, config.HEIGHT / 2 - 190, self.game.display, (95, 43, 46))
        else:
            data = service.file_load(config.FILE_NAME)
            service.draw_text("Your Score", 30, config.WIDTH / 2, config.HEIGHT / 2 - 190, self.game.display, (95, 43, 46))
            service.draw_text(str(f"Highscore: {data['score']['highscore']}"), 20, config.WIDTH / 2, config.HEIGHT / 2 - 15, self.game.display, (95, 43, 46))
            
        service.draw_text(str(self.game.score), 
                            50, 
                            config.WIDTH / 2, config.HEIGHT / 2 - 145, 
                            self.game.display, 
                            (95, 43, 46))
            
        service.draw_quote(self.text_quote, 
                            22, 
                            config.WIDTH / 2, config.HEIGHT / 2 -130,
                            self.game.display,
                            (95, 43, 46))

            



    def base_background(self):
        self.game.display.fill('black')
        self.game.bg.draw(self.game.display)
        self.game.grd.draw(self.game.display)
        self.mouse_pos = pygame.mouse.get_pos()
        
        # for debugging
        self.fps = service.draw_text(str(int(self.game.clock.get_fps())),20, 30, 30, self.game.display)
        