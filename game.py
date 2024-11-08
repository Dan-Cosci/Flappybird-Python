import pygame

from objects import background, bird, button, ground, pipe
from src import config



pygame.init()
screen = pygame.display.set_mode((config.SCREENWIDTH,config.SCREENHEIGTH ))
clock = pygame.time.Clock()

bg = background.Background(0,0, 2)

run = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    bg.draw(screen)
    clock.tick(config.FPS)
    pygame.display.flip()

pygame.quit()