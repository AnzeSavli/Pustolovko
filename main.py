import pygame, sys
from collectable import *
from controller import *
from enemy import *
from level import *
from player import *
from settings import *
from tiles import *


# ------ INIT ------

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

# ------ GAME CLOCK ------

GAME_CLOCK = pygame.time.Clock()

# ------ SETTINGS ------

settings = Settings()

# ------ SCREEN ------

SCREEN = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

pygame.display.set_caption("Pustolovko")
pygame.display.set_icon(pygame.image.load('./assets/menu/icon/icon.png').convert_alpha())

# ------ ASSETS ------

settings.load_assets("player", "earth", "collectables", "enemies")


# ------ MUSIC ------

# pygame.mixer.music.play(-1)

# ------ BUTTONS ------

resume_image = pygame.image.load('./assets/menu/buttons/resume.png').convert_alpha()
resume_button = Button(settings.SCREEN_WIDTH/2 - resume_image.get_width()/2, (settings.SCREEN_HEIGHT/2 - resume_image.get_height()),resume_image)
start_image = pygame.image.load('./assets/menu/buttons/start.png').convert_alpha()
start_button = Button(settings.SCREEN_WIDTH/2 - start_image.get_width()/2, (settings.SCREEN_HEIGHT/2 - start_image.get_height()),start_image)
settings_image = pygame.image.load('./assets/menu/buttons/settings.png').convert_alpha()
settings_button = Button(settings.SCREEN_WIDTH/2 - resume_image.get_width()/2, (settings.SCREEN_HEIGHT/2 + settings_image.get_height()/4),settings_image)
exit_image = pygame.image.load('./assets/menu/buttons/exit.png').convert_alpha()
exit_button = Button(settings.SCREEN_WIDTH/2 - exit_image.get_width()/2, (settings.SCREEN_HEIGHT/2 + exit_image.get_height() * 3 / 2),exit_image)
video_image = pygame.image.load('./assets/menu/buttons/video.png').convert_alpha()
video_button = Button(settings.SCREEN_WIDTH/2 - video_image.get_width()/2, (settings.SCREEN_HEIGHT / 5 - video_image.get_height()/2), video_image)
audio_image = pygame.image.load('./assets/menu/buttons/audio.png').convert_alpha()
audio_button = Button(settings.SCREEN_WIDTH/2 - audio_image.get_width()/2, (settings.SCREEN_HEIGHT * 2 / 5 - audio_image.get_height()/2), audio_image)
keybinds_image = pygame.image.load('./assets/menu/buttons/keybinds.png').convert_alpha()
keybinds_button = Button(settings.SCREEN_WIDTH/2 - keybinds_image.get_width()/2, (settings.SCREEN_HEIGHT * 3 / 5 - keybinds_image.get_height()/2), keybinds_image)
back_image = pygame.image.load('./assets/menu/buttons/back.png').convert_alpha()
back_button = Button(settings.SCREEN_WIDTH/2 - back_image.get_width()/2, (settings.SCREEN_HEIGHT * 4 / 5 - back_image.get_height()/2), back_image)
music_image = pygame.image.load('./assets/menu/buttons/music.png').convert_alpha()
music_button = Button(settings.SCREEN_WIDTH/2 - music_image.get_width()/2, (settings.SCREEN_HEIGHT * 2 / 5 - music_image.get_height()/2), music_image)
minus_image = pygame.image.load('./assets/menu/buttons/minus.png').convert_alpha()
music_minus_button = Button(settings.SCREEN_WIDTH/2 - music_image.get_width()/2 - 5 - minus_image.get_width(), (settings.SCREEN_HEIGHT * 2 / 5 - music_image.get_height()/2), minus_image)
plus_image = pygame.image.load('./assets/menu/buttons/plus.png').convert_alpha()
music_plus_button = Button(settings.SCREEN_WIDTH/2 + music_image.get_width()/2 + 5, (settings.SCREEN_HEIGHT * 2 / 5 - music_image.get_height()/2), plus_image)

sfx_image = pygame.image.load('./assets/menu/buttons/sfx.png').convert_alpha()
sfx_button = Button(settings.SCREEN_WIDTH/2 - sfx_image.get_width()/2, (settings.SCREEN_HEIGHT * 3 / 5 - sfx_image.get_height()/2), sfx_image)
sfx_minus_button = Button(settings.SCREEN_WIDTH/2 - sfx_image.get_width()/2 - 5 - minus_image.get_width(), (settings.SCREEN_HEIGHT * 3 / 5 - sfx_image.get_height()/2), minus_image)
sfx_plus_button = Button(settings.SCREEN_WIDTH/2 + sfx_image.get_width()/2 + 5, (settings.SCREEN_HEIGHT * 3 / 5 - sfx_image.get_height()/2), plus_image)

