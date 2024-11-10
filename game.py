import pygame

from objects import background, bird, button, ground, pipe
from src import config


pygame.init()
screen = pygame.display.set_mode((config.SCREENWIDTH, config.SCREENHEIGTH))
clock = pygame.time.Clock()
pygame.display.set_caption("FlappyBird")
pygame.display.set_icon(pygame.image.load('assets/bird1.png'))

bg = background.Background(0, 0, 1.2)
grd = ground.Ground(0, (config.SCREENHEIGTH - (config.SCREENHEIGTH // 6)), 1.2)

start = button.Button(config.SCREENWIDTH/2, config.SCREENHEIGTH/2, 1.3)

Flappy = bird.Bird(config.SCREENWIDTH/2, config.SCREENHEIGTH/2, 1.3)

run = True
game = False


def draw(screen):
    bg.draw(screen)
    grd.draw(screen)
    Flappy.draw(screen)


def update():
    bg.update()
    grd.update()
    Flappy.update()


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            game = True
            Flappy.flap()

    screen.fill('black')

    draw(screen)
    
    if game:
        update()

    if Flappy.img_rect.colliderect(grd.img_rect):
        game = False
        run = False


    clock.tick(config.FPS)
    pygame.display.flip()

pygame.quit()