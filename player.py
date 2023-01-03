import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, collision_sprites, settings): #, collectable_sprites
        self.settings = settings
        self.size = size
        super().__init__(groups)
        self.animations = self.settings.ASSETS['player']
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.state = 'stand'
        self.last_direction = 'right'
        self.in_water = False
        self.slimed = False
        self.grounded = False
        self.jump_boosted = False
        self.image = pygame.transform.scale(self.animations[self.state][self.animation_frame], (size))
        self.rect = self.image.get_rect(topleft = pos)
        self.start_pos = pos
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.55
        self.jump_span = -12
        self.max_jumps = 1
        self.jump_amounts = self.max_jumps
        self.jump_on_cooldown =  False
        self.health = 3
        self.walking_timer = 0

        self.collision_sprites = collision_sprites

    def check_movement(self):  
        keys = pygame.key.get_pressed()


        if keys[self.settings.KEYBINDS['right']]:
            self.direction.x = 1
            self.last_direction = 'right'
        elif keys[self.settings.KEYBINDS['left']]:
            self.direction.x = -1
            self.last_direction = 'left'
        else:
            self.direction.x = 0
        if keys[self.settings.KEYBINDS['jump']] and self.jump_amounts > 0 and not self.jump_on_cooldown:
            if not(self.settings.SFX_MUTED):
                    self.settings.SFX['jump2'].set_volume(int(self.settings.SFX_VOLUME) / 100)
                    self.settings.SFX['jump2'].play()
            self.jump()
            self.jump_on_cooldown = True
        
        if not keys[self.settings.KEYBINDS['jump']]:
            self.jump_on_cooldown = False


    def get_state(self):
        if self.in_water:
            self.state = 'swim'
        elif self.direction.y < 0:
            self.state = 'jump'
        elif self.direction.y > self.gravity:
            self.state = 'fall'
        elif self.direction.x > 0:
            self.state = 'run'
        elif self.direction.x < 0:
            self.state = 'run'
        else:
            self.state = 'stand'
        

    def show_animations(self):
        animation = self.animations[self.state]
        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(animation):
            self.animation_frame = 0
        if self.last_direction == 'right' : 
            self.image = pygame.transform.scale(animation[int(self.animation_frame)], (self.size))
        else:
            self.image = pygame.transform.flip(pygame.transform.scale(animation[int(self.animation_frame)], (self.size)), True, False)

        if self.grounded:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)

    def movement_collision(self):
        for tile in self.collision_sprites.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = tile.rect.right
                elif self.direction.x > 0:
                    self.rect.right = tile.rect.left

    def jump_collision(self):
        for tile in self.collision_sprites.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                    self.jump_amounts = self.max_jumps
                    self.grounded = True
                elif self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.direction.y = 0
        
        if self.grounded and self.direction.y != 0:
            self.grounded = False


    def fall(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if not self.jump_on_cooldown:
            self.direction.y = self.jump_span
            self.jump_amounts = self.jump_amounts - 1 if self.jump_amounts > 0 else 0

    def player_died(self):
        if self.health == 0:
            self.settings.GAME_PAUSED = True
            self.settings.MENU_STATE = "main"

    def  map_limits(self):
        if (self.rect.y > self.settings.LEVEL_HEIGHT + 4*self.settings.TILE_SIZE):
            self.respawn()

    def check_water(self):
        if(self.in_water):
            self.speed = 3
            self.jump_span = -9
            # self.in_water = False
        else:
            self.speed = 8
            self.jump_span = -12

    def check_boost(self):
        if (self.jump_boosted):
            self.max_jumps = 2

    def respawn(self):
        self.health -= 1
        self.direction = pygame.math.Vector2(0,0)
        self.rect.topleft = self.start_pos

    def update(self):
        self.player_died()
        self.check_water()
        self.map_limits()
        self.check_movement()
        self.check_boost()
        self.rect.x += self.direction.x * self.speed
        self.movement_collision()
        self.fall()
        self.jump_collision()
        self.get_state()
        self.show_animations()
        self.in_water = False
        
        