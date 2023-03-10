import pygame
from settings import *
import math
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, type, barriers, settings):
        self.settings = settings
        self.size = size
        self.type = type
        self.barriers = barriers
        super().__init__(groups)
        self.animations = self.settings.ASSETS['enemies']
        self.animation_frame = 0
        self.state = 'normal'
        self.previous_state = 'normal'
        self.orientation = 'left'
        self.image = pygame.transform.scale(self.animations[self.type][self.animation_frame], (self.size))
        self.direction = pygame.math.Vector2(-1,0)
        self.speed = 4
        self.rect = self.image.get_rect(topleft= pos)

class Barrier(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, side, settings):
        self.settings = settings
        self.size = size
        self.side = side
        super().__init__(groups)

        self.image = pygame.Surface((size))
        self.rect = self.image.get_rect(topleft=pos)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, type, collidables, settings):
        self.settings = settings
        self.type = type
        self.size = size
        self.collision_blocks = collidables
        super().__init__(groups)
        self.animations = self.settings.ASSETS['enemies']
        self.image = pygame.transform.scale(self.animations[self.type][3], (self.size))
        self.direction = pygame.math.Vector2(0, 1)
        self.speed = 3
        self.rect = self.image.get_rect(topleft=pos)

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.respawn()
            self.kill()

    def map_collision(self):
        for tile in self.collision_blocks.sprites():
            if tile.rect.colliderect(self.rect):
                self.kill()
    
    def out_of_bounds(self):
        if self.rect.y > self.settings.LEVEL_HEIGHT:
            self.kill()


    def update(self, player):
        self.rect.y += self.direction.y * self.speed *self.settings.Y_SCALE
        self.player_collision(player)
        self.map_collision()
        self.out_of_bounds()
        self.player_collision(player)

