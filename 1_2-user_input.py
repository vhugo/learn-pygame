import pygame
import sys

from pygame.locals import QUIT

pygame.init()

screen = pygame.display.set_mode((800, 600))
rectangle = pygame.Rect(0, 0, 100, 100)
speed = 5

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    # Process player input
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

    # Rendering
    screen.fill((50, 150, 150))
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    pygame.display.flip()
    pygame.time.delay(32)
