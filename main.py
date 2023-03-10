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

SCREEN = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Pustolovko")
pygame.display.set_icon(pygame.image.load('./assets/menu/icon/icon.png').convert_alpha())

NAME_INPUT = pygame_gui.UIManager((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT), './assets/menu/input/theme.json')

# ------ TEXT FIELD ------

TEXT_FIELD = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((settings.SCREEN_WIDTH/4 - 37, settings.SCREEN_HEIGHT / 2 - 100), (settings.SCREEN_WIDTH*9/16, 50)), manager=NAME_INPUT, object_id="#name_input_field", initial_text=settings.PLAYER_NAME)

# ------ ASSETS ------

settings.load_assets("player", "earth", "collectables", "enemies", "HUD")
settings.load_menu_assets("buttons")
settings.load_sfx()

set_keybinds(settings)

# ------ MUSIC ------

pygame.mixer.music.play(-1)

# ------ BUTTONS ------
start_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['start'].get_width()/2, (settings.SCREEN_HEIGHT/2 - settings.MENU_ASSETS['buttons']['start'].get_height()),settings.MENU_ASSETS['buttons']['start'], settings)
# scores_button = Button(settings.SCREEN_WIDTH/4 - settings.MENU_ASSETS['buttons']['scores'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['scores'].get_height() / 3),settings.MENU_ASSETS['buttons']['scores'], settings)
main_settings_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['settings'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['settings'].get_height() /4),settings.MENU_ASSETS['buttons']['settings'], settings)
exit_button = Button(settings.SCREEN_WIDTH/2 - settings.MENU_ASSETS['buttons']['exit'].get_width()/2, (settings.SCREEN_HEIGHT/2 + settings.MENU_ASSETS['buttons']['exit'].get_height()* 3/2),settings.MENU_ASSETS['buttons']['exit'], settings)

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

