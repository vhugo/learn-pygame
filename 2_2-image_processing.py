import sys
import pygame

from pygame import QUIT

# Dimensions
lena = pygame.image.load("images/lena.bmp")
w = lena.get_width()
h = lena.get_height()

# Setup
screen = pygame.display.set_mode((w, h))

lenaPixelArray = pygame.PixelArray(lena)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    # Rendering
    # screen.blit(pygame.transform.laplacian(lena), (0, 0))
    # screen.fill(pygame.transform.average_color(lena))

    for x in range(0, w):
        for y in range(0, h):
            pixel = lenaPixelArray[x, y]
            if pixel > 0x444444:
                lenaPixelArray[x, y] = 0xFFFFFF
    screen.blit(lenaPixelArray.make_surface(), (0, 0))

    pygame.display.flip()
