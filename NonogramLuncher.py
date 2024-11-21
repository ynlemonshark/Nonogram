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

pygame.display.set_caption("Nonogram")

def main():
    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()
        SURFACE.fill((255, 0, 0))
        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