level_1_button = Button(settings.SCREEN_WIDTH / 4 - math.ceil(settings.MENU_ASSETS['buttons']['1'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['1'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['1'], settings)
level_2_button = Button(settings.SCREEN_WIDTH * 3/8 - math.ceil(settings.MENU_ASSETS['buttons']['2'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['2'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['2'], settings)
level_3_button = Button(settings.SCREEN_WIDTH / 2- math.ceil(settings.MENU_ASSETS['buttons']['3'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['3'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['3'], settings)
level_4_button = Button(settings.SCREEN_WIDTH * 5/8 - math.ceil(settings.MENU_ASSETS['buttons']['4'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['4'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['4'], settings)
level_5_button = Button(settings.SCREEN_WIDTH * 3/4 - math.ceil(settings.MENU_ASSETS['buttons']['5'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['5'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['5'], settings)
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
            if event.type == pygame.VIDEORESIZE:
                if (SCREEN.get_width() < 1200):
                    settings.SCREEN_WIDTH = 1200
                else:
                    settings.SCREEN_WIDTH = SCREEN.get_width()
                if (SCREEN.get_height() < 800):
                    settings.SCREEN_HEIGHT = 800
                else:
                    settings.SCREEN_HEIGHT = SCREEN.get_height()
                pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
                settings.X_SCALE = settings.SCREEN_WIDTH / settings.ORIGINAL_SCREEN_WIDTH
                settings.Y_SCALE = settings.SCREEN_HEIGHT / settings.ORIGINAL_SCREEN_HEIGHT

                NAME_INPUT = pygame_gui.UIManager((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT), './assets/menu/input/theme.json')

                # ------ TEXT FIELD ------
                TEXT_FIELD = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((settings.SCREEN_WIDTH/4 - math.ceil(37 * settings.X_SCALE), settings.SCREEN_HEIGHT / 2 - math.ceil(100 * settings.Y_SCALE)), (settings.SCREEN_WIDTH*9/16, math.ceil(50 * settings.Y_SCALE))), manager=NAME_INPUT, object_id="#name_input_field", initial_text=settings.PLAYER_NAME)

                start_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['start'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 - math.ceil(settings.MENU_ASSETS['buttons']['start'].get_height() * settings.Y_SCALE)),settings.MENU_ASSETS['buttons']['start'], settings)
                # scores_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['scores'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['scores'].get_height() * settings.Y_SCALE) / 3),settings.MENU_ASSETS['buttons']['scores'], settings)
                main_settings_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_height() * settings.Y_SCALE) /4),settings.MENU_ASSETS['buttons']['settings'], settings)
                exit_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['exit'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['exit'].get_height() * settings.Y_SCALE) * 3/2),settings.MENU_ASSETS['buttons']['exit'], settings)

                resume_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['resume'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 - math.ceil(settings.MENU_ASSETS['buttons']['resume'].get_height() * settings.Y_SCALE)),settings.MENU_ASSETS['buttons']['resume'], settings)
                settings_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_height() * settings.Y_SCALE)/4),settings.MENU_ASSETS['buttons']['settings'], settings)
                mainmenu_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['mainmenu'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['mainmenu'].get_height() * settings.Y_SCALE)* 3/2),settings.MENU_ASSETS['buttons']['mainmenu'], settings)

                audio_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['audio'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['audio'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['audio'], settings)
                keybinds_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['keybinds'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT /2 + math.ceil(settings.MENU_ASSETS['buttons']['keybinds'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['keybinds'], settings)
                back_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['back'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['back'].get_height() * settings.Y_SCALE)*3/2), settings.MENU_ASSETS['buttons']['back'], settings)
                music_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['music'], settings)
                music_minus_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width() * settings.X_SCALE)/2 - math.ceil(5 * settings.X_SCALE) - math.ceil(settings.MENU_ASSETS['buttons']['minus'].get_width() * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['minus'], settings)
                music_plus_button = Button(settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width() * settings.X_SCALE)/2 + math.ceil(5 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['plus'], settings)
                sfx_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['sfx'], settings)
                sfx_minus_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_width() * settings.X_SCALE)/2 - math.ceil(5 * settings.X_SCALE) - math.ceil(settings.MENU_ASSETS['buttons']['minus'].get_width() * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['minus'], settings)
                sfx_plus_button = Button(settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_width() * settings.X_SCALE)/2 + math.ceil(5 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['plus'], settings)

                left_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE) * 9 / 4), settings.MENU_ASSETS['buttons']['button'], settings)
                right_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['button'], settings)
                jump_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT /2 + math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['button'], settings)

                level_1_button = Button(settings.SCREEN_WIDTH / 4 - math.ceil(settings.MENU_ASSETS['buttons']['1'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['1'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['1'], settings)
                level_2_button = Button(settings.SCREEN_WIDTH * 3/8 - math.ceil(settings.MENU_ASSETS['buttons']['2'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['2'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['2'], settings)
                level_3_button = Button(settings.SCREEN_WIDTH / 2- math.ceil(settings.MENU_ASSETS['buttons']['3'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['3'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['3'], settings)
                level_4_button = Button(settings.SCREEN_WIDTH * 5/8 - math.ceil(settings.MENU_ASSETS['buttons']['4'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['4'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['4'], settings)
                level_5_button = Button(settings.SCREEN_WIDTH * 3/4 - math.ceil(settings.MENU_ASSETS['buttons']['5'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['5'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['5'], settings)

                level = Level(settings)

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
            if event.type == pygame.VIDEORESIZE:
                if (SCREEN.get_width() < 1200):
                    settings.SCREEN_WIDTH = 1200
                else:
                    settings.SCREEN_WIDTH = SCREEN.get_width()
                if (SCREEN.get_height() < 800):
                    settings.SCREEN_HEIGHT = 800
                else:
                    settings.SCREEN_HEIGHT = SCREEN.get_height()
                pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
                settings.X_SCALE = settings.SCREEN_WIDTH / settings.ORIGINAL_SCREEN_WIDTH
                settings.Y_SCALE = settings.SCREEN_HEIGHT / settings.ORIGINAL_SCREEN_HEIGHT

                NAME_INPUT = pygame_gui.UIManager((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT), './assets/menu/input/theme.json')

                # ------ TEXT FIELD ------

                TEXT_FIELD = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((settings.SCREEN_WIDTH/4 - math.ceil(37 * settings.X_SCALE), settings.SCREEN_HEIGHT / 2 - math.ceil(100 * settings.Y_SCALE)), (settings.SCREEN_WIDTH*9/16, math.ceil(50 * settings.Y_SCALE))), manager=NAME_INPUT, object_id="#name_input_field", initial_text=settings.PLAYER_NAME)

                start_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['start'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 - math.ceil(settings.MENU_ASSETS['buttons']['start'].get_height() * settings.Y_SCALE)),settings.MENU_ASSETS['buttons']['start'], settings)
                # scores_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['scores'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['scores'].get_height() * settings.Y_SCALE) / 3),settings.MENU_ASSETS['buttons']['scores'], settings)
                main_settings_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_height() * settings.Y_SCALE) / 4),settings.MENU_ASSETS['buttons']['settings'], settings)
                exit_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['exit'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['exit'].get_height() * settings.Y_SCALE) * 3/2),settings.MENU_ASSETS['buttons']['exit'], settings)

                resume_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['resume'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 - math.ceil(settings.MENU_ASSETS['buttons']['resume'].get_height() * settings.Y_SCALE)),settings.MENU_ASSETS['buttons']['resume'], settings)
                settings_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['settings'].get_height() * settings.Y_SCALE)/4),settings.MENU_ASSETS['buttons']['settings'], settings)
                mainmenu_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['mainmenu'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT/2 + math.ceil(settings.MENU_ASSETS['buttons']['mainmenu'].get_height() * settings.Y_SCALE)* 3/2),settings.MENU_ASSETS['buttons']['mainmenu'], settings)

                audio_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['audio'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['audio'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['audio'], settings)
                keybinds_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['keybinds'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT /2 + math.ceil(settings.MENU_ASSETS['buttons']['keybinds'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['keybinds'], settings)
                back_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['back'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['back'].get_height() * settings.Y_SCALE)*3/2), settings.MENU_ASSETS['buttons']['back'], settings)
                music_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['music'], settings)
                music_minus_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width() * settings.X_SCALE)/2 - math.ceil(5 * settings.X_SCALE) - math.ceil(settings.MENU_ASSETS['buttons']['minus'].get_width() * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['minus'], settings)
                music_plus_button = Button(settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width() * settings.X_SCALE)/2 + math.ceil(5 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['plus'], settings)
                sfx_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['sfx'], settings)
                sfx_minus_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_width() * settings.X_SCALE)/2 - math.ceil(5 * settings.X_SCALE) - math.ceil(settings.MENU_ASSETS['buttons']['minus'].get_width() * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['minus'], settings)
                sfx_plus_button = Button(settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_width() * settings.X_SCALE)/2 + math.ceil(5 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['sfx'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['plus'], settings)

                left_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE) * 9 / 4), settings.MENU_ASSETS['buttons']['button'], settings)
                right_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['button'], settings)
                jump_button = Button(settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT /2 + math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)/4), settings.MENU_ASSETS['buttons']['button'], settings)

                level_1_button = Button(settings.SCREEN_WIDTH / 4 - math.ceil(settings.MENU_ASSETS['buttons']['1'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['1'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['1'], settings)
                level_2_button = Button(settings.SCREEN_WIDTH * 3/8 - math.ceil(settings.MENU_ASSETS['buttons']['2'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['2'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['2'], settings)
                level_3_button = Button(settings.SCREEN_WIDTH / 2- math.ceil(settings.MENU_ASSETS['buttons']['3'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['3'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['3'], settings)
                level_4_button = Button(settings.SCREEN_WIDTH * 5/8 - math.ceil(settings.MENU_ASSETS['buttons']['4'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['4'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['4'], settings)
                level_5_button = Button(settings.SCREEN_WIDTH * 3/4 - math.ceil(settings.MENU_ASSETS['buttons']['5'].get_width() * settings.X_SCALE)/2, (settings.SCREEN_HEIGHT * 2 / 3 - math.ceil(settings.MENU_ASSETS['buttons']['5'].get_height() * settings.Y_SCALE)), settings.MENU_ASSETS['buttons']['5'], settings)

                level = Level(settings)

            if settings.TUTORIAL == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if settings.TUTORIAL_LEVEL == 4:
                        settings.TUTORIAL = True
                        settings.write_tutorial_state({'tutorial' : True})
                    else:
                        settings.TUTORIAL_LEVEL += 1
            if settings.MENU_STATE == "lvlsel":
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#name_input_field" and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.PLAYER_NAME = event.text
                NAME_INPUT.process_events(event)
            if settings.MENU_STATE == "keybinds" and waiting_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if waiting_for == "left":
                            left_button.image = settings.MENU_ASSETS["buttons"]["button"]
                            left_button.image = pygame.transform.scale(left_button.image, (math.ceil(left_button.image.get_width() * settings.X_SCALE), math.ceil(left_button.image.get_height() * settings.Y_SCALE)))
                        if waiting_for == "right":
                            right_button.image = settings.MENU_ASSETS["buttons"]["button"]
                            right_button.image = pygame.transform.scale(right_button.image, (math.ceil(right_button.image.get_width() * settings.X_SCALE), math.ceil(right_button.image.get_height() * settings.Y_SCALE)))
                        if waiting_for == "jump":
                            jump_button.image = settings.MENU_ASSETS["buttons"]["button"]
                            jump_button.image = pygame.transform.scale(jump_button.image, (math.ceil(jump_button.image.get_width() * settings.X_SCALE), math.ceil(jump_button.image.get_height() * settings.Y_SCALE)))
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
                            left_button.image = pygame.transform.scale(left_button.image, (math.ceil(left_button.image.get_width() * settings.X_SCALE), math.ceil(left_button.image.get_height() * settings.Y_SCALE)))
                        elif waiting_for == "right":
                            save_settings({
                                'left' : settings.KEYBINDS['left'],
                                'right': event.key,
                                'jump': settings.KEYBINDS['jump']
                            })
                            right_button.image = settings.MENU_ASSETS["buttons"]["button"]
                            right_button.image = pygame.transform.scale(right_button.image, (math.ceil(right_button.image.get_width() * settings.X_SCALE), math.ceil(right_button.image.get_height() * settings.Y_SCALE)))
                        elif waiting_for == "jump":
                            save_settings({
                                'left' : settings.KEYBINDS['left'],
                                'right': settings.KEYBINDS['right'],
                                'jump': event.key
                            })
                            jump_button.image = settings.MENU_ASSETS["buttons"]["button"]
                            jump_button.image = pygame.transform.scale(jump_button.image, (math.ceil(jump_button.image.get_width() * settings.X_SCALE), math.ceil(jump_button.image.get_height() * settings.Y_SCALE)))
                        set_keybinds(settings)
                        waiting_input = False
                        waiting_for = ""

        background_image = pygame.image.load('./assets/menu/bg/bg.png').convert_alpha()
        background_image = pygame.transform.scale(background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        SCREEN.blit(background_image, (0,0))

        if (settings.TUTORIAL == False):
            background_image = pygame.image.load('./assets/tutorial/' + str(settings.TUTORIAL_LEVEL) + '.png').convert_alpha()
            background_image = pygame.transform.scale(background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            SCREEN.blit(background_image, (0,0))
        else:
            if (settings.MENU_STATE == 'main'):
                # print("main menu", settings.GAME_PAUSED, settings.RUNNING)
                title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()
                title_image = pygame.transform.scale(title_image, (math.ceil(title_image.get_width() * settings.X_SCALE), math.ceil(title_image.get_height() * settings.Y_SCALE)))

                SCREEN.blit(title_image, ((settings.SCREEN_WIDTH/2 - title_image.get_width()/2),(settings.SCREEN_HEIGHT/4 - title_image.get_height() * 3 / 4)))
                
                if start_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.PREVIOUS_MENU = "main"
                    settings.MENU_STATE = "lvlsel"
                

                # if scores_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                #     pass

                if main_settings_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    # settings.SFX['click'].play()
                    settings.PREVIOUS_MENU = "main"
                    settings.MENU_STATE = "settings"
                    settings.MENU_CD = pygame.time.get_ticks()
                    continue

                if exit_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.RUNNING = False
                    continue
            
            if (settings.MENU_STATE == 'lvlsel'):

                NAME_INPUT.update(GAME_CLOCK.tick(60) / 300)
                NAME_INPUT.draw_ui(SCREEN)

                title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()
                title_image = pygame.transform.scale(title_image, (math.ceil(title_image.get_width() * settings.X_SCALE), math.ceil(title_image.get_height() * settings.Y_SCALE)))

                SCREEN.blit(title_image, ((settings.SCREEN_WIDTH/2 - title_image.get_width()/2),(settings.SCREEN_HEIGHT/4 - title_image.get_height() * 3 / 4)))

                if level_1_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.GAME_PAUSED = False
                    settings.CURRENT_LEVEL = 1
                    level = Level(settings)
                    continue
                if level_2_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.GAME_PAUSED = False
                    settings.CURRENT_LEVEL = 2
                    level = Level(settings)
                    continue
                if level_3_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.GAME_PAUSED = False
                    settings.CURRENT_LEVEL = 3
                    level = Level(settings)
                    continue
                if level_4_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.GAME_PAUSED = False
                    settings.CURRENT_LEVEL = 4
                    level = Level(settings)
                    continue
                if level_5_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.GAME_PAUSED = False
                    settings.CURRENT_LEVEL = 5
                    level = Level(settings)
                    continue

            if (settings.MENU_STATE == 'pause'):
                # print("pause menu", settings.GAME_PAUSED, settings.RUNNING)
                pygame.mixer.music.pause()
                title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()
                title_image = pygame.transform.scale(title_image, (math.ceil(title_image.get_width() * settings.X_SCALE), math.ceil(title_image.get_height() * settings.Y_SCALE)))

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
                # print("settings menu", settings.GAME_PAUSED, settings.RUNNING)
                pygame.mixer.music.pause()

                title_image = pygame.image.load('./assets/menu/title/title.png').convert_alpha()
                title_image = pygame.transform.scale(title_image, (math.ceil(title_image.get_width() * settings.X_SCALE), math.ceil(title_image.get_height() * settings.Y_SCALE)))

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
                # print("audio menu", settings.GAME_PAUSED, settings.RUNNING)
                background_image = pygame.image.load('./assets/menu/bg/bg.png').convert_alpha()
                background_image = pygame.transform.scale(background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                SCREEN.blit(background_image, (0,0))
                if music_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    if settings.MUSIC_MUTED:
                        settings.MUSIC_MUTED = False
                        music_button.image = settings.MENU_ASSETS["buttons"]["music"]
                        music_button.image = pygame.transform.scale(music_button.image, (math.ceil(music_button.image.get_width() * settings.X_SCALE), math.ceil(music_button.image.get_height() * settings.Y_SCALE)))
                    else:
                        settings.MUSIC_MUTED = True
                        music_button.image = settings.MENU_ASSETS["buttons"]["music_muted"]
                        music_button.image = pygame.transform.scale(music_button.image, (math.ceil(music_button.image.get_width() * settings.X_SCALE), math.ceil(music_button.image.get_height() * settings.Y_SCALE)))
                if sfx_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    if settings.SFX_MUTED:
                        settings.SFX_MUTED = False
                        sfx_button.image = settings.MENU_ASSETS["buttons"]["sfx"]
                        sfx_button.image = pygame.transform.scale(sfx_button.image, (math.ceil(sfx_button.image.get_width() * settings.X_SCALE), math.ceil(sfx_button.image.get_height() * settings.Y_SCALE)))
                    else:
                        settings.SFX_MUTED = True
                        sfx_button.image = settings.MENU_ASSETS["buttons"]["sfx_muted"]                
                        sfx_button.image = pygame.transform.scale(sfx_button.image, (math.ceil(sfx_button.image.get_width() * settings.X_SCALE), math.ceil(sfx_button.image.get_height() * settings.Y_SCALE)))

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

                draw_text(SCREEN, str(int(settings.MUSIC_VOLUME)), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width()* settings.X_SCALE)*1/4 - math.ceil(30 * settings.X_SCALE), (settings.SCREEN_HEIGHT /2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE) + math.ceil(10 * settings.Y_SCALE))) if not settings.MUSIC_MUTED else draw_text(SCREEN, str(0), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width()* settings.X_SCALE)*1/4 - math.ceil(30 * settings.X_SCALE), (settings.SCREEN_HEIGHT /2 - math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE) + math.ceil(10 * settings.Y_SCALE)))
                draw_text(SCREEN, str(int(settings.SFX_VOLUME)), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width()* settings.X_SCALE)*1/4 - math.ceil(30 * settings.X_SCALE), (settings.SCREEN_HEIGHT /2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)/4 + math.ceil(10 * settings.Y_SCALE))) if not settings.SFX_MUTED else draw_text(SCREEN, str(0), settings.MENU_FONT, (255,255,255), settings.SCREEN_WIDTH/2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_width()* settings.X_SCALE)*1/4 - math.ceil(30 * settings.X_SCALE), (settings.SCREEN_HEIGHT /2 + math.ceil(settings.MENU_ASSETS['buttons']['music'].get_height() * settings.Y_SCALE)/4 + math.ceil(10 * settings.Y_SCALE)))
                
                if back_button.draw(SCREEN) and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    settings.MENU_STATE = "settings"
                    settings.MENU_CD = pygame.time.get_ticks()
                    continue

            if (settings.MENU_STATE == "keybinds"):
                # print("keybinds menu", settings.GAME_PAUSED, settings.RUNNING)
            

                if left_button.draw(SCREEN) and not waiting_input and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:

    
                    left_button.image = settings.MENU_ASSETS["buttons"]["buttonpressed"]
                    left_button.image = pygame.transform.scale(left_button.image, (math.ceil(left_button.image.get_width() * settings.X_SCALE), math.ceil(left_button.image.get_height() * settings.Y_SCALE)))
                    waiting_input = True
                    waiting_for = "left"
                draw_text(SCREEN, "LEFT   ", settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2 + math.ceil(10 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE) * 9 / 4) + math.ceil(10 * settings.Y_SCALE))    
                if not waiting_for == "left":
                    draw_text(SCREEN, "LEFT    %s" % (pygame.key.name(settings.KEYBINDS['left']).upper()), settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2 + math.ceil(10 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE) * 9 / 4) + math.ceil(10 * settings.Y_SCALE))
                                
                if right_button.draw(SCREEN) and not waiting_input and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:

                    right_button.image = settings.MENU_ASSETS["buttons"]["buttonpressed"]
                    right_button.image = pygame.transform.scale(right_button.image, (math.ceil(right_button.image.get_width() * settings.X_SCALE), math.ceil(right_button.image.get_height() * settings.Y_SCALE)))
                    waiting_input = True
                    waiting_for = "right"
                draw_text(SCREEN, "RIGHT  ", settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2 + math.ceil(10 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)) + math.ceil(10 * settings.Y_SCALE))    
                if not waiting_for == "right":
                    draw_text(SCREEN, "RIGHT  %s" % (pygame.key.name(settings.KEYBINDS['right']).upper()), settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width()/2 * settings.X_SCALE) + math.ceil(10 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)) + math.ceil(10 * settings.Y_SCALE))
                if jump_button.draw(SCREEN) and not waiting_input and (pygame.time.get_ticks() - settings.MENU_CD) >= 175:
                    jump_button.image = settings.MENU_ASSETS["buttons"]["buttonpressed"]
                    jump_button.image = pygame.transform.scale(jump_button.image, (math.ceil(jump_button.image.get_width() * settings.X_SCALE), math.ceil(jump_button.image.get_height() * settings.Y_SCALE)))
                    waiting_input = True
                    waiting_for = "jump"
                draw_text(SCREEN, "JUMP  ", settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2 + math.ceil(10 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)/4) + math.ceil(10 * settings.Y_SCALE))    
                if not waiting_for == "jump":
                    draw_text(SCREEN, "JUMP   %s" % (pygame.key.name(settings.KEYBINDS['jump']).upper()), settings.MENU_FONT, (255, 255, 255), settings.SCREEN_WIDTH/2 - math.ceil(settings.MENU_ASSETS['buttons']['button'].get_width() * settings.X_SCALE)/2 + math.ceil(10 * settings.X_SCALE), (settings.SCREEN_HEIGHT / 2 + math.ceil(settings.MENU_ASSETS['buttons']['button'].get_height() * settings.Y_SCALE)/4) + math.ceil(10 * settings.Y_SCALE))
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