class Bat(Enemy):
    def __init__(self, pos, size, groups, type, barriers, collidables, settings):
        super().__init__(pos, size, groups, type, barriers, settings)
        self.collidables = collidables
        self.animation_frames = 2
        self.all_groups = groups
        self.animation_speed = 0.04

    def check_player_distance(self, player): 
        return math.hypot(self.rect.x - player.rect.x, self.rect.y - player.rect.y)

    def collide_player(self, player):
        if pygame.sprite.collide_mask(self, player):
            if not(self.settings.SFX_MUTED):
                    self.settings.SFX['hit'].set_volume(int(self.settings.SFX_VOLUME) / 100)
                    self.settings.SFX['hit'].play()
            self.state = 'dying'

    def spawn_bullets(self,player):
        dist = self.check_player_distance(player)
        if dist <= math.ceil(1000 * (self.settings.X_SCALE + self.settings.Y_SCALE) / 2) and dist > math.ceil(600 * (self.settings.X_SCALE + self.settings.Y_SCALE) / 2):
            if random.randint(0, 200) == 5:
                Bullet(((self.rect.x + self.rect.width / 2), (self.rect.y + self.rect.height)), (math.ceil(self.settings.TILE_SIZE / 4 * self.settings.X_SCALE), math.ceil(self.settings.TILE_SIZE * 3/ 4 * self.settings.Y_SCALE)), self.all_groups, 'bat', self.collidables, self.settings)
        if dist <= math.ceil(600* (self.settings.X_SCALE + self.settings.Y_SCALE) / 2) and dist > math.ceil(300* (self.settings.X_SCALE + self.settings.Y_SCALE) / 2):
            if random.randint(0, 800) == 5:
                Bullet(((self.rect.x + self.rect.width / 2),(self.rect.y + self.rect.height)), (math.ceil(self.settings.TILE_SIZE / 4 * self.settings.X_SCALE), math.ceil(self.settings.TILE_SIZE * 3/ 4 * self.settings.Y_SCALE)), self.all_groups, 'bat', self.collidables, self.settings)
        if dist <= math.ceil(300* (self.settings.X_SCALE + self.settings.Y_SCALE) / 2):
            if random.randint(0, 50) == 5:
                Bullet(((self.rect.x + self.rect.width / 2), (self.rect.y + self.rect.height)), (math.ceil(self.settings.TILE_SIZE / 4 * self.settings.X_SCALE), math.ceil(self.settings.TILE_SIZE * 3/ 4 * self.settings.Y_SCALE)), self.all_groups, 'bat', self.collidables, self.settings)

    def map_collision(self):
        for tile in self.collidables.sprites():
            if tile.rect.colliderect(self.rect):
                self.kill()

    def movement(self):
        if self.state == 'normal':
            for tile in self.barriers.sprites():
                if tile.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        if tile.side == 'left':
                            self.orientation = 'right'
                            self.direction.x = 1
                        else:
                            self.orientation = "left"
                            self.direction.x = -1
                    elif self.direction.x < 0:
                        if tile.side == 'right':
                            self.orientation = 'left'
                            self.direction.x = -1
                        else:
                            self.orientation = "right"
                            self.direction.x = 1

            if self.orientation == "left":
                self.direction.x = -1
            elif self.orientation == "right":
                self.direction.x = 1
        elif self.state == 'dying':
            self.direction.x = 0
            self.direction.y = 1

    def image_handler(self):
        if self.state == 'normal':
            self.animation_frame += self.animation_speed
            if self.animation_frame >= self.animation_frames:
                self.animation_frame = 0
            if self.orientation == 'left':
                self.image = pygame.transform.scale(self.animations[self.type][int(self.animation_frame)], (self.size))
            elif self.orientation == 'right':
                self.image = pygame.transform.flip(pygame.transform.scale(self.animations[self.type][int(self.animation_frame)], (self.size)), True, False)
        elif self.state == 'dying':
            self.animation_frame = 2
            if self.orientation == 'left':
                self.image = pygame.transform.flip(pygame.transform.scale(self.animations[self.type][int(self.animation_frame)], (self.size)), False, True)
            elif self.orientation == 'right':
                self.image = pygame.transform.flip(pygame.transform.scale(self.animations[self.type][int(self.animation_frame)], (self.size)), True, True)

    def update(self, player):
        self.rect.x += self.direction.x * self.speed * self.settings.X_SCALE
        self.rect.y += self.direction.y * self.speed * self.settings.Y_SCALE
        if self.state == 'normal':
            self.collide_player(player)
            self.spawn_bullets(player)
            self.movement()
        elif self.state == 'dying':
            self.map_collision()
        self.image_handler()


class Slime(Enemy):
    def __init__(self, pos, size, groups, type, barriers, settings):
        super().__init__(pos, size, groups, type, barriers, settings)
        self.animation_frames = 2
        self.all_groups = groups
        self.animation_speed = 0.05
        self.detect_range = 400
        self.invsible_timer = 0
        self.state = 'normal'
        self.is_dead = False

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.respawn()

    def check_player_distance(self, player): 
        return math.hypot(self.rect.x - player.rect.x, self.rect.y - player.rect.y) < math.ceil(self.detect_range * (self.settings.X_SCALE + self.settings.Y_SCALE) / 2)

    def make_invisible(self, player):
        if self.check_player_distance(player):
            self.invsible_timer += 0.018
            if self.invsible_timer < 1:
                self.state = 'normal'
            elif self.invsible_timer >= 1 and self.invsible_timer < 2:
                self.state = 'invisible'
            else:
                self.state = 'normal'
                self.invsible_timer = 0
        else:
            self.invsible_timer = 0
            self.state = 'normal'

        if self.state == 'normal':
            self.add(self.all_groups)
        elif self.state == 'invisible':
            for tmp_group in self.groups():
                if tmp_group.__class__.__name__ == 'CameraSprites':
                    self.remove(tmp_group)

    def movement(self):
        for tile in self.barriers.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    if tile.side == 'left':
                        self.orientation = 'right'
                        self.direction.x = 1
                    else:
                        self.orientation = "left"
                        self.direction.x = -1
                elif self.direction.x < 0:
                    if tile.side == 'right':
                        self.orientation = 'left'
                        self.direction.x = -1
                    else:
                        self.orientation = "right"
                        self.direction.x = 1

        if self.orientation == "left":
            self.direction.x = -1
        elif self.orientation == "right":
            self.direction.x = 1

    def image_handler(self):
        self.animation_frame += self.animation_speed
        if self.animation_frame >= self.animation_frames:
            self.animation_frame = 0
        if self.orientation == 'left':
            self.image = pygame.transform.scale(self.animations[self.type][int(self.animation_frame)], (self.size))
        elif self.orientation == 'right':
            self.image = pygame.transform.flip(pygame.transform.scale(self.animations[self.type][int(self.animation_frame)], (self.size)), True, False)

    def update(self, player):
        self.rect.x += self.direction.x * self.speed * self.settings.X_SCALE
        self.movement()
        self.player_collision(player)
        self.make_invisible(player)
        self.image_handler()

