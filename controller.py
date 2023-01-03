import os
import pygame
import json

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

def init_save():
    save = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "jump": pygame.K_UP
    }
    return save

def save_settings(data):
    with open("./saves/settings/settings.json", "w") as file:
        json.dump(data,file)

def load_saved_settings():
    with open("./saves/settings/settings.json", 'r+') as file:
        keybinds = json.load(file)
    return keybinds

def load_saved():
    try:
        saved_keybinds = load_saved_settings()
    except:
        saved_keybinds = init_save()
        save_settings(saved_keybinds)
    return saved_keybinds
        
def set_keybinds(settings):
    for keybind, value in load_saved().items():
        settings.KEYBINDS[keybind] = value