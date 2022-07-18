#!/usr/bin/env python3

# by death-magnet
# MIT License

# Copyright(c) 2022 death-magnet

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# Credit is given when using all or part of this source code. Credit
# to be given to death-magnet

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Based in part on a Game of Life example by https://github.com/StanislavPetrovV/

import pygame as pg
from random import randint
from copy import deepcopy
import itertools, sys
from numba import njit
spinner = itertools.cycle([ '/', '-', '\\', '|'])



pg.init()

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DIMGRAY = (20, 20, 20)
COLOR_GREEN = (34, 125, 50)
BACKGROUND = COLOR_BLACK
# Game Setup
FPS = 10
CLOCK = pg.time.Clock()

# window title
TITLE = "Conway's Game of Life in Python"

pg.display.set_caption(TITLE)

# initialize screen to default values
INFO = pg.display.Info()

SCREEN_WIDTH = int(INFO.current_w * 0.833333)
SCREEN_HEIGHT = int(INFO.current_h * 0.833333)

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TILE = int(SCREEN_HEIGHT * 0.01)
W, H = SCREEN_WIDTH // TILE, SCREEN_HEIGHT // TILE


seednum = 0
value = str(0)
paused = False
# The main function that controls the game
def main():
    global current_gen, seednum, value, paused
    fullscreen = False

    looping = True
    paused = False
    print("simulating")
    def screen_setup():
        # get current screen resolution
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, TILE, W, H, INFO

        INFO = pg.display.Info()

        

        # set screen dimensions
        if fullscreen == True:
            # full screen at current resolution
            SCREEN_WIDTH = int(INFO.current_w)
            SCREEN_HEIGHT = int(INFO.current_h)
            SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
            pg.mouse.set_visible(False)
        else:
            # set window resolution to be a bit smaller than full screen
            # This should make it about 1600x900 on a 1920x1080 screen for example
            SCREEN_WIDTH = int(INFO.current_w * 0.833333)
            SCREEN_HEIGHT = int(INFO.current_h * 0.833333)
            SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pg.mouse.set_visible(True)


        # set up the game board
        TILE = int(SCREEN_HEIGHT * 0.008)
        if TILE < 1:
            TILE = 1

        SCREEN_WIDTH = SCREEN_WIDTH * 1.2
        SCREEN_HEIGHT = SCREEN_HEIGHT * 1.2

        SCREEN_WIDTH = int(SCREEN_WIDTH)
        SCREEN_HEIGHT = int(SCREEN_HEIGHT)

        W, H = SCREEN_WIDTH // TILE, SCREEN_HEIGHT // TILE

        [pg.draw.line(SCREEN, COLOR_DIMGRAY, (x, 0), (x, SCREEN_HEIGHT))
             for x in range(0, SCREEN_WIDTH, TILE)]
        [pg.draw.line(SCREEN, COLOR_DIMGRAY, (0, y), (SCREEN_WIDTH, y))
            for y in range(0, SCREEN_HEIGHT, TILE)]


    screen_setup()
    def game_intro():
        global seednum
        global value
        intro=True
        SCREEN.fill(COLOR_BLACK)
        text = "Please enter a number or press return for a random one"
        font = pg.font.SysFont(None, 25)
        text1 = font.render(text, True, COLOR_WHITE)
        SCREEN.blit(text1, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4))
        pg.display.flip()
        seednum = randint(5, 9999999999999999) # randint(1,9999999999999999)
        print(seednum)
        while intro:
            
            
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()

                if event.type==pg.KEYDOWN:
                    if event.key == pg.K_0 or event.key==pg.K_KP0:
                        value = value + str(0)
                    if event.key == pg.K_1 or event.key==pg.K_KP1:
                        value = value + str(1)
                    if event.key == pg.K_2 or event.key==pg.K_KP2:
                        value = value + str(2)
                    if event.key == pg.K_3 or event.key==pg.K_KP3:
                        value = value + str(3)
                    if event.key == pg.K_4 or event.key==pg.K_KP4:
                        value = value + str(4)
                    if event.key == pg.K_5 or event.key==pg.K_KP5:
                        value = value + str(5)
                    if event.key == pg.K_6 or event.key==pg.K_KP6:
                        value = value + str(6)
                    if event.key == pg.K_7 or event.key==pg.K_KP7:
                        value = value + str(7)
                    if event.key == pg.K_8 or event.key==pg.K_KP8:
                        value = value + str(8)
                    if event.key == pg.K_9 or event.key==pg.K_KP9:
                        value = value + str(9)
                    if event.key==pg.K_KP_ENTER or event.key==pg.K_RETURN:
                        if int(value) >= 5:
                            seednum = int(value)
                            value = str(0)
                            print(seednum)
                        elif int(value) > 0 and int(value) < 5:
                            seednum = int(value) + 5
                            value = str(0)
                        else:
                            value = str(0)
                        intro=False
            # print(value)
            if int(value) is not 0:
                text2 = font.render(value[1:], True, COLOR_WHITE)
                SCREEN.blit(text2, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
            
            pg.display.flip()
            CLOCK.tick(FPS)
    game_intro()
    
    
    # seed method below

    next_gen = [[0 for i in range(W)] for j in range(H)] # initialize to zeroes
    current_gen = [[1 if not ((seednum % (i + 1)) * (seednum % (j + 1))) else 0 for i in range(W)] for j in range(H)]

    # see if each cell in grid should be alive or dead

    def check_cell(current_gen, x, y):
        count = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if current_gen[j][i]:
                    count = count + 1

        if current_gen[y][x]:
            count = count - 1

            if count == 2 or count == 3:
                return 1
            return 0
        else:
            if count == 3:
                return 1
            return 0

    
    # The main game loop
    while looping:
        
        stats = "Seed number: " + str(seednum)
        newtitle = TITLE + " - " + stats + " - FPS: " + str(int(CLOCK.get_fps()))
        pg.display.set_caption(newtitle)
        # Get inputs
        def check_events():
            global paused, next_gen, current_gen, seednum, W, H
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        paused = not paused
                    if event.key == pg.K_F11:
                        # do full screen stuff
                        paused = True
                        fullscreen = not fullscreen
                        screen_setup()
                        paused = False
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        exit()
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        value = str(0)
                        game_intro()
                        # new seed
                        next_gen = [[0 for i in range(W)] for j in range(H)]
                        current_gen = [[1 if not ((seednum % (i + 1)) * (seednum % (j + 1))) else 0 for i in range(W)] for j in range(H)]
        check_events()
        if not paused:

            def draw_game():
                global current_gen
                SCREEN.fill(BACKGROUND)

                # draw grid of lines
                [pg.draw.line(SCREEN, COLOR_DIMGRAY, (x, 0), (x, SCREEN_HEIGHT))
                for x in range(0, SCREEN_WIDTH, TILE)]
                [pg.draw.line(SCREEN, COLOR_DIMGRAY, (0, y), (SCREEN_WIDTH, y))
                for y in range(0, SCREEN_HEIGHT, TILE)]

                # draw individual cells according to the rules
                for x in range(1, W - 1):
                    for y in range(1, H - 1):
                        if current_gen[y][x]:
                            pg.draw.rect(SCREEN, COLOR_GREEN,
                                        (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
                        next_gen[y][x] = check_cell(current_gen, x, y)
                current_gen = deepcopy(next_gen)

                # update display
                pg.display.flip()
                CLOCK.tick(FPS)
            draw_game()
            sys.stdout.write(next(spinner))   # write the next character
            sys.stdout.flush()                # flush stdout buffer (actual character display)
            sys.stdout.write('\b')            # erase the last written char
            check_events()

        else:
            check_events()
if __name__ == "__main__":
    main()
