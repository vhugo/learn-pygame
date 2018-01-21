#! /usr/bin/env python3

# Plot random pixels on the screen.
# https://lorenzod8n.wordpress.com/2007/12/16/pygame-tutorial-5-pixels/

import sys
import random
import pygame

from pygame import QUIT

# window dimensions
width = 800
height = 600

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
framerate = 240
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    screen.set_at((x, y), (red, green, blue))

    pygame.display.flip()
    clock.tick(framerate)
