import pygame
import sys
import glob
import os
from pygame.locals import QUIT, Rect
from random import choice


def setting_import():
    setting_compulsory_data = {"Display_width": 800,
                               "Display_height": 800,
                               "FPS": 40,
                               "Sensitivity": 10}

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

if not os.path.exists("setting.txt"):
    with open("setting.txt", "w") as setting_file:
        setting_file.write("Display_width:800\nDisplay_height:800\nFPS:40\nSensitivity:10")
if not os.path.exists("cleared_games.txt"):
    with open("cleared_games.txt", "w") as cleared_games_file:
        cleared_games_file.write("")

with open("cleared_games.txt", "r") as cleared_games_file:
    cleared_games = cleared_games_file.read()
cleared_games = cleared_games.split(",")

if not os.path.exists("games"):
    os.mkdir("games")


pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()

theme_color = (0, 0, 63)
theme2_color = (127, 127, 191)
theme3_color = (63, 63, 63)
theme4_color = (63, 0, 63)
theme5_color = (191, 127, 191)

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


def button_make(color, text, rect, width, font_size):
    e_image = pygame.Surface(rect.size)
    e_image.fill((255, 255, 255))
    e_font = pygame.font.SysFont(None, font_size, False, False)
    e_text = e_font.render(text, True, color)
    e_text_rect = e_text.get_rect()
    e_text_rect.center = (rect.w / 2, rect.h / 2)
    e_image.blit(e_text, e_text_rect.topleft)
    pygame.draw.rect(e_image, color, (0, 0, rect.w, rect.h), width)

    return e_image


select_game_button_rect = pygame.Rect(100, 480, 600, 60)
select_game_button_image = button_make(theme_color, "Select game", select_game_button_rect, 3, 50)

select_game_button_image_targeted = button_make(theme2_color, "Select game", select_game_button_rect, 3, 50)

random_game_button_rect = pygame.Rect(100, 580, 600, 60)
random_game_button_image = button_make(theme_color, "Random game", random_game_button_rect, 3, 50)

random_game_button_image_targeted = button_make(theme2_color, "Random game", random_game_button_rect, 3, 50)

selectable_game_button_font = pygame.font.SysFont(None, 45, False, False)


def selectable_game_button_image_make(color, text):
    e_image = pygame.Surface((600, 50))
    e_image.fill((255, 255, 255))
    e_text = selectable_game_button_font.render(text, True, color)
    e_text_rect = e_text.get_rect()
    e_text_rect.midleft = (25, 25)
    e_image.blit(e_text, e_text_rect.topleft)
    pygame.draw.rect(e_image, color, (0, 0, 600, 50), 2)

    return e_image


selectable_games = []
selectable_game_buttons_rect = []
selectable_game_buttons_image = []
selectable_game_buttons_image_cleared = []
selectable_game_buttons_image_targeted = []
selectable_game_buttons_image_cleared_targeted = []
for repeat, e_game_name in enumerate(os.listdir("games")):
    selectable_games.append(e_game_name)
    selectable_game_buttons_rect.append(Rect(150, repeat * 70 + 30, 600, 50))
    selectable_game_buttons_image.append(selectable_game_button_image_make(theme_color, e_game_name))
    selectable_game_buttons_image_cleared.append(selectable_game_button_image_make(theme4_color, e_game_name))
    selectable_game_buttons_image_targeted.append(selectable_game_button_image_make(theme2_color, e_game_name))
    selectable_game_buttons_image_cleared_targeted.append(selectable_game_button_image_make(theme5_color, e_game_name))

select_game_exit_button_font = pygame.font.SysFont(None, 30, False, False)
select_game_exit_button_rect = Rect(30, 30, 90, 50)
select_game_exit_button_image = button_make(theme_color, "Exit", select_game_exit_button_rect, 2, 30)
select_game_exit_button_image_targeted = button_make(theme2_color, "Exit", select_game_exit_button_rect, 2, 30)

if len(selectable_games):
    select_game_max_drag = max(800, selectable_game_buttons_rect[-1].bottom + 30) - 800
else:
    select_game_max_drag = 0

x_mark = pygame.Surface((100, 100))
x_mark.fill((255, 255, 255))
pygame.draw.line(x_mark, theme_color, (20, 20), (80, 80), 10)
pygame.draw.line(x_mark, theme_color, (20, 80), (80, 20), 10)

