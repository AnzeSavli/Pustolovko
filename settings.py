import pygame
import os
import math
from controller import get_images

class Button():
    def __init__(self, x, y, image, settings):
        self.settings = settings
        self.image = pygame.transform.scale(image, (math.ceil(image.get_width() * settings.X_SCALE), math.ceil(image.get_height() * settings.Y_SCALE)))
        self.rect = self.image.get_rect(topleft= (x,y))
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and (pygame.time.get_ticks() - self.settings.MENU_BUTTON_PRESSED) >= 150:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                self.settings.MENU_BUTTON_PRESSED = pygame.time.get_ticks()
                # pygame.mixer.Sound.play(self.settings.SFX['click'])
                # if not self.settings.SFX_MUTED and not pygame.mixer.Channel(33).get_busy():
                #     pygame.mixer.Channel(33).play(self.settings.SFX['click'])

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
    def draw_buttons(self, surface):

        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                action = True
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                action = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Settings():

    def __init__(self):

        # ------ SCREEN ------

        self.TILE_SIZE = 64
        self.ORIGINAL_SCREEN_WIDTH = 1200
        self.ORIGINAL_SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800

        self.X_SCALE = 1
        self.Y_SCALE = 1
        

        # ------ GAME DATA ------

        self.MAX_LEVEL = 3
        self.CURRENT_LEVEL = 1
        self.LEVEL_HEIGHT = 0
        self.FINISHED = False
        self.GAME_PAUSED = True
        self.MENU_STATE = "main"
        self.PREVIOUS_MENU = "main"
        self.MENU_CD = 0
        self.RUNNING = True
        self.MENU_BUTTON_PRESSED = 0
        self.KEYBINDS = dict()
        self.EVENTS = None
        

        # ------ FONTS & COLORS ------

        self.MENU_FONT = pygame.font.Font("./assets/fonts/GILLUBCD.TTF", 40)
        self.NAME_FONT = pygame.font.Font("./assets/fonts/GILLUBCD.TTF", 24)
        self.TEXT_COLOR = (0, 0, 0)

        # ------ MUSIC ------

        self.MUSIC_VOLUME = 10
        self.MUSIC_MUTED = False
        pygame.mixer.music.set_volume(int(self.MUSIC_VOLUME) / 100)
        pygame.mixer.music.load('./assets/sounds/music.wav')

        # ------ SFX ------

        self.SFX_VOLUME = 70
        self.SFX_MUTED = False

        # ------ PLAYER DATA ------

        self.PLAYER_NAME = "Player"
        self.MAX_HEALTH = 3

    
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
        self.MENU_ASSETS = {key : {} for key in assetslist}
        assets_path = './assets/menu/'
        for asset in assetslist:
            path = assets_path + asset + "/"
            for _,__, data in os.walk(path):
                for image in data:
                    self.MENU_ASSETS[asset][image.split('.', 1)[0]] = pygame.image.load(path + image).convert_alpha()

    def load_sfx(self):
        self.SFX = dict()

        assets_path = './assets/sounds/sfx/'

        for _,__,data in os.walk(assets_path):
            for sound in data:
                self.SFX[sound.split('.', 1)[0]] = pygame.mixer.Sound(assets_path + sound)

