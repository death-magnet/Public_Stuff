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

import pygame as pg
from random import randint
from copy import deepcopy


pg.init()

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DIMGRAY = (80, 80, 80)
COLOR_GREEN = (34, 125, 50)
BACKGROUND = COLOR_BLACK
# Game Setup
FPS = 10
CLOCK = pg.time.Clock()
INFO = pg.display.Info()
SCREEN_WIDTH = int(INFO.current_w * 0.833333)
SCREEN_HEIGHT = int(INFO.current_h * 0.833333)
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TITLE = "Conway's Game of Life in Python"

TILE = int(SCREEN_HEIGHT * 0.01)
W, H = SCREEN_WIDTH // TILE, SCREEN_HEIGHT // TILE

pg.display.set_caption(TITLE)

# The main function that controls the game


def main():
    looping = True
    paused = False
    # The main game loop

    next_gen = [[0 for i in range(W)] for j in range(H)]
    current_gen = [[randint(0, 1) for i in range(W)] for j in range(H)]

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

    while looping:
        # Get inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = not paused

        if not paused:
            CLOCK.tick(FPS)

            SCREEN.fill(BACKGROUND)

            [pg.draw.line(SCREEN, COLOR_DIMGRAY, (x, 0), (x, SCREEN_HEIGHT))
             for x in range(0, SCREEN_WIDTH, TILE)]
            [pg.draw.line(SCREEN, COLOR_DIMGRAY, (0, y), (SCREEN_WIDTH, y))
             for y in range(0, SCREEN_HEIGHT, TILE)]

            for x in range(1, W - 1):
                for y in range(1, H - 1):
                    if current_gen[y][x]:
                        pg.draw.rect(SCREEN, COLOR_GREEN,
                                     (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
                    next_gen[y][x] = check_cell(current_gen, x, y)
            current_gen = deepcopy(next_gen)

            pg.display.flip()


if __name__ == "__main__":
    main()