x_marks = {"0": pygame.transform.scale(x_mark, (48, 48)),
           "1": pygame.transform.scale(x_mark, (32, 32)),
           "2": pygame.transform.scale(x_mark, (24, 24)),
           }

game_number_font0 = pygame.font.SysFont(None, 40, False, False)
game_number_font1 = pygame.font.SysFont(None, 30, False, False)
game_number_font2 = pygame.font.SysFont(None, 20, False, False)

game_number_images = {"0": [], "1": [], "2": []}
game_number_toplefts = {"0": [], "1": [], "2": []}
for number in range(10):
    number_image = game_number_font0.render(str(number+1), True, theme_color)
    number_rect = number_image.get_rect()
    number_rect.center = (0, 0)
    game_number_images["0"].append(number_image)
    game_number_toplefts["0"].append(number_rect.topleft)
for number in range(15):
    number_image = game_number_font1.render(str(number+1), True, theme_color)
    number_rect = number_image.get_rect()
    number_rect.center = (0, 0)
    game_number_images["1"].append(number_image)
    game_number_toplefts["1"].append(number_rect.topleft)
for number in range(20):
    number_image = game_number_font2.render(str(number+1), True, theme_color)
    number_rect = number_image.get_rect()
    number_rect.center = (0, 0)
    game_number_images["2"].append(number_image)
    game_number_toplefts["2"].append(number_rect.topleft)

life_image = pygame.Surface((30, 30))
life_image.fill(theme2_color)
pygame.draw.rect(life_image, theme_color, (0, 0, 30, 30), 3)

exit_button_rect = Rect(650, 630, 100, 40)
exit_button_image = button_make(theme_color, "Exit", exit_button_rect, 2, 40)
exit_button_image_targeted = button_make(theme2_color, "Exit", exit_button_rect, 2, 40)

really_exit_question = button_make(theme_color, "Really Exit?", Rect(100, 100, 600, 100), 3, 70)

really_exit_yes_rect = Rect(100, 250, 250, 100)
really_exit_yes_image = button_make(theme_color, "Yes", really_exit_yes_rect, 3, 40)
really_exit_yes_image_targeted = button_make(theme2_color, "Yes", really_exit_yes_rect, 3, 40)
really_exit_no_rect = Rect(450, 250, 250, 100)
really_exit_no_image = button_make(theme_color, "No", really_exit_no_rect, 3, 40)
really_exit_no_image_targeted = button_make(theme2_color, "No", really_exit_no_rect, 3, 40)

veil = pygame.Surface((800, 800))

fail_message = button_make(theme_color, "Game over", Rect(100, 100, 600, 100), 3, 70)
clear_message = button_make(theme_color, "Game clear", Rect(100, 100, 600, 100), 3, 70)


retry_button_rect = Rect(100, 300, 250, 100)
retry_button_image = button_make(theme_color, "Retry", retry_button_rect, 3, 40)
retry_button_image_targeted = button_make(theme2_color, "Retry", retry_button_rect, 3, 40)
gotolobby_button_rect = Rect(450, 300, 250, 100)
gotolobby_button_image = button_make(theme_color, "Go to lobby", retry_button_rect, 3, 40)
gotolobby_button_image_targeted = button_make(theme2_color, "Go to lobby", retry_button_rect, 3, 40)

gotolobby2_button_rect = Rect(100, 650, 600, 70)
gotolobby2_button_image = button_make(theme_color, "Go to lobby", gotolobby2_button_rect, 3, 50)
gotolobby2_button_image_targeted = button_make(theme2_color, "Go to lobby", gotolobby2_button_rect, 3, 50)

all_random_button_rect = Rect(100, 100, 600, 100)
all_random_button_image = button_make(theme_color, "Random game", all_random_button_rect, 3, 50)
all_random_button_image_targeted = button_make(theme2_color, "Random game", all_random_button_rect, 3, 50)
uncleared_random_button_rect = Rect(100, 300, 600, 100)
uncleared_random_button_image = button_make(theme_color, "Uncleared random game", uncleared_random_button_rect, 3, 50)
uncleared_random_button_image_targeted = button_make(theme2_color, "Uncleared random game", uncleared_random_button_rect, 3, 50)

