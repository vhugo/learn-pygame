import pygame
import sys

from pygame.locals import QUIT

pygame.init()

screen = pygame.display.set_mode((800, 600))

red = 255
green = 0
blue = 0
redDirection = -1
greenDirection = 1
blueDirection = 1

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    red += redDirection
    if red == 255 or red == 0:
        redDirection *= -1

    green += greenDirection
    if green == 255 or green == 0:
        greenDirection *= -1

    blue += blueDirection
    if blue == 255 or blue == 0:
        blueDirection *= -1

    screen.fill((red, green, blue))
    pygame.display.flip()
    pygame.time.delay(16)
