import pygame

file_name = "games/test.txt"

game_name = "test"
game_type = 0
icon = ""
matrix = ""

icon_file = pygame.image.load("icon.png")
if game_type == 0:
    icon_range = 10
elif game_type == 1:
    icon_range = 15
else:
    icon_range = 20
for y in range(icon_range):
    for x in range(icon_range):
        if icon_file.get_at((x, y)) == (255, 0, 0): icon += "a"
        if icon_file.get_at((x, y)) == (255, 127, 0): icon += "b"
        if icon_file.get_at((x, y)) == (255, 255, 0): icon += "c"
        if icon_file.get_at((x, y)) == (0, 255, 0): icon += "d"
        if icon_file.get_at((x, y)) == (0, 127, 0): icon += "e"
        if icon_file.get_at((x, y)) == (0, 255, 255): icon += "f"
        if icon_file.get_at((x, y)) == (0, 127, 255): icon += "g"
        if icon_file.get_at((x, y)) == (0, 0, 255): icon += "h"
        if icon_file.get_at((x, y)) == (191, 0, 255): icon += "i"
        if icon_file.get_at((x, y)) == (255, 127, 255): icon += "j"
        if icon_file.get_at((x, y)) == (255, 0, 255): icon += "k"
        if icon_file.get_at((x, y)) == (0, 0, 0): icon += "l"
        if icon_file.get_at((x, y)) == (255, 255, 255): icon += "m"
        if icon_file.get_at((x, y)) == (191, 191, 191): icon += "n"
        if icon_file.get_at((x, y)) == (127, 127, 127): icon += "o"
        if icon_file.get_at((x, y)) == (63, 63, 63): icon += "p"
        if icon_file.get_at((x, y)) == (127, 63, 31): icon += "q"


matrix_file = pygame.image.load("matrix.png")
if game_type == 0:
    matrix_range = 10
elif game_type == 1:
    matrix_range = 15
else:
    matrix_range = 20
for y in range(matrix_range):
    for x in range(matrix_range):
        if matrix_file.get_at((x, y)) == (0, 0, 0):
            matrix += "1"
        else:
            matrix += "0"

with open(file_name, 'w') as file:
    file.write(game_name + "\n" + str(game_type) + "\n" + icon + "\n" + matrix)
