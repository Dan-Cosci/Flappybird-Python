import pygame

from objects import background, bird, button, ground, pipe
from src import config



pygame.init()
screen = pygame.display.set_mode((config.SCREENWIDTH, config.SCREENHEIGTH))
pygame.display.set_caption("FlappyBird")
pygame.display.set_icon(pygame.image.load('assets/bird1.png'))
clock = pygame.time.Clock()

bg = background.Background(0, 0, 1.2)
grd = ground.Ground(0, (config.SCREENHEIGTH - (config.SCREENHEIGTH // 6)), 1.2)

run = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill('black')

    bg.draw(screen)
    bg.update()

    grd.draw(screen)
    grd.update()

    clock.tick(config.FPS)
    pygame.display.flip()

pygame.quit()