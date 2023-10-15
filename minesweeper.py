from random import randint
from copy import deepcopy

import pygame
import numpy as np

pygame.init()

# None = not playing, True = playing, False = lost
game_state = None

# Initialize the images needed for the ui
png_names = ["unopened", "one", "two", "three", "four", "five", "six", "seven", "eight", "mine", "opened_empty"]
images = [pygame.image.load("images/" + name + ".png") for name in png_names]

font_big = pygame.font.SysFont("Helvetica", 100)
font_small = pygame.font.SysFont("Helvetica", 30)

block_size = images[10].get_height()

sreen_width = 32 * block_size
screen_height = 19 * block_size
click_location = (-1, -1)

screen = pygame.display.set_mode((sreen_width, screen_height))

grid = np.ndarray((16, 30))


def detect_win(grid: np.ndarray):
    """Returns True if the game is won, False otherwise"""
    win = not any([any(i) for i in (np.isin(grid, 0))])
    return win


def mine_randomizer(x: int, y: int):
    """Fills the grid with 100 mines randomly."""
    amount = 0

    # The list conatining the no mine coordinates
    no_mine_zone = []

    # Takes into account if the starting point is near an edge
    start_y = -1
    end_y = 2
    if y == 0:
        start_y = 0
    elif y == 15:
        end_y = 1

    # creates a list of the coordinates of the no mine zone.
    for i in range(start_y, end_y):
        for j in range(-1, 2):
            if x == 0 and j == -1:
                continue
            if x == 29 and j == 1:
                continue
            no_mine_zone.append((x + j, y + i))

    # Adds 100 mines randomly to the grid excluding the no mine zone.
    while amount < 99:
        y, x = randint(0, 15), randint(0, 29)
        if grid[(y, x)] == 0 and ((x, y) not in no_mine_zone):
            grid[(y, x)] = 9
            amount += 1


def determine_block_state(x: int, y: int):
    """Determines the state of each block in the grid."""
    amount = 0
    start_y = -1
    end_y = 2
    if y == 0:
        start_y = 0
    elif y == 15:
        end_y = 1

    # Calculates the amount of mines in a 3x3 area around the clicked block.
    for i in range(start_y, end_y):
        for j in range(-1, 2):
            if x == 0 and j == -1:
                continue
            if x == 29 and j == 1:
                continue
            if grid[y + i][x + j] == 9:
                amount += 1

    return amount


def area_cleanup(grid):
    """Automatically opens up the cells that have no mines near them"""
    old_grid = deepcopy(grid)
    changed = False
    for y in range(0, 16):
        for x in range(0, 30):
            # Checks an 3x3 area around every opened empty cells
            if grid[(y, x)] == 10:
                start_y = -1
                end_y = 2
                if y == 0:
                    start_y = 0
                elif y == 15:
                    end_y = 1

                # Determine the amount of mines in a 3x3 area around the clicked block one cell at a time.
                found = []
                next = False
                for i in range(start_y, end_y):
                    if next:
                        break
                    for j in range(-1, 2):
                        if x == 0 and j == -1:
                            continue
                        if x == 29 and j == 1:
                            continue
                        cell_state = determine_block_state(x + j, y + i)
                        found.append(cell_state)

                        # If an unopened bomb cell is found, move to the next area
                        if 9 in found:
                            next = True
                            break

                        # Updates the state of the grid
                        cell = determine_block_state(x + j, y + i)
                        if cell != 0:
                            grid[y + i][x + j] = cell
                        else:
                            grid[y + i][x + j] = 10

                if not np.array_equal(grid, old_grid) and not changed:
                    changed = True

    # If some changes have been made to the grid, run the area cleanup function again
    # to see if further cleanup is in order.
    if changed:
        area_cleanup(grid)


def grid_manipulation(grid: np.ndarray, coordinates: tuple):
    """Handles the grid during gameplay"""
    global game_state

    # Starts the game when a cell is clicked.
    if game_state == None and (32 < coordinates[0] < 992) and (64 < coordinates[1] < 578):
        x = int((coordinates[0] - 32) / 32)
        y = int((coordinates[1] - 64) / 32)
        mine_randomizer(x, y)
        game_state = True

    # If the game is not running, draw a unopened grid.
    elif game_state == None:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                screen.blit(images[int(grid[(y, x)])], (block_size * (1 + x), block_size * (2 + y)))

    # Updates the grid as the game progresses and draws it
    for y in range(len(grid)):
        if not game_state:
            break
        for x in range(len(grid[y])):
            if grid[(y, x)] == 0 or grid[(y, x)] == 9:
                if (block_size * (1 + x)) <= coordinates[0] < (block_size * (1 + x) + block_size) and block_size * (
                        2 + y) <= coordinates[1] < block_size * (2 + y) + block_size:
                    if grid[(y, x)] == 0:
                        amount_of_nearby_mines = determine_block_state(x, y)
                        if amount_of_nearby_mines != 0:
                            grid[(y, x)] = amount_of_nearby_mines
                            screen.blit(images[amount_of_nearby_mines], (block_size * (1 + x), block_size * (2 + y)))
                        else:
                            grid[(y, x)] = 10
                            area_cleanup(grid)
                            screen.blit(images[10], (block_size * (1 + x), block_size * (2 + y)))

                    elif grid[(y, x)] == 9:
                        game_state = False
                        break

                elif grid[(y, x)] == 9:
                    screen.blit(images[0], (block_size * (1 + x), block_size * (2 + y)))
                else:
                    screen.blit(images[0], (block_size * (1 + x), block_size * (2 + y)))

            else:
                screen.blit(images[int(grid[(y, x)])], (block_size * (1 + x), block_size * (2 + y)))

    return game_state


while True:
    new_game = False
    screen.fill((100, 0, 0))
    directions_esc = font_small.render("Quit the game: esc", True, (255, 0, 0))
    screen.blit(directions_esc, (10, 0))

    # Detects game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_location = event.pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_game = True

    if grid_manipulation(grid, click_location) == False:
        # When a mine is opened
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                screen.blit(images[int(grid[(y, x)])], (block_size * (1 + x), block_size * (2 + y)))

        teksti = font_big.render("Hävisit!", True, (255, 0, 0))
        text3 = font_big.render("Uusi peli: space", True, (255, 0, 0))
        screen.blit(teksti, ((sreen_width - teksti.get_width()) / 2, (screen_height - teksti.get_height()) / 2))
        screen.blit(text3,
                    ((sreen_width - text3.get_width()) / 2, (200 + screen_height - text3.get_height()) / 2))
        if new_game:
            grid = np.ndarray((16, 30))
            click_location = (-1, -1)
            game_state = None

    if game_state:
        win = detect_win(grid)
        if win:
            # If all the cells except the mines are opened
            font2 = pygame.font.SysFont("Helvetica", 100)
            text2 = font_big.render("You won!", True, (255, 0, 0))
            text3 = font_big.render("New game: space", True, (255, 0, 0))
            screen.blit(text2,
                        ((sreen_width - text2.get_width()) / 2, (screen_height - text2.get_height()) / 2))
            screen.blit(text3,
                        ((sreen_width - text3.get_width()) / 2, (200 + screen_height - text3.get_height()) / 2))

            if new_game:
                game_state = None

    pygame.display.flip()