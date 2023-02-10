import pygame
from tiles import *
from player import Player
from settings import *
from collectable import *
from controller import *
from enemy import *

class Level:
    def __init__(self, settings):
        self.maxcoins = 0
        self.display = pygame.display.get_surface()
        self.settings = settings
        self.curr_level = self.settings.CURRENT_LEVEL
    
        self.keys = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.background_decorations = CameraSprites(self.settings)
        self.visible_sprites = MainCamera(self.settings)
        self.visible_enemies = CameraSprites(self.settings)
        self.barriers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.collectable_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group() # Sprites that actively change based on other stuff
        self.animated_sprites = pygame.sprite.Group() # Sprites that animate staticly, not dependant on anything #TODO: use it
        self.theme = 'earth' #if self.settings.CURRENT_LEVEL%3 == 1 else 'space' if self.settings.CURRENT_LEVEL%3 == 2 else 'candy'
        self.setup()
        self.start_time = pygame.time.get_ticks()
        self.pause_time = 0
        
        

    def setup(self):

        #Background decoration
        levelfile = open('./assets/levels/' + str(self.curr_level) + '/background.csv', "r")
        levellines = levelfile.readlines()
        for row_i, row in enumerate(levellines):
            for column_i, column in enumerate(row.split(',')):
                if self.theme == 'earth':
                    if column == '14': 
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE * 2, self.settings.TILE_SIZE), [self.background_decorations], self.theme, "clouds", self.settings)

        levelfile.close()

        levelfile = open('./assets/levels/' + str(self.curr_level) + '/decoration.csv', "r")
        levellines = levelfile.readlines()

        for row_i, row in enumerate(levellines):
            # print(row)
            for column_i, column in enumerate(row.split(',')):
                if self.theme == 'earth':
                    if column == '189':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites], self.theme, "sign_right", self.settings)
                    if column == '123':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites], self.theme, "fence", self.settings)
                    if column == '42':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites], self.theme, "mushroom_1", self.settings)
                    if column == '48':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites], self.theme, "plant", self.settings)

        levelfile.close()

        levelfile = open('./assets/levels/' + str(self.curr_level) + '/interactable.csv', "r")
        levellines = levelfile.readlines()
        for row_i, row in enumerate(levellines):
            # print(row)
            for column_i, column in enumerate(row.split(',')):
                if column == '18':
                    Coin((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collectable_sprites, self.coins], self.theme, "coin", self.settings)
                    self.maxcoins += 1
                if column == '39':
                    Key((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collectable_sprites, self.keys], self.theme, "key_green", self.settings)
                if column == '38':
                    Key((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collectable_sprites, self.keys], self.theme, "key_blue", self.settings)
                if column == '40':
                    Key((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collectable_sprites, self.keys], self.theme, "key_red", self.settings)
                if column == '55':
                    Boost((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collectable_sprites], self.theme, "star", self.settings)

        levelfile.close()

        levelfile = open('./assets/levels/' + str(self.curr_level) + '/enemies.csv', "r")
        levellines = levelfile.readlines()
        for row_i, row in enumerate(levellines):
            # print(row)
            for column_i, column in enumerate(row.split(',')):
                if column == '61':
                    Barrier((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.barriers], 'left', self.settings)
                if column == '62':
                    Barrier((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.barriers], 'right', self.settings)
                if column == '285':
                    Ghost((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE * 3 / 4, self.settings.TILE_SIZE), [self.visible_enemies, self.enemies], "ghost", self.barriers, self.settings)
                if column == '310':
                    Slime((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE + self.settings.TILE_SIZE / 2), (self.settings.TILE_SIZE, self.settings.TILE_SIZE / 2), [self.visible_enemies, self.enemies], "slime", self.barriers, self.settings)
                if column == '259':   
                    Bat((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE + self.settings.TILE_SIZE / 2), (self.settings.TILE_SIZE , self.settings.TILE_SIZE * 3 / 5), [self.visible_enemies, self.enemies], "bat", self.barriers, self.collision_sprites, self.settings)
        levelfile.close()

        levelfile = open('./assets/levels/' + str(self.curr_level) + '/tiles.csv', "r")
        levellines = levelfile.readlines()
        self.settings.LEVEL_HEIGHT = len(levellines) * self.settings.TILE_SIZE
        for row_i, row in enumerate(levellines):
            # print(row)
            for column_i, column in enumerate(row.split(',')):
                if self.theme == 'earth':
                    if column == '142':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collision_sprites], self.theme, "grass_left", self.settings)
                    if column == '143':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collision_sprites], self.theme, "grass_middle", self.settings)
                    if column == '144':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collision_sprites], self.theme, "grass_right", self.settings)
                    if column == '126':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collision_sprites], self.theme, "dirt", self.settings)
                    if column == '125':
                        Tile((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.collision_sprites], self.theme, "grass", self.settings)
                    if column == '156' or column == '155':
                        Water((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.animated_sprites, self.interactable_sprites], self.theme, "water", self.settings)
                    if column == '186':
                        Finish((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites, self.interactable_sprites], self.theme, "finish", self.settings)
                if column == '0':
                    self.player = Player((column_i * self.settings.TILE_SIZE, row_i * self.settings.TILE_SIZE), (self.settings.TILE_SIZE, self.settings.TILE_SIZE), [self.visible_sprites,self.active_sprites],self.collision_sprites, self.settings)  

        levelfile.close()

    def draw_hud(self, time):
        heart_full = pygame.transform.scale(self.settings.ASSETS['HUD']['heart'][0], (32, 32))
        heart_empty = pygame.transform.scale(self.settings.ASSETS['HUD']['heart'][1], (32, 32))

        coin = pygame.transform.scale(self.settings.ASSETS['HUD']['coin'][0], (32, 32))

        blue_full = pygame.transform.scale(self.settings.ASSETS['HUD']['blue'][0], (36, 32))
        blue_empty = pygame.transform.scale(self.settings.ASSETS['HUD']['blue'][1], (36, 32))
        green_full = pygame.transform.scale(self.settings.ASSETS['HUD']['green'][0], (36, 32))
        green_empty = pygame.transform.scale(self.settings.ASSETS['HUD']['green'][1], (36, 32))
        red_full = pygame.transform.scale(self.settings.ASSETS['HUD']['red'][0], (36, 32))
        red_empty = pygame.transform.scale(self.settings.ASSETS['HUD']['red'][1], (36, 32))
        

        for i in range(self.player.health):
            self.display.blit(heart_full, (10 + i*42, 15))
        for i in range(self.player.health, self.settings.MAX_HEALTH):
            self.display.blit(heart_empty, (10 + i*42, 15))
        
        milis = time % 100
        seconds = (time / 1000) % 60
        minutes = (time / (1000 * 60)) % 60 
        text = "%02.0f:%02.0f:%02.0f" % (int(minutes), int(seconds), int(milis))
        draw_text(self.display, text, self.settings.MENU_FONT, self.settings.TEXT_COLOR, self.settings.SCREEN_WIDTH / 2 - self.settings.SCREEN_WIDTH / 10, 0)

        self.display.blit(coin, (self.settings.SCREEN_WIDTH * 5 / 7, 15))

        coin_count = "%d/%d" % (self.maxcoins - len(self.coins), self.maxcoins)
        draw_text(self.display, coin_count, self.settings.MENU_FONT, (255,204,0), self.settings.SCREEN_WIDTH * 5 / 7 + 40, 6)

        if "green" in [key.key_color for key in self.keys]:
            self.display.blit(green_empty, (self.settings.SCREEN_WIDTH * 6 / 7, 15))
        else:
            self.display.blit(green_full, (self.settings.SCREEN_WIDTH * 6 / 7, 15))
        if "blue" in [key.key_color for key in self.keys]:
            self.display.blit(blue_empty, (self.settings.SCREEN_WIDTH * 6 / 7 + 40, 15))
        else:
            self.display.blit(blue_full, (self.settings.SCREEN_WIDTH * 6 / 7 + 40, 15))
        if "red" in [key.key_color for key in self.keys]:
            self.display.blit(red_empty, (self.settings.SCREEN_WIDTH * 6 / 7 + 80, 15))
        else:
            self.display.blit(red_full, (self.settings.SCREEN_WIDTH * 6 / 7 + 80, 15))



    def draw(self):
        curr_time = pygame.time.get_ticks()
        time = (curr_time - self.start_time - self.pause_time)
        
        
        self.collectable_sprites.update(self.player)
        self.interactable_sprites.update(self.player, self.keys, time + len(self.coins)*5000)
        self.enemies.update(self.player)
        self.active_sprites.update()
        
        bg = pygame.image.load('./assets/images/' + self.theme + '/bg/bg.png').convert_alpha()
        bg = pygame.transform.scale(bg, (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        self.display.blit(bg, (0,0))
        self.background_decorations.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)
        self.visible_enemies.custom_draw(self.player)
        
        self.draw_hud(time)


class MainCamera(pygame.sprite.Group):
    def __init__(self, settings):
        self.settings = settings
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2((self.settings.SCREEN_WIDTH / 9),(self.settings.SCREEN_HEIGHT / 4))

        # camera
        cam_left = self.settings.SCREEN_WIDTH / 9
        cam_top = self.settings.SCREEN_HEIGHT / 4
        cam_width = self.display_surface.get_size()[0] - (cam_left + (self.settings.SCREEN_WIDTH / 8))
        cam_height = self.display_surface.get_size()[1] - (cam_top * 5 / 2)

        self.camera_rect = pygame.Rect(cam_left,cam_top,cam_width,cam_height)

    def custom_draw(self,player):
        self.drawn = 0
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # camera offset 
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - (self.settings.SCREEN_WIDTH / 9),
            self.camera_rect.top - (self.settings.SCREEN_HEIGHT / 4))
        for sprite in self.sprites():
            if sprite.rect.left + sprite.rect.width < (self.camera_rect.left - (self.settings.SCREEN_WIDTH / 9)) or sprite.rect.left > (self.camera_rect.left - (self.settings.SCREEN_WIDTH / 9) + self.settings.SCREEN_WIDTH) or sprite.rect.top + sprite.rect.height < (self.camera_rect.top - (self.settings.SCREEN_HEIGHT / 4)) or sprite.rect.top > (self.camera_rect.top - (self.settings.SCREEN_HEIGHT / 4) + self.settings.SCREEN_HEIGHT):
                continue
            if sprite == player:
                continue
            else:
                self.drawn += 1
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)

        offset_pos = player.rect.topleft - self.offset
        self.display_surface.blit(player.image,offset_pos)
        player_name = self.settings.NAME_FONT.render(self.settings.PLAYER_NAME, True, self.settings.TEXT_COLOR)
        self.display_surface.blit(player_name, (offset_pos.x - player_name.get_width()/2 + player.rect.width / 2, offset_pos.y - player_name.get_height() - 5))

        # print("drawn: %d/%d" % (self.drawn + 1, len(self.sprites())))


