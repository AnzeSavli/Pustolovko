import pygame
import os
from controller import get_images

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft= (x,y))
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Settings():

    def __init__(self):

        # ------ SCREEN ------

        self.TILE_SIZE = 64
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800

        # ------ GAME DATA ------

        self.MAX_LEVEL = 1
        self.CURRENT_LEVEL = 1
        self.LEVEL_HEIGHT = 0
        self.GAME_PAUSED = True
        self.MENU_STATE = "main"
        self.PREVIOUS_MENU = ""
        self.RUNNING = True
        

        # ------ FONTS & COLORS ------

        self.FONT = pygame.font.SysFont("arialblack", 40)
        self.TEXT_COLOR = (0, 0, 0)

        # ------ MUSIC ------

        self.MUSIC_VOLUME = 0.5
        pygame.mixer.music.set_volume(self.MUSIC_VOLUME)
        pygame.mixer.music.load('./assets/sounds/music.wav')

        # ------ SFX ------

        self.SFX_VOLUME = 0.5

        

    
    def load_assets(self, *assetslist):
        self.ASSETS = {key : {} for key in assetslist}
        assets_path = './assets/images/'
        for asset in assetslist:
            path = assets_path + asset + "/"
            self.curr_assets = {data : [] for data in os.listdir(path)}
            for animation in self.curr_assets.keys():
                animation_path = path + animation
                self.ASSETS[asset][animation] = get_images(animation_path)

    def load_menu_assets(self, *assetslist):
        self.ASSETS = {key : {} for key in assetslist}
        assets_path = './assets/menu/'
        for asset in assetslist:
            path = assets_path + asset + "/"
            self.curr_assets = {data : [] for data in os.listdir(path)}
            for animation in self.curr_assets.keys():
                animation_path = path + animation
                self.ASSETS[asset][animation] = get_images(animation_path)