class Ghost(Enemy):
    def __init__(self, pos, size, groups, type, barriers, settings):
        super().__init__(pos, size, groups, type, barriers, settings)
        self.detect_range = 200
        self.startpos = (self.rect.x, self.rect.y)


    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.respawn()

    def check_player_distance(self, player): 
        return math.hypot(self.rect.x - player.rect.x, self.rect.y - player.rect.y) < math.ceil(self.detect_range * (self.settings.X_SCALE + self.settings.Y_SCALE) / 2)

    def state_handler(self, player):
        self.previous_state = self.state
        if self.check_player_distance(player):
            self.targetpos = (player.rect.x, player.rect.y)
            self.state = 'detected'
            if self.previous_state == 'normal':
                self.startpos = (self.rect.x, self.rect.y)
        else:
            if self.rect.y == self.startpos[1]:
                self.state = 'normal'
                self.startpos = (self.rect.x, self.rect.y)
            else:
                self.state = 'returning'
            
    def movement(self):
        for tile in self.barriers.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    if tile.side == 'left':
                        self.orientation = 'right'
                        self.direction.x = 1 
                    else:
                        self.orientation = "left"
                        self.direction.x = -1
                elif self.direction.x < 0:
                    if tile.side == 'right':
                        self.orientation = 'left'
                        self.direction.x = -1
                    else:
                        self.orientation = "right"
                        self.direction.x = 1

        if self.orientation == "left":
            self.direction.x = -1
        elif self.orientation == "right":
            self.direction.x = 1

    def calculate_direction(self, target):
        angle = math.atan2(target[1] - self.rect.y, target[0] - self.rect.x)
        self.direction.x = 1 if math.cos(angle) > 0.01 else -1 if math.cos(angle) < -0.01 else 0
        self.direction.y = 1 if math.sin(angle) > 0.01 else -1 if math.sin(angle) < -0.01 else 0

        self.orientation = 'left' if self.direction.x < 0 else 'right'
 
    def move_enemy(self, player):
        self.rect.x += self.direction.x * self.speed * self.settings.X_SCALE
        self.rect.y += self.direction.y * self.speed * self.settings.Y_SCALE
        if self.state == 'normal':
            self.movement()
            self.animation_frame = 0
        elif self.state == 'detected':
            self.calculate_direction(self.targetpos)
            self.animation_frame = 1
        elif self.state == 'returning':
            self.calculate_direction(self.startpos)
            self.animation_frame = 0
        self.state_handler(player)

    def image_handler(self):
        if self.orientation == 'left':
            self.image = pygame.transform.scale(self.animations[self.type][self.animation_frame], (self.size))
        elif self.orientation == 'right':
            self.image = pygame.transform.flip(pygame.transform.scale(self.animations[self.type][self.animation_frame], (self.size)), True, False)

    def update(self, player):
        self.move_enemy(player)
        self.player_collision(player)
        self.image_handler()

