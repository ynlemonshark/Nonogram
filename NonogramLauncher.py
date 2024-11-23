import pygame
import sys
import glob
from pygame.locals import QUIT, Rect


def setting_import():
    setting_compulsory_data = {"Display_width": 800,
                               "Display_height": 800,
                               "FPS": 40}

    settings = {}
    if glob.glob("setting.txt"):
        settings_file = open("setting.txt", "r")
        while True:
            line = settings_file.readline()
            line.replace("\n", "")
            if line:
                line = line.split(":")
                settings[line[0]] = int(line[1])
            else:
                break

    settings_keys = list(settings.keys())
    setting_compulsory_keys = list(setting_compulsory_data.keys())

    for key in setting_compulsory_keys:
        if key not in settings_keys:
            settings[key] = setting_compulsory_data[key]

    return settings


setting = setting_import()
Display_width = setting["Display_width"]
Display_height = setting["Display_height"]
Surface_width = 800
Surface_height = 800
display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height
FPS = setting["FPS"]
pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()

theme_color = (0, 0, 63)
theme2_color = (127, 127, 191)
theme3_color = (31, 31, 31)

pygame.display.set_caption("Nonogram")

icon = pygame.Surface((100, 100))
icon.fill((255, 255, 255))
pygame.draw.rect(icon, theme_color, (0, 0, 50, 50))
pygame.draw.line(icon, theme_color, (60, 60), (90, 90), 5)
pygame.draw.line(icon, theme_color, (60, 90), (90, 60), 5)
pygame.draw.rect(icon, theme3_color, (0, 0, 100, 100), 5)
pygame.draw.line(icon, theme3_color, (50, 0), (50, 100), 5)
pygame.draw.line(icon, theme3_color, (0, 50), (100, 50), 5)

pygame.display.set_icon(icon)

title_font = pygame.font.SysFont(None, 170, False, False)
title = title_font.render("Nonogram", True, theme_color)
title_rect = title.get_rect()
title_rect.center = (400, 200)

new_game_button_font = pygame.font.SysFont(None, 50, False, False)


select_game_button_rect = pygame.Rect(100, 480, 600, 60)
select_game_button_image = pygame.Surface(select_game_button_rect.size)
select_game_button_text = new_game_button_font.render("Select game", True, theme_color)
select_game_button_text_rect = select_game_button_text.get_rect()
select_game_button_text_rect.center = (select_game_button_rect.width / 2, select_game_button_rect.height / 2)
select_game_button_image.fill((255, 255, 255))
select_game_button_image.blit(select_game_button_text, select_game_button_text_rect.topleft)
pygame.draw.rect(select_game_button_image, theme_color, ((0, 0), select_game_button_rect.size), 3)

select_game_button_image_targeted = pygame.Surface(select_game_button_rect.size)
select_game_button_image_targeted.fill((255, 255, 255))
select_game_button_text_targeted = new_game_button_font.render("Select game", True, theme2_color)
select_game_button_image_targeted.blit(select_game_button_text_targeted, select_game_button_text_rect.topleft)
pygame.draw.rect(select_game_button_image_targeted, theme2_color, ((0, 0), select_game_button_rect.size), 3)

random_game_button_rect = pygame.Rect(100, 580, 600, 60)
random_game_button_image = pygame.Surface(random_game_button_rect.size)
random_game_button_text = new_game_button_font.render("Random game", True, theme_color)
random_game_button_text_rect = random_game_button_text.get_rect()
random_game_button_text_rect.center = (random_game_button_rect.width / 2, random_game_button_rect.height / 2)
random_game_button_image.fill((255, 255, 255))
random_game_button_image.blit(random_game_button_text, random_game_button_text_rect.topleft)
pygame.draw.rect(random_game_button_image, theme_color, ((0, 0), random_game_button_rect.size), 3)

random_game_button_image_targeted = pygame.Surface(random_game_button_rect.size)
random_game_button_image_targeted.fill((255, 255, 255))
random_game_button_text_targeted = new_game_button_font.render("Random game", True, theme2_color)
random_game_button_image_targeted.blit(random_game_button_text_targeted, random_game_button_text_rect.topleft)
pygame.draw.rect(random_game_button_image_targeted, theme2_color, ((0, 0), random_game_button_rect.size), 3)


def main():
    Channel = 0
    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] / display_ratio_x, mouse_pos[1] / display_ratio_y)
        SURFACE.fill((255, 255, 255))
        if Channel == 0:
            if select_game_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(select_game_button_image_targeted, select_game_button_rect.topleft)
            else:
                SURFACE.blit(select_game_button_image, select_game_button_rect.topleft)
            if random_game_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(random_game_button_image_targeted, random_game_button_rect.topleft)
            else:
                SURFACE.blit(random_game_button_image, random_game_button_rect.topleft)
            SURFACE.blit(title, title_rect.topleft)

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
