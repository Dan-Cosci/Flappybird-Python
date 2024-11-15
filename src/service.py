import pygame
import math
import json
import random

from src import config



def draw_text(text: str, size: int, x: int, y: int, display: pygame.display, color=(255,255,255)) -> None:
        font_name = "assets/ui_elements/flappy-font.ttf"
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)

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


def file_save(file, data: dict) -> None:
    with open(file, 'w') as file:
        json.dump(data, file, indent = 8)


def draw_quote(text: str, size: int, x: int, y: int, display: pygame.display, color=(255,255,255)) -> None:
    sentences = []
    for lines in text.splitlines():
        sentences.append(lines)

    font_name = "assets/ui_elements/flappy-font.ttf"
    font = pygame.font.Font(font_name, size)

    for lines, offset in zip(sentences, range(1, len(sentences)+1)):
        text_surface = font.render(lines, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y + 25 * offset)

        display.blit(text_surface, text_rect)


def quote(score: int, high: bool = False) -> str:
    data  = file_load(config.FILE_NAME)

    if high:
        quotes = data['score']['highscore_quotes']
        length = len(quotes)
        index = random.randint(0,length - 1)
    else:
        quotes = data['score']['lowscore_quotes']        
        if score == 1:
            return "Oh, a whole 1 point?\nYou're really\nsetting records here"
        
        if score == 2:
            return "Wow, two pipes!\nThey will be writing songs\nabout this achievement"
        if score == 4:
            return "Let's be real you are not\ngoing to get past 5"
        else:
            length = len(quotes)
            index = random.randint(0,length - 1)
    
    return quotes[index]