import pygame
import math
import json

def draw_text(text: str, size: int, x: int, y: int, display: pygame.display) -> None:
        font_name = "assets/ui_elements/flappy-font.ttf"
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255,255,255))

        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)

        display.blit(text_surface, text_rect)


def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
    t = pygame.time.get_ticks() / 2 % time
    y = math.sin(t / speed) * how_far + overall_y
    return int(y)

def file_load(file) -> dict:
    with open(file, 'r') as file:
        data = json.load(file)
    
    return data