exit2_button_rect = Rect(100, 600, 600, 100)
exit2_button_image = button_make(theme_color, "Exit", exit2_button_rect, 3, 50)
exit2_button_image_targeted = button_make(theme2_color, "Exit", exit2_button_rect, 3, 50)


class Game:
    def __init__(self, file_name, name, g_type, f_icon, matrix):
        self.file_name = file_name
        self.life = 3
        self.veil_time = 0

        self.name = name
        self.g_type = g_type
        self.f_icon = f_icon
        self.matrix = matrix

        self.opened = "0"
        if g_type == "0":
            self.opened *= 100
        elif g_type == "1":
            self.opened *= 225
        else:
            self.opened *= 400

        if g_type == "0":
            size = 10
        elif g_type == "1":
            size = 15
        else:
            size = 20

        self.x_numbers = []
        self.y_numbers = []
        for y in range(size):
            stacks = []
            stack = 0
            for x in range(size):
                if self.return_matrix_pos(x, y) == "1":
                    stack += 1
                else:
                    if stack:
                        stacks.append(stack)
                        stack = 0
            if stack:
                stacks.append(stack)
            self.x_numbers.append(stacks)
        for x in range(size):
            stacks = []
            stack = 0
            for y in range(size):
                if self.return_matrix_pos(x, y) == "1":
                    stack += 1
                else:
                    if stack:
                        stacks.append(stack)
                        stack = 0
            if stack:
                stacks.append(stack)
            self.y_numbers.append(stacks)

        self.s_icon = pygame.Surface((size, size))
        for x in range(size):
            for y in range(size):
                if self.f_icon[x+y*size] == "a": self.s_icon.set_at((x, y), (255, 0, 0))
                if self.f_icon[x+y*size] == "b": self.s_icon.set_at((x, y), (255, 127, 0))
                if self.f_icon[x+y*size] == "c": self.s_icon.set_at((x, y), (255, 255, 0))
                if self.f_icon[x+y*size] == "d": self.s_icon.set_at((x, y), (0, 255, 0))
                if self.f_icon[x+y*size] == "e": self.s_icon.set_at((x, y), (0, 127, 0))
                if self.f_icon[x+y*size] == "f": self.s_icon.set_at((x, y), (0, 255, 255))
                if self.f_icon[x+y*size] == "g": self.s_icon.set_at((x, y), (0, 127, 255))
                if self.f_icon[x+y*size] == "h": self.s_icon.set_at((x, y), (0, 0, 255))
                if self.f_icon[x+y*size] == "i": self.s_icon.set_at((x, y), (191, 0, 255))
                if self.f_icon[x+y*size] == "j": self.s_icon.set_at((x, y), (255, 127, 255))
                if self.f_icon[x+y*size] == "k": self.s_icon.set_at((x, y), (255, 0, 255))
                if self.f_icon[x+y*size] == "l": self.s_icon.set_at((x, y), (0, 0, 0))
                if self.f_icon[x+y*size] == "m": self.s_icon.set_at((x, y), (255, 255, 255))
                if self.f_icon[x+y*size] == "n": self.s_icon.set_at((x, y), (191, 191, 191))
                if self.f_icon[x+y*size] == "o": self.s_icon.set_at((x, y), (127, 127, 127))
                if self.f_icon[x+y*size] == "p": self.s_icon.set_at((x, y), (63, 63, 63))
                if self.f_icon[x+y*size] == "q": self.s_icon.set_at((x, y), (127, 63, 31))

        self.s_icon = pygame.transform.scale(self.s_icon, (360, 360))
        self.s_name = button_make(theme_color, self.name, Rect(0, 0, 380, 50), 5, 40)

    def matrix_pos(self, x, y):
        if self.g_type == "0":
            if self.opened[x+y*10] == "1":
                return self.matrix[x+y*10]
            else:
                return "None"
        if self.g_type == "1":
            if self.opened[x+y*15] == "1":
                return self.matrix[x+y*15]
            else:
                return "None"
        else:
            if self.opened[x+y*20] == "1":
                return self.matrix[x+y*20]
            else:
                return "None"

    def return_matrix_pos(self, x, y):
        if self.g_type == "0":
            return self.matrix[x+y*10]
        if self.g_type == "1":
            return self.matrix[x+y*15]
        else:
            return self.matrix[x+y*20]

    def draw_numbers(self):
        if self.g_type == "0":
            size = 48
            constant = 30
        elif self.g_type == "1":
            size = 32
            constant = 20
        else:
            size = 24
            constant = 10
        for index in range(len(self.x_numbers)):
            for index2 in range(len(self.x_numbers[index])):
                SURFACE.blit(game_number_images[self.g_type][self.x_numbers[index][index2] - 1],
                             (game_number_toplefts[self.g_type][self.x_numbers[index][index2] - 1][0] + 500 + index2 * 20,
                              game_number_toplefts[self.g_type][self.x_numbers[index][index2] - 1][1] + constant + index * size))
        for index in range(len(self.y_numbers)):
            for index2 in range(len(self.y_numbers[index])):
                SURFACE.blit(game_number_images[self.g_type][self.y_numbers[index][index2] - 1],
                             (game_number_toplefts[self.g_type][self.y_numbers[index][index2] - 1][0] + constant + index * size,
                              game_number_toplefts[self.g_type][self.y_numbers[index][index2] - 1][1] + 500 + index2 * 20))

    def open(self, x, y):
        if self.g_type == "0":
            self.opened = self.opened[:x+y*10] + "1" + self.opened[x+y*10+1:]
        elif self.g_type == "1":
            self.opened = self.opened[:x+y*15] + "1" + self.opened[x+y*15+1:]
        else:
            self.opened = self.opened[:x+y*20] + "1" + self.opened[x+y*20+1:]

    def return_opened(self, x, y):
        if self.g_type == "0":
            return self.opened[x+y*10]
        if self.g_type == "1":
            return self.opened[x+y*15]
        else:
            return self.opened[x+y*20]