# ------ MAIN MENU ------

settings.RUNNING = True
pause_start = 0

while settings.RUNNING:
    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
    if (settings.GAME_PAUSED):

        background_image = pygame.image.load('./assets/menu/bg/bg.png').convert_alpha()
        background_image = pygame.transform.scale(background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        SCREEN.blit(background_image, (0,0))

        if (settings.MENU_STATE == 'main'):
            if start_button.draw(SCREEN):
                settings.GAME_PAUSED = False
                level = Level(settings)
            pass

        if (settings.MENU_STATE == 'pause'):
            pygame.mixer.music.pause()
            title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()
            SCREEN.blit(title_image, ((settings.SCREEN_WIDTH/2 - title_image.get_width()/2),(settings.SCREEN_HEIGHT/4 - title_image.get_height() * 3 / 4)))

            if resume_button.draw(SCREEN):
                settings.GAME_PAUSED = False
                level.pause_time += (pygame.time.get_ticks() - pause_start)
                pause_start = 0
            if settings_button.draw(SCREEN):
                settings.PREVIOUS_MENU = settings.MENU_STATE
                settings.MENU_STATE = "settings"
            if exit_button.draw(SCREEN):
                settings.RUNNING = False

        if (settings.MENU_STATE == "settings"):
            pygame.mixer.music.pause()
            video_button.draw(SCREEN)
            if audio_button.draw(SCREEN):
                settings.PREVIOUS_MENU = settings.MENU_STATE
                settings.MENU_STATE = "audio"

            keybinds_button.draw(SCREEN)
            if back_button.draw(SCREEN):
                settings.MENU_STATE = settings.PREVIOUS_MENU
                settings.PREVIOUS_MENU = "settings"

        if (settings.MENU_STATE == "audio"):
            background_image = pygame.image.load('./assets/menu/bg/bg.png').convert_alpha()
            background_image = pygame.transform.scale(background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            SCREEN.blit(background_image, (0,0))

            if music_button.draw(SCREEN):
                pass
            draw_text(SCREEN, str(int(settings.MUSIC_VOLUME * 100)), settings.FONT, (255,255,255), settings.SCREEN_WIDTH/2 + music_image.get_width()*1/4 - 30, (settings.SCREEN_HEIGHT * 2 / 5 - music_image.get_height()/2 + 10))
            if sfx_button.draw(SCREEN):
                pass
            draw_text(SCREEN, str(int(settings.SFX_VOLUME * 100)), settings.FONT, (255,255,255), settings.SCREEN_WIDTH/2 + music_image.get_width()*1/4 - 30, (settings.SCREEN_HEIGHT * 3 / 5 - music_image.get_height()/2 + 10))    
            if music_plus_button.draw(SCREEN):
                if settings.MUSIC_VOLUME < 1:
                    settings.MUSIC_VOLUME += 0.01
                    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
            if music_minus_button.draw(SCREEN):
                if settings.MUSIC_VOLUME > 0:
                    settings.MUSIC_VOLUME -= 0.01
                    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
            if sfx_plus_button.draw(SCREEN):
                if settings.SFX_VOLUME < 1:
                    settings.SFX_VOLUME += 0.01
            if sfx_minus_button.draw(SCREEN):
                if settings.SFX_VOLUME > 0:
                    settings.SFX_VOLUME -= 0.01

            if back_button.draw(SCREEN):
                settings.MENU_STATE = settings.PREVIOUS_MENU
                settings.PREVIOUS_MENU = "pause"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.RUNNING = False


    else:
        pygame.mixer.music.unpause()
        level.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings.MENU_STATE = 'pause'
                    pause_start = pygame.time.get_ticks()
                    settings.GAME_PAUSED = True


    pygame.display.update()
    GAME_CLOCK.tick(60)

pygame.quit()
sys.exit()



















 #### GAME

# pygame.init()

# SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# pygame.display.set_caption("Pustolovko")
# GAME_CLOCK = pygame.time.Clock()

# level = Level(1)

# #Main loop

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

    
#     level.draw()

#     pygame.display.update()
#     GAME_CLOCK.tick(60)

