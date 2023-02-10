import pygame, sys, pygame_gui
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
pygame.mixer.set_num_channels(64)

# ------ GAME CLOCK ------

GAME_CLOCK = pygame.time.Clock()

# ------ SETTINGS ------

settings = Settings()

# ------ SCREEN ------

SCREEN = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

pygame.display.set_caption("Pustolovko")
pygame.display.set_icon(pygame.image.load('./assets/menu/icon/icon.png').convert_alpha())

NAME_INPUT = pygame_gui.UIManager((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT), './assets/menu/input/theme.json')

# ------ TEXT FIELD ------

TEXT_FIELD = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((settings.SCREEN_WIDTH/2 - 100, settings.SCREEN_HEIGHT / 2 - 55), (settings.SCREEN_WIDTH*3/7, 50)), manager=NAME_INPUT, object_id="#name_input_field", initial_text=settings.PLAYER_NAME)

# ------ ASSETS ------

settings.load_assets("player", "earth", "collectables", "enemies", "HUD")
settings.load_menu_assets("buttons")
settings.load_sfx()

set_keybinds(settings)

# ------ MUSIC ------

pygame.mixer.music.play(-1)

# ------ BUTTONS ------

start_button = Button(settings.SCREEN_WIDTH/4 - settings.MENU_ASSETS['buttons']['start'].get_width()/2, (settings.SCREEN_HEIGHT/2 - settings.MENU_ASSETS['buttons']['start'].get_height()),settings.MENU_ASSETS['buttons']['start'], settings)
scores_button = Button(settings.SCREEN_WIDTH/4 - settings.MENU_ASSETS['buttons']['scores'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['scores'].get_height() / 3),settings.MENU_ASSETS['buttons']['scores'], settings)
main_settings_button = Button(settings.SCREEN_WIDTH/4 - settings.MENU_ASSETS['buttons']['settings'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['settings'].get_height() * 5 / 3),settings.MENU_ASSETS['buttons']['settings'], settings)
exit_button = Button(settings.SCREEN_WIDTH/4 - settings.MENU_ASSETS['buttons']['exit'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['exit'].get_height() * 3),settings.MENU_ASSETS['buttons']['exit'], settings)

resume_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['resume'].get_width()/2, (settings.SCREEN_HEIGHT/2 - settings.MENU_ASSETS['buttons']['resume'].get_height()),settings.MENU_ASSETS['buttons']['resume'], settings)
settings_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['settings'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['settings'].get_height()/4),settings.MENU_ASSETS['buttons']['settings'], settings)
mainmenu_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['mainmenu'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['mainmenu'].get_height()* 3/2),settings.MENU_ASSETS['buttons']['mainmenu'], settings)

audio_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['audio'].get_width()/2, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['audio'].get_height()), settings.MENU_ASSETS['buttons']['audio'], settings)
keybinds_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['keybinds'].get_width()/2, (settings.SCREEN_HEIGHT /2 + settings.MENU_ASSETS['buttons']['keybinds'].get_height()/4), settings.MENU_ASSETS['buttons']['keybinds'], settings)
back_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['back'].get_width()/2, (settings.SCREEN_HEIGHT / 2 + settings.MENU_ASSETS['buttons']['back'].get_height()*3/2), settings.MENU_ASSETS['buttons']['back'], settings)
music_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['music'].get_width()/2, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['music'].get_height()), settings.MENU_ASSETS['buttons']['music'], settings)
music_minus_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['music'].get_width()/2 - 5 - settings.MENU_ASSETS['buttons']['minus'].get_width(), (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['music'].get_height()), settings.MENU_ASSETS['buttons']['minus'], settings)
music_plus_button = Button(settings.SCREEN_WIDTH/2 + settings.MENU_ASSETS['buttons']['music'].get_width()/2 + 5, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['music'].get_height()), settings.MENU_ASSETS['buttons']['plus'], settings)
sfx_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['sfx'].get_width()/2, (settings.SCREEN_HEIGHT / 2 + settings.MENU_ASSETS['buttons']['sfx'].get_height()/4), settings.MENU_ASSETS['buttons']['sfx'], settings)
sfx_minus_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['sfx'].get_width()/2 - 5 - settings.MENU_ASSETS['buttons']['minus'].get_width(), (settings.SCREEN_HEIGHT / 2 + settings.MENU_ASSETS['buttons']['sfx'].get_height()/4), settings.MENU_ASSETS['buttons']['minus'], settings)
sfx_plus_button = Button(settings.SCREEN_WIDTH/2 + settings.MENU_ASSETS['buttons']['sfx'].get_width()/2 + 5, (settings.SCREEN_HEIGHT / 2 + settings.MENU_ASSETS['buttons']['sfx'].get_height()/4), settings.MENU_ASSETS['buttons']['plus'], settings)

