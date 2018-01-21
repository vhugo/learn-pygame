import sys
import pygame

from pygame import QUIT


def imageLoader(image, scale, area):
    asset = pygame.image.load(image)
    clipped = pygame.Surface(area[2:])
    clipped.blit(asset, (0, 0), area)
    scaledClipArea = (area[2] * scale, area[3] * scale)
    return pygame.transform.scale(clipped, scaledClipArea)


# Dimensions
w = 800
h = 600

# Setup
framerate = 60
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

# background
background = pygame.image.load("images/nebula.bmp")
backgroundStretched = pygame.transform.scale(background, (w, h))
screen.blit(backgroundStretched, (0, 0))

# player
player = imageLoader("images/hunter.bmp", 2, (25, 1, 23, 23))
playerRotated = pygame.transform.rotate(player, 30)
screen.blit(playerRotated, (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    pygame.display.flip()
    clock.tick(framerate)
