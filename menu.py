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
        self.play = pygame.transform.scale_by(self.play, 1.2)
        self.start_rect = self.play.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2))
        
        self.start_hover = False

        self.play2 = pygame.image.load("assets/ui_elements/play.png").convert_alpha()
        self.play2 = pygame.transform.scale_by(self.play2, 1.25)
        self.start_rect2 = self.play2.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2))

        # quit
        self.quit_button = pygame.image.load("assets/ui_elements/quit.png").convert_alpha()
        self.quit_button = pygame.transform.scale_by(self.quit_button, 1.2)
        self.quit_rect = self.quit_button.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 45))

        self.quit_hover = False

        self.quit_button2 = pygame.image.load("assets/ui_elements/quit.png").convert_alpha()
        self.quit_button2 = pygame.transform.scale_by(self.quit_button2, 1.25)
        self.quit_rect2 = self.quit_button2.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 45))


    def display_menu(self):
        while self.run_display:
            self.base_background()

            service.draw_text("FlappyBird", 60, config.WIDTH/ 2, service.sine(100,2500,10,(config.HEIGHT / 6)), self.game.display)
            self.play_button()
            self.blit_screen()

    def play_button(self):
        
        # base menu buttons
        self.game.display.blit(self.play, self.start_rect)
        self.game.display.blit(self.quit_button, self.quit_rect)

        # animation for the menu buttons
        if self.mouse_hover:
            if self.start_hover:
                self.game.display.blit(self.play2, self.start_rect2)
            if self.quit_hover:
                self.game.display.blit(self.quit_button2, self.quit_rect2)
        