class CameraSprites(pygame.sprite.Group):
    def __init__(self, settings):
        self.settings = settings
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2((self.settings.SCREEN_WIDTH / 9),(self.settings.SCREEN_HEIGHT / 4))

        # camera
        cam_left = self.settings.SCREEN_WIDTH / 9
        cam_top = self.settings.SCREEN_HEIGHT / 4
        cam_width = self.display_surface.get_size()[0] - (cam_left + (self.settings.SCREEN_WIDTH / 8))
        cam_height = self.display_surface.get_size()[1] - (cam_top * 5 / 2)

        self.camera_rect = pygame.Rect(cam_left,cam_top,cam_width,cam_height)

    def custom_draw(self,player):
        self.drawn = 0
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # camera offset 
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - (self.settings.SCREEN_WIDTH / 9),
            self.camera_rect.top - (self.settings.SCREEN_HEIGHT / 4))
        for sprite in self.sprites():
            if sprite.rect.left + sprite.rect.width < (self.camera_rect.left - (self.settings.SCREEN_WIDTH / 9)) or sprite.rect.left > (self.camera_rect.left - (self.settings.SCREEN_WIDTH / 9) + self.settings.SCREEN_WIDTH) or sprite.rect.top + sprite.rect.height  < (self.camera_rect.top - (self.settings.SCREEN_HEIGHT / 4)) or sprite.rect.top  > (self.camera_rect.top - (self.settings.SCREEN_HEIGHT / 4) + self.settings.SCREEN_HEIGHT):
                continue
            self.drawn += 1
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
