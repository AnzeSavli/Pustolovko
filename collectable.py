import pygame
from settings import *

class Collectable(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups,theme, type, settings):
        self.settings = settings
        self.theme = theme
        self.size = size
        super().__init__(groups)
        self.animations = self.settings.ASSETS['collectables']
        self.animation_frame = 0
        
        self.image = self.animations[type][self.animation_frame]
        self.rect = self.image.get_rect(topleft= pos)

class Coin(Collectable):
    def __init__(self, pos, size, groups,theme, type, settings):
        super().__init__(pos, size, groups, theme, type, settings)
        self.collision_rect = self.rect.copy()
        self.collision_rect.update((self.collision_rect.left + (self.size[0] / 3)), (self.collision_rect.top + (self.size[1] / 3)), (self.size[0] / 3), (self.size[1] / 3))

    def update(self, player):
        if self.collision_rect.colliderect(player.rect):
            self.kill()

class Boost(Collectable):
    def __init__(self, pos, size, groups,theme, type, settings):
        super().__init__(pos, size, groups, theme, type, settings)
        self.collision_rect = self.rect.copy()
        self.collision_rect.update((self.collision_rect.left + (self.size[0] / 3)), (self.collision_rect.top + (self.size[1] / 3)), (self.size[0] / 3), (self.size[1] / 3))

    def update(self, player):
        if self.collision_rect.colliderect(player.rect):
            player.jump_boosted = True
            self.kill()

class Key(Collectable):
    def __init__(self, pos, size, groups,theme, type, settings):
        super().__init__(pos, size, groups, theme, type, settings)
        self.collision_rect = self.rect.copy()
        self.collision_rect.update((self.collision_rect.left + (self.size[0] / 3)), (self.collision_rect.top + (self.size[1] / 3)), (self.size[0] / 3), (self.size[1] / 3))

    def update(self, player):
        if self.collision_rect.colliderect(player.rect):
            self.kill()