def import_game(file_name):
    data = []
    with open("games/"+file_name, "r") as file:
        data.append(file.readline().replace("\n", ""))
        data.append(file.readline().replace("\n", ""))
        data.append(file.readline().replace("\n", ""))
        data.append(file.readline().replace("\n", ""))
    return Game(file_name, data[0], data[1], data[2], data[3])


def main():
    Channel = 0
    game_select_dragging = 0

    GAME = 0

    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                with open("cleared_games.txt", "w") as cleared_games_file_w:
                    to_append = ""
                    for file_name in cleared_games:
                        if file_name:
                            to_append += file_name
                            to_append += ","
                    if to_append:
                        to_append = to_append[:-1]
                    cleared_games_file_w.write(to_append)

                pygame.quit()
                sys.exit()
            if pygame_event.type == pygame.MOUSEBUTTONUP:
                event_pos = (pygame_event.pos[0] / display_ratio_x, pygame_event.pos[1] / display_ratio_y)
                if Channel == 0:
                    if select_game_button_rect.collidepoint(event_pos):
                        Channel = 1
                    if random_game_button_rect.collidepoint(event_pos):
                        Channel = 2
                elif Channel == 1:
                    if select_game_exit_button_rect.collidepoint(event_pos):
                        Channel = 0

                    for index in range(len(selectable_game_buttons_rect)):
                        if selectable_game_buttons_rect[index].collidepoint((event_pos[0], event_pos[1] + game_select_dragging)):
                            Channel = 6
                            GAME = import_game(selectable_games[index])

                elif Channel == 2:
                    if all_random_button_rect.collidepoint(event_pos):
                        if len(selectable_games):
                            Channel = 3
                            GAME = import_game(choice(selectable_games))
                    if uncleared_random_button_rect.collidepoint(event_pos):
                        if len(list(set(selectable_games).difference(cleared_games))):
                            Channel = 3
                            GAME = import_game(choice(list(set(selectable_games).difference(cleared_games))))
                    if exit2_button_rect.collidepoint(event_pos):
                        Channel = 0

                elif Channel == 3:
                    if exit_button_rect.collidepoint(event_pos):
                        Channel = 4

            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                event_pos = (pygame_event.pos[0] / display_ratio_x, pygame_event.pos[1] / display_ratio_y)
                if Channel == 4:
                    if really_exit_yes_rect.collidepoint(event_pos):
                        Channel = 0
                    if really_exit_no_rect.collidepoint(event_pos):
                        Channel = 3
                elif Channel == 5:
                    if retry_button_rect.collidepoint(event_pos):
                        Channel = 3
                        GAME = import_game(GAME.file_name)
                    if gotolobby_button_rect.collidepoint(event_pos):
                        Channel = 0
                elif Channel == 6:
                    if gotolobby2_button_rect.collidepoint(event_pos):
                        Channel = 0

            if pygame_event.type == pygame.MOUSEWHEEL:
                if Channel == 1:
                    game_select_dragging -= pygame_event.y * setting["Sensitivity"]
                    game_select_dragging = min(max(game_select_dragging, 0), select_game_max_drag)

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
        if Channel == 1:
            if select_game_exit_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(select_game_exit_button_image_targeted, select_game_exit_button_rect.topleft)
            else:
                SURFACE.blit(select_game_exit_button_image, select_game_exit_button_rect.topleft)
            for index in range(len(selectable_game_buttons_rect)):
                if selectable_games[index] in cleared_games:
                    if selectable_game_buttons_rect[index].collidepoint((mouse_pos[0], mouse_pos[1] + game_select_dragging)):
                        SURFACE.blit(selectable_game_buttons_image_cleared_targeted[index],
                                     (selectable_game_buttons_rect[index].left,
                                      selectable_game_buttons_rect[index].top - game_select_dragging))
                    else:
                        SURFACE.blit(selectable_game_buttons_image_cleared[index],
                                     (selectable_game_buttons_rect[index].left,
                                      selectable_game_buttons_rect[index].top - game_select_dragging))
                else:
                    if selectable_game_buttons_rect[index].collidepoint((mouse_pos[0], mouse_pos[1] + game_select_dragging)):
                        SURFACE.blit(selectable_game_buttons_image_targeted[index],
                                     (selectable_game_buttons_rect[index].left,
                                      selectable_game_buttons_rect[index].top - game_select_dragging))
                    else:
                        SURFACE.blit(selectable_game_buttons_image[index],
                                     (selectable_game_buttons_rect[index].left,
                                      selectable_game_buttons_rect[index].top - game_select_dragging))

        elif Channel == 2:
            if all_random_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(all_random_button_image_targeted, all_random_button_rect.topleft)
            else:
                SURFACE.blit(all_random_button_image, all_random_button_rect.topleft)
            if uncleared_random_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(uncleared_random_button_image_targeted, uncleared_random_button_rect.topleft)
            else:
                SURFACE.blit(uncleared_random_button_image, uncleared_random_button_rect.topleft)
            if exit2_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(exit2_button_image_targeted, exit2_button_rect.topleft)
            else:
                SURFACE.blit(exit2_button_image, exit2_button_rect.topleft)

        elif Channel == 3:
            if GAME.g_type == "0":
                g_size = 48
                g_range = 10
            elif GAME.g_type == "1":
                g_size = 32
                g_range = 15
            else:
                g_size = 24
                g_range = 20

            if pygame.mouse.get_pressed()[0]:
                if 0 < mouse_pos[0] / g_size < g_range and 0 < mouse_pos[1] / g_size < g_range:
                    if GAME.return_opened(int(mouse_pos[0] / g_size), int(mouse_pos[1] / g_size)) == "0":
                        GAME.open(int(mouse_pos[0] / g_size), int(mouse_pos[1] / g_size))
                        if GAME.return_matrix_pos(int(mouse_pos[0] / g_size), int(mouse_pos[1] / g_size)) == "0":
                            GAME.life -= 1
                            GAME.veil_time = 500
                            veil.fill((255, 0, 0))
            if pygame.mouse.get_pressed()[2]:
                if 0 < mouse_pos[0] / g_size < g_range and mouse_pos[1] / g_size < g_range:
                    if GAME.return_opened(int(mouse_pos[0] / g_size), int(mouse_pos[1] / g_size)) == "0":
                        GAME.open(int(mouse_pos[0] / g_size), int(mouse_pos[1] / g_size))
                        if GAME.return_matrix_pos(int(mouse_pos[0] / g_size), int(mouse_pos[1] / g_size)) == "1":
                            GAME.life -= 1
                            GAME.veil_time = 500
                            veil.fill((255, 0, 0))

            if not GAME.opened.count("0"):
                Channel = 6
                cleared_games.append(GAME.file_name)
            if not GAME.life:
                Channel = 5

            if GAME.g_type == "0":
                for x in range(10):
                    for y in range(10):
                        if GAME.matrix_pos(x, y) == "0":
                            SURFACE.blit(x_marks[GAME.g_type], (x * 48, y * 48))
                        elif GAME.matrix_pos(x, y) == "1":
                            pygame.draw.rect(SURFACE, theme_color, (x * 48, y * 48, 48, 48))

                for x in range(11):
                    pygame.draw.line(SURFACE, theme3_color, (x * 48, 0), (x * 48, 600), 2)
                for y in range(11):
                    pygame.draw.line(SURFACE, theme3_color, (0, y * 48), (800, y * 48), 2)
                pygame.draw.line(SURFACE, theme3_color, (0, 600), (800, 600), 2)

            elif GAME.g_type == "1":
                for x in range(15):
                    for y in range(15):
                        if GAME.matrix_pos(x, y) == "0":
                            SURFACE.blit(x_marks[GAME.g_type], (x * 32, y * 32))
                        elif GAME.matrix_pos(x, y) == "1":
                            pygame.draw.rect(SURFACE, theme_color, (x * 32, y * 32, 32, 32))

                for x in range(16):
                    pygame.draw.line(SURFACE, theme3_color, (x * 32, 0), (x * 32, 600), 2)
                for y in range(16):
                    pygame.draw.line(SURFACE, theme3_color, (0, y * 32), (800, y * 32), 2)
                pygame.draw.line(SURFACE, theme3_color, (0, 600), (800, 600), 2)
            else:
                for x in range(20):
                    for y in range(20):
                        if GAME.matrix_pos(x, y) == "0":
                            SURFACE.blit(x_marks[GAME.g_type], (x * 24, y * 24))
                        elif GAME.matrix_pos(x, y) == "1":
                            pygame.draw.rect(SURFACE, theme_color, (x * 24, y * 24, 24, 24))

                for x in range(21):
                    pygame.draw.line(SURFACE, theme3_color, (x * 24, 0), (x * 24, 600), 2)
                for y in range(21):
                    pygame.draw.line(SURFACE, theme3_color, (0, y * 24), (800, y * 24), 2)
                pygame.draw.line(SURFACE, theme3_color, (0, 600), (800, 600), 2)
            GAME.draw_numbers()

            for repeat in range(GAME.life):
                SURFACE.blit(life_image, (80 + repeat * 40, 630))

            if exit_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(exit_button_image_targeted, exit_button_rect.topleft)
            else:
                SURFACE.blit(exit_button_image, exit_button_rect.topleft)

            if GAME.veil_time:
                veil.set_alpha(int(GAME.veil_time / 500 * 255))
                GAME.veil_time -= 1000 / FPS
                GAME.veil_time = max(GAME.veil_time, 0)
                SURFACE.blit(veil, (0, 0))

        elif Channel == 4:
            SURFACE.blit(really_exit_question, (100, 100))
            if really_exit_yes_rect.collidepoint(mouse_pos):
                SURFACE.blit(really_exit_yes_image_targeted, really_exit_yes_rect.topleft)
            else:
                SURFACE.blit(really_exit_yes_image, really_exit_yes_rect.topleft)
            if really_exit_no_rect.collidepoint(mouse_pos):
                SURFACE.blit(really_exit_no_image_targeted, really_exit_no_rect.topleft)
            else:
                SURFACE.blit(really_exit_no_image, really_exit_no_rect.topleft)
        elif Channel == 5:
            SURFACE.blit(fail_message, (100, 100))
            if retry_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(retry_button_image_targeted, retry_button_rect.topleft)
            else:
                SURFACE.blit(retry_button_image, retry_button_rect.topleft)
            if gotolobby_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(gotolobby_button_image_targeted, gotolobby_button_rect.topleft)
            else:
                SURFACE.blit(gotolobby_button_image, gotolobby_button_rect.topleft)

        elif Channel == 6:
            SURFACE.blit(clear_message, (100, 50))
            SURFACE.blit(GAME.s_icon, (220, 200))
            pygame.draw.rect(SURFACE, theme_color, (210, 190, 380, 380), 5)
            SURFACE.blit(GAME.s_name, (210, 565))
            if gotolobby2_button_rect.collidepoint(mouse_pos):
                SURFACE.blit(gotolobby2_button_image_targeted, gotolobby2_button_rect.topleft)
            else:
                SURFACE.blit(gotolobby2_button_image, gotolobby2_button_rect.topleft)

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
