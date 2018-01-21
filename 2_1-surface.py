import sys
import pygame

from pygame import QUIT

# Colors
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
bgcolor = white

# Dimensions
screenWidth = 800
screenHeight = 600
screenWidthCenter = int(screenWidth / 2)
screenHeightCenter = int(screenHeight / 2)
screenCenter = (screenWidthCenter, screenHeightCenter)

circleRadius = 100
surfaceWidth = circleRadius * 2
surfaceHeight = circleRadius * 2
surfaceWidthCenter = int(surfaceWidth / 2)
surfaceHeightCenter = int(surfaceHeight / 2)
surfaceCenter = (surfaceWidthCenter, surfaceHeightCenter)

polyPos = [(surfaceWidthCenter, surfaceHeightCenter - circleRadius),
           (surfaceWidthCenter + circleRadius, surfaceHeightCenter),
           (surfaceWidthCenter, surfaceHeightCenter + circleRadius),
           (surfaceWidthCenter - circleRadius, surfaceHeightCenter)]

# Set up
framerate = 5

screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill(bgcolor)

newSurface = pygame.Surface((surfaceWidth, surfaceHeight))
newSurface.set_colorkey(black)

clock = pygame.time.Clock()

# Drawing
pygame.draw.circle(newSurface, blue, surfaceCenter, circleRadius, 3)
pygame.draw.polygon(newSurface, red, polyPos, 3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    screen.blit(newSurface, surfaceCenter)
    screen.blit(newSurface, (0, 0))

    pygame.display.flip()
    clock.tick(framerate)