left_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['button'].get_height() * 9 / 4), settings.MENU_ASSETS['buttons']['button'], settings)
right_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['button'].get_height()), settings.MENU_ASSETS['buttons']['button'], settings)
jump_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2, (settings.SCREEN_HEIGHT /2 + settings.MENU_ASSETS['buttons']['button'].get_height()/4), settings.MENU_ASSETS['buttons']['button'], settings)

# ------ MAIN MENU ------

settings.RUNNING = True
pause_start = 0
waiting_input = False
waiting_for = ""

while settings.RUNNING:
    settings.EVENTS = pygame.event.get()

    if (settings.MUSIC_MUTED):
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(int(settings.MUSIC_VOLUME) / 100)


    if not (settings.GAME_PAUSED):

        for event in settings.EVENTS:
            if event.type == pygame.QUIT:
                settings.RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings.MENU_STATE = 'pause'
                    pause_start = pygame.time.get_ticks()
                    settings.MENU_CD = pygame.time.get_ticks()
                    settings.GAME_PAUSED = True
                if event.key == pygame.K_SPACE:
                    settings.SCREEN_WIDTH += 100
                    pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        if not settings.GAME_PAUSED:
            if settings.FINISHED:
                if settings.CURRENT_LEVEL == settings.MAX_LEVEL:
                    settings.CURRENT_LEVEL = 1
                else:
                    settings.CURRENT_LEVEL += 1
                settings.FINISHED = False
                level = Level(settings)

            pygame.mixer.music.unpause()
            level.draw()


    elif (settings.GAME_PAUSED):

        for event in settings.EVENTS:
            if event.type == pygame.QUIT:
                settings.RUNNING = False
            if settings.MENU_STATE == "main":
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#name_input_field" and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.PLAYER_NAME = event.text
                NAME_INPUT.process_events(event)
            if settings.MENU_STATE == "keybinds" and waiting_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if waiting_for == "left":
                            left_button.image = settings.MENU_ASSETS["buttons"]["button"]
                        if waiting_for == "right":
                            right_button.image = settings.MENU_ASSETS["buttons"]["button"]
                        if waiting_for == "jump":
                            jump_button.image = settings.MENU_ASSETS["buttons"]["button"]
                        waiting_for = ""
                        waiting_input = False
                    elif event.key not in [settings.KEYBINDS['left'], settings.KEYBINDS['right'], settings.KEYBINDS['jump']]:
                        if waiting_for == "left":
                            save_settings({
                                'left' : event.key,
                                'right': settings.KEYBINDS['right'],
                                'jump': settings.KEYBINDS['jump']
                            })
                            left_button.image = settings.MENU_ASSETS["buttons"]["button"]
                        elif waiting_for == "right":
                            save_settings({
                                'left' : settings.KEYBINDS['left'],
                                'right': event.key,
                                'jump': settings.KEYBINDS['jump']
                            })
                            right_button.image = settings.MENU_ASSETS["buttons"]["button"]
                        elif waiting_for == "jump":
                            save_settings({
                                'left' : settings.KEYBINDS['left'],
                                'right': settings.KEYBINDS['right'],
                                'jump': event.key
                            })
                            jump_button.image = settings.MENU_ASSETS["buttons"]["button"]

                        set_keybinds(settings)
                        waiting_input = False
                        waiting_for = ""

        background_image = pygame.image.load('./assets/menu/bg/bg.png').convert_alpha()
        background_image = pygame.transform.scale(background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        SCREEN.blit(background_image, (0,0))

        if (settings.MENU_STATE == 'main'):
            print("main menu", settings.GAME_PAUSED, settings.RUNNING)
            NAME_INPUT.update(GAME_CLOCK.tick(60) / 300)
            NAME_INPUT.draw_ui(SCREEN)

            title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()

            SCREEN.blit(title_image, ((settings.SCREEN_WIDTH/2 - title_image.get_width()/2),(settings.SCREEN_HEIGHT/4 - title_image.get_height() * 3 / 4)))
            
            if start_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.GAME_PAUSED = False
                level = Level(settings)
                continue

            if scores_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                pass

            if main_settings_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                # settings.SFX['click'].play()
                settings.PREVIOUS_MENU = "main"
                settings.MENU_STATE = "settings"
                settings.MENU_CD = pygame.time.get_ticks()
                continue

            if exit_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.RUNNING = False
                continue

        if (settings.MENU_STATE == 'pause'):
            print("pause menu", settings.GAME_PAUSED, settings.RUNNING)
            pygame.mixer.music.pause()
            title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()
            SCREEN.blit(title_image, ((settings.SCREEN_WIDTH/2 - title_image.get_width()/2),(settings.SCREEN_HEIGHT/4 - title_image.get_height() * 3 / 4)))

            if resume_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.GAME_PAUSED = False
                level.pause_time += (pygame.time.get_ticks() - pause_start)
                pause_start = 0
                continue

            if settings_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.PREVIOUS_MENU = "pause"
                settings.MENU_STATE = "settings"
                settings.MENU_CD = pygame.time.get_ticks()
                continue

            if mainmenu_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.MENU_STATE = "main"
                settings.MENU_CD = pygame.time.get_ticks()
                continue

        if (settings.MENU_STATE == "settings"):
            print("settings menu", settings.GAME_PAUSED, settings.RUNNING)
            pygame.mixer.music.pause()

            title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()
            SCREEN.blit(title_image, ((settings.SCREEN_WIDTH/2 - title_image.get_width()/2),(settings.SCREEN_HEIGHT/4 - title_image.get_height() * 3 / 4)))

            if audio_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.MENU_STATE = "audio"
                settings.MENU_CD = pygame.time.get_ticks()
                continue

            if keybinds_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.MENU_STATE = "keybinds"
                settings.MENU_CD = pygame.time.get_ticks()
                continue

            if back_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                # settings.SFX['click'].play()
                settings.MENU_STATE = settings.PREVIOUS_MENU
                settings.MENU_CD = pygame.time.get_ticks()
                continue

        if (settings.MENU_STATE == "audio"):
            print("audio menu", settings.GAME_PAUSED, settings.RUNNING)
            background_image = pygame.image.load('./assets/menu/bg/bg.png').convert_alpha()
            background_image = pygame.transform.scale(background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            SCREEN.blit(background_image, (0,0))
            if music_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                if settings.MUSIC_MUTED:
                    settings.MUSIC_MUTED = False
                    music_button.image = settings.MENU_ASSETS["buttons"]["music"]
                else:
                    settings.MUSIC_MUTED = True
                    music_button.image = settings.MENU_ASSETS["buttons"]["music_muted"]

            if sfx_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                if settings.SFX_MUTED:
                    settings.SFX_MUTED = False
                    sfx_button.image = settings.MENU_ASSETS["buttons"]["sfx"]
                else:
                    settings.SFX_MUTED = True
                    sfx_button.image = settings.MENU_ASSETS["buttons"]["sfx_muted"]                

            if music_plus_button.draw_buttons(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                if settings.MUSIC_VOLUME < 100:
                    settings.MUSIC_VOLUME += 0.2
                    pygame.mixer.music.set_volume(int(settings.MUSIC_VOLUME) / 100)
            if music_minus_button.draw_buttons(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                if settings.MUSIC_VOLUME > 0:
                    settings.MUSIC_VOLUME -= 0.2
                    pygame.mixer.music.set_volume(int(settings.MUSIC_VOLUME) / 100)
            if sfx_plus_button.draw_buttons(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                if settings.SFX_VOLUME < 100:
                    settings.SFX_VOLUME += 0.2
                    pygame.mixer.music.set_volume(int(settings.MUSIC_VOLUME) / 100)
            if sfx_minus_button.draw_buttons(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                if settings.SFX_VOLUME > 0:
                    settings.SFX_VOLUME -= 0.2
                    pygame.mixer.music.set_volume(int(settings.MUSIC_VOLUME) / 100)

            draw_text(SCREEN, str(int(settings.MUSIC_VOLUME)), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + settings.MENU_ASSETS['buttons']['music'].get_width()*1/4 - 30, (settings.SCREEN_HEIGHT /2 - settings.MENU_ASSETS['buttons']['music'].get_height() + 10)) if not settings.MUSIC_MUTED else draw_text(SCREEN, str(0), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + settings.MENU_ASSETS['buttons']['music'].get_width()*1/4 - 30, (settings.SCREEN_HEIGHT /2 - settings.MENU_ASSETS['buttons']['music'].get_height() + 10))
            draw_text(SCREEN, str(int(settings.SFX_VOLUME)), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + settings.MENU_ASSETS['buttons']['music'].get_width()*1/4 - 30, (settings.SCREEN_HEIGHT /2 + settings.MENU_ASSETS['buttons']['music'].get_height()/4 + 10)) if not settings.SFX_MUTED else draw_text(SCREEN, str(0), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + settings.MENU_ASSETS['buttons']['music'].get_width()*1/4 - 30, (settings.SCREEN_HEIGHT /2 + settings.MENU_ASSETS['buttons']['music'].get_height()/4 + 10))
            
            if back_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.MENU_STATE = "settings"
                settings.MENU_CD = pygame.time.get_ticks()
                continue

        if (settings.MENU_STATE == "keybinds"):
            print("keybinds menu", settings.GAME_PAUSED, settings.RUNNING)
         

            if left_button.draw(SCREEN) and not waiting_input and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:

 
                left_button.image = settings.MENU_ASSETS["buttons"]["buttonpressed"]
                waiting_input = True
                waiting_for = "left"
            draw_text(SCREEN, "LEFT   ", settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2 + 10, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['button'].get_height() * 9 / 4) + 10)    
            if not waiting_for == "left":
                draw_text(SCREEN, "LEFT    %s" % (pygame.key.name(settings.KEYBINDS['left']).upper()), settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2 + 10, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['button'].get_height() * 9 / 4) + 10)
                             
            if right_button.draw(SCREEN) and not waiting_input and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:

                right_button.image = settings.MENU_ASSETS["buttons"]["buttonpressed"]
                waiting_input = True
                waiting_for = "right"
            draw_text(SCREEN, "RIGHT  ", settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2 + 10, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['button'].get_height()) + 10)    
            if not waiting_for == "right":
                draw_text(SCREEN, "RIGHT  %s" % (pygame.key.name(settings.KEYBINDS['right']).upper()), settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2 + 10, (settings.SCREEN_HEIGHT / 2 - settings.MENU_ASSETS['buttons']['button'].get_height()) + 10)
            if jump_button.draw(SCREEN) and not waiting_input and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                jump_button.image = settings.MENU_ASSETS["buttons"]["buttonpressed"]
                waiting_input = True
                waiting_for = "jump"
            draw_text(SCREEN, "JUMP  ", settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2 + 10, (settings.SCREEN_HEIGHT / 2 + settings.MENU_ASSETS['buttons']['button'].get_height()/4) + 10)    
            if not waiting_for == "jump":
                draw_text(SCREEN, "JUMP   %s" % (pygame.key.name(settings.KEYBINDS['jump']).upper()), settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['button'].get_width()/2 + 10, (settings.SCREEN_HEIGHT / 2 + settings.MENU_ASSETS['buttons']['button'].get_height()/4) + 10)
            if back_button.draw(SCREEN) and not waiting_input and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                settings.MENU_STATE = "settings"
                settings.MENU_CD = pygame.time.get_ticks()
                continue

    else:
        continue

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

