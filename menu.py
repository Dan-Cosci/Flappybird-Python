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


    def blit_screen(self):
        self.game.check_events()
        self.game.window.blit(self.game.display, (0,0))
        self.game.clock.tick(config.FPS)
        pygame.display.update()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
        # start button image
        self.play = pygame.image.load("assets/ui_elements/play.png").convert_alpha()
        self.play = pygame.transform.scale_by(self.play, 1.2)
        self.start_rect = self.play.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2))
        
        # quit
        self.option_button = pygame.image.load("assets/ui_elements/option.png").convert_alpha()
        self.option_button = pygame.transform.scale_by(self.option_button, 1.2)
        self.options_rect = self.option_button.get_rect(center = (config.WIDTH / 2, config.HEIGHT / 2 + 45))

    def display_menu(self):
        while self.run_display:
            self.base_background()

            service.draw_text("FlappyBird", 60, config.WIDTH/ 2, service.sine(100,2500,10,(config.HEIGHT / 6)), self.game.display)
            self.play_button()
            self.blit_screen()

    def play_button(self):
        self.game.display.blit(self.play, self.start_rect)
        self.game.display.blit(self.option_button, self.options_rect)

        