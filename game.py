from src import config
import pygame

pygame.init()
screen = pygame.display.set_mode((config.SCREENWIDTH,config.SCREENHEIGTH ))
clock = pygame.time.Clock()

run = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    clock.tick(config.FPS)
    pygame.display.flip()

pygame.quit()