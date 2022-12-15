import os
import pygame

def get_images(path):
    surfaces = []
    for _,__,data in os.walk(path):
        for img in data:
            img_path = path + '/' + img
            surface = pygame.image.load(img_path).convert_alpha()
            surfaces.append(surface)

    return surfaces

def draw_text(SCREEN, text, font, color, x, y):
    img = font.render(text, True, color)
    SCREEN.blit(img, (x, y))