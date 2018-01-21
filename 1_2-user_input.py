import pygame
import sys
import random

from pygame.locals import QUIT

pygame.init()

screenbg = (50, 150, 150)
screen = pygame.display.set_mode((800, 600))
screen.fill(screenbg)

rectangle = pygame.Rect(0, 0, 100, 100)
lastRect = (0, 0, 0, 0)

clock = pygame.time.Clock()
totalTime = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    # Process player input
    # timeChange = pygame.time.get_ticks() - totalTime
    # speedCorrection = timeChange / 16
    # speed = speedCorrection
    speed = 3

    up = pygame.key.get_pressed()[pygame.K_UP]
    down = pygame.key.get_pressed()[pygame.K_DOWN]
    left = pygame.key.get_pressed()[pygame.K_LEFT]
    right = pygame.key.get_pressed()[pygame.K_RIGHT]

    # Update game state logic
    max_width = screen.get_width() - rectangle.width
    max_height = screen.get_height() - rectangle.height

    if up and rectangle.y > 0:
        rectangle.y += speed * -1
    if down and rectangle.y < max_height:
        rectangle.y += speed * 1
    if left and rectangle.x > 0:
        rectangle.x += speed * -1
    if right and rectangle.x < max_width:
        rectangle.x += speed * 1

    # Simulate game lag
    randDelay = random.randrange(0, 500)
    pygame.time.delay(randDelay)

    # Rendering
    pygame.draw.rect(screen, screenbg, lastRect)
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    pygame.display.flip()
    lastRect = pygame.Rect(
        rectangle.x,
        rectangle.y,
        rectangle.width,
        rectangle.height)

    clock.tick(60)
