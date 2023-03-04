import pygame
from settings import *
import sys
import requests
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups,theme, type, settings):
        self.settings = settings
        self.theme = theme
        self.size = size
        super().__init__(groups)
        self.animations = self.settings.ASSETS[self.theme]
        self.animation_frame = 0
        self.animation_speed = 0.02
        
        self.image = pygame.transform.scale(self.animations[type][self.animation_frame], (size))
        self.rect = self.image.get_rect(topleft= pos)



class Cloud(Tile):
    def __init__(self, pos, size, groups,theme, type, settings):
        super().__init__(pos, size, groups,theme, type, settings)
        self.animation_speed = 0.004
        self.amount = 0
        self.chance = 150
        self.x_dir = 0
        self.y_dir = 0

    def move_cloud(self):
        if self.amount == 0:
            self.amount = random.randint(50, 150)
            self.x_dir = random.randint(-1,1)
            self.y_dir = random.randint(-1,1)

        if random.randint(0,self.chance) == 0 and self.amount != 0:
            self.rect.x += self.x_dir * 1
            self.rect.y += self.y_dir * 1
            self.amount -= 1

    def update(self):
        self.move_cloud()
        animation = self.animations["clouds"]
        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(animation):
            self.animation_frame = 0
        self.image = pygame.transform.scale(animation[int(self.animation_frame)], (self.size))

class Water(Tile):
    def __init__(self, pos, size, groups,theme, type, settings):
        super().__init__(pos, size, groups,theme, type, settings)
        self.animation_speed = 0.048

    def animate(self):
        animation = self.animations["water"]
        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(animation):
            self.animation_frame = 0
        self.image = pygame.transform.scale(animation[int(self.animation_frame)], (self.size))

    def update(self, player, *__):
        self.animate()
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
                # print(text)
                body = {'player' : self.settings.PLAYER_NAME,
                        'score' : text,
                        'level' : self.settings.CURRENT_LEVEL}
                headers = {'safety_token' : "!A%D*G-KaPdSgVkYp3s6v9y/B?E(H+MbQeThWmZq4t7w!z%C&F)J@NcRfUjXn2r5u8x/A?D(G-KaPdSgVkYp3s6v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D(G+KbPeShVkYp3s6v9y$B&E)H@McQfTjWnZq4t7w!z%C*F-JaNdRgUkXp2s5u8x/A?D(G+KbPeShVmYq3t6w9y$B&E)H@McQfTjWnZr4u7x!A%C*F-JaNd"}
                try:
                    requests.post('http://86.61.23.85:3000/score', json=body, headers=headers)
                except:
                    print('no scoreboard server')
                self.settings.FINISHED = True


