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

SCREEN_WIDTH = int(INFO.current_w)
SCREEN_HEIGHT = int(INFO.current_h)

font = pg.font.SysFont(None, 25)


class Game():

    def __init__(self):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.WINDOW_WIDTH = int(self.SCREEN_WIDTH * 0.833333)
        self.WINDOW_HEIGHT = int(self.SCREEN_HEIGHT * 0.833333)
        self.SCREEN = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.tile_num = 0.0042
        self.tile = int(self.WINDOW_WIDTH * self.tile_num)
        self.seednum = 0
        self.value = str(0)
        self.current_gen=[]
        self.paused = False
        self.fullscreen = False
        self.info = pg.display.Info()
        
    def screen_setup(self):
        if self.fullscreen == True:
            # do full screen at current resolution
            self.W_res = self.SCREEN_WIDTH
            self.H_res = self.SCREEN_HEIGHT
            self.SCREEN = pg.display.set_mode((self.W_res, self.H_res), pg.FULLSCREEN)
            pg.mouse.set_visible(False)

        else:
            # set window resolution at ~80% of current screen res
            # example - a 1920x1080 screen will create a ~ 1600x900 game window
            self.W_res = self.WINDOW_WIDTH
            self.H_res = self.WINDOW_HEIGHT
            pg.display.set_mode((self.W_res, self.H_res))
            pg.mouse.set_visible(True)
        
        self.tile = int(self.W_res * self.tile_num)

        self.W = (self.W_res // self.tile) + 1
        self.H = (self.H_res // self.tile) + 2
        print(self.W, self.H)
        if self.tile < 1:
            self.tile = 1

    def intro(self):
        intro = True
        self.SCREEN.fill(COLOR_BLACK)
        text = "Please enter a number or press return for a random one"
        text1 = font.render(text, True, COLOR_WHITE)
        self.SCREEN.blit(text1, (self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT // 4))
        pg.display.flip()
        self.value = str(0)
        self.seednum = randint(5, 9999999999999999) # randint(1,9999999999999999)
        self.next_gen = [[0 for i in range(self.W)] for j in range(self.H)] # initialize to zeroes
        self.random = randint(0, self.W_res - 360) # random location for info box each run
        while intro:
            
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()

                if event.type==pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        exit()
                    if event.key == pg.K_0 or event.key==pg.K_KP0:
                        self.value = self.value + str(0)
                    if event.key == pg.K_1 or event.key==pg.K_KP1:
                        self.value = self.value + str(1)
                    if event.key == pg.K_2 or event.key==pg.K_KP2:
                        self.value = self.value + str(2)
                    if event.key == pg.K_3 or event.key==pg.K_KP3:
                        self.value = self.value + str(3)
                    if event.key == pg.K_4 or event.key==pg.K_KP4:
                        self.value = self.value + str(4)
                    if event.key == pg.K_5 or event.key==pg.K_KP5:
                        self.value = self.value + str(5)
                    if event.key == pg.K_6 or event.key==pg.K_KP6:
                        self.value = self.value + str(6)
                    if event.key == pg.K_7 or event.key==pg.K_KP7:
                        self.value = self.value + str(7)
                    if event.key == pg.K_8 or event.key==pg.K_KP8:
                        self.value = self.value + str(8)
                    if event.key == pg.K_9 or event.key==pg.K_KP9:
                        self.value = self.value + str(9)
                    if event.key==pg.K_KP_ENTER or event.key==pg.K_RETURN:
                        if int(self.value) >= 5:
                            self.seednum = int(self.value)
                            self.value = str(0)
                        elif int(self.value) > 0 and int(self.value) < 5:
                            self.seednum = int(self.value) + 5
                            self.value = str(0)
                        else:
                            self.value = str(0)
                        intro=False

            if int(self.value) is not 0:
                text2 = font.render(self.value[1:], True, COLOR_WHITE)
                self.SCREEN.blit(text2, (self.W_res // 3, self.H_res // 3))
            
            self.current_gen = [[1 if not ((self.seednum % (i + 1)) * (self.seednum % (j + 1))) else 0 for i in range(self.W)] for j in range(self.H)]
            pg.display.flip()
            CLOCK.tick(FPS)

    # see if each cell in grid should be alive or dead

    def check_cell(self, current_gen, x, y):
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

    def debug(self, info, x=10, y=10):
        debug_surf = font.render(str(info), True, COLOR_WHITE)
        debug_rect = debug_surf.get_rect(topleft=(x, y))
        self.SCREEN.blit(debug_surf, debug_rect)

    def update(self):
        if not self.paused:
            self.SCREEN.fill(BACKGROUND)

            [pg.draw.line(self.SCREEN, COLOR_DIMGRAY, (x, 0), (x, self.H_res)) for x in range(0, self.W_res, self.tile)]

            [pg.draw.line(self.SCREEN, COLOR_DIMGRAY, (0, y), (self.W_res, y)) for y in range(0, self.H_res, self.tile)]

            for x in range(0, self.W - 1):
                for y in range(0, self.H - 1):
                    if self.current_gen[y][x]:
                        pg.draw.rect(self.SCREEN, COLOR_GREEN,
                                    (x * self.tile + 2, y * self.tile + 2, self.tile - 2, self.tile - 2))
                    self.next_gen[y][x] = self.check_cell(self.current_gen, x, y)

            self.current_gen = deepcopy(self.next_gen) # update display

            self.debug("Seed: " + str(f'{self.seednum:0>16}')+ " by death-magnet", self.random, self.H_res - 20)
            pg.display.flip()

def main():
    game = Game()
    looping = True
    game.screen_setup()
    game.intro()
    while looping:

        # Get inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game.paused = not game.paused
                if event.key == pg.K_F11:
                    game.fullscreen = not game.fullscreen
                    game.screen_setup()
                    game.intro()
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    game.value = str(0)
                    game.intro()
        if not game.paused:
            game.update()

        CLOCK.tick(FPS)        


if __name__ == "__main__":
    main()
