import pygame
from settings import *
import sys

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups,theme, type, settings):
        self.settings = settings
        self.theme = theme
        self.size = size
        super().__init__(groups)
        self.animations = self.settings.ASSETS[self.theme]
        self.animation_frame = 0
        
        self.image = pygame.transform.scale(self.animations[type][self.animation_frame], (size))
        self.rect = self.image.get_rect(topleft= pos)
        

class Water(Tile):
    def __init__(self, pos, size, groups,theme, type, settings):
        super().__init__(pos, size, groups,theme, type, settings)

    def update(self, player, *__):
        if self.rect.colliderect(player.rect):
            player.in_water = True


class Finish(Tile):
    def __init__(self, pos, size, groups,theme, type, settings):
        super().__init__(pos, size, groups,theme, type, settings)
        self.can_finish = False
        self.collision_rect = self.rect.copy()
        self.collision_rect.update((self.collision_rect.left + (self.size[0] / 3)), (self.collision_rect.top + (self.size[1] / 3)), (self.size[0] / 3), (self.size[1] / 3))

    
    def change_image(self):
        animation = self.animations["finish"]
        self.image = pygame.transform.scale(animation[int(self.animation_frame)], (self.size))

    def update(self, player, keys, time, *__):
        if len(keys.sprites()) == 0:
            self.can_finish = True
            self.animation_frame = 1
            self.change_image()
        
        if self.can_finish:
            if self.collision_rect.colliderect(player.rect):
                milis = time % 100
                seconds = (time / 1000) % 60
                minutes = (time / (1000 * 60)) % 60 
                text = "%02.0f:%02.0f:%02.0f" % (int(minutes), int(seconds), int(milis))
                print(text)

                self.settings.FINISHED = True


