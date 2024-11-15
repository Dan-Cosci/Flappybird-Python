import pygame
import math
import json
import random



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


def quote(score: int) -> str:
    quotes = [
          "Flapping through\nliFe aimlessly…\njust like you",
          "Flapping with all\nthe grace oF a\nbrick in water",
          "That pipe did not move\nJust saying",
          "This is the best\nyou will achieve\nall day",
          "No one believes in you\nespecially this bird",
          "A legend in\nyour own mind",
          "Keep trying\nYou’re only getting\nslightly less terrible",
          "You're really out here\ntrying huh?",
        "That was…\nwell...\nit was something",
        "At this rate, even\na snail would lap you",
        "This is deFinitely\nyour Finest\nattempt yet",
        "You’re almost there!\njust kidding\nnot even close",
        "Did you even\ntry that time?",
        "Wow, you’re still\nplaying? That’s\ndetermination or denial",
        "IF only eFFort\ncounted For anything",
        "One day you will\nget it Today is\njust not that day"
          ]
          
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