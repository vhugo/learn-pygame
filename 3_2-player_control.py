import sys
import pygame

from lib.gameobjects import Background, Player, Enemy, Asteroid
from pygame import QUIT

# Dimensions
w = 800
h = 600

# Setup
framerate = 60
gameObjects = []
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

# background
background = Background("images/nebula.bmp", w, h)
gameObjects.append(background)

# player
player = Player("images/player.bmp", 2, (25, 1, 23, 23))
gameObjects.append(player)

# enemy
enemy = Enemy("images/enemy.bmp", 1, (101, 13, 91, 59))
enemy.position((int(w / 2), int(h / 2)))
gameObjects.append(enemy)

# asteroid
asteroid = Asteroid("images/asteroid.bmp", 1, (6, 3, 80, 67))
asteroid.position((700, 150))
gameObjects.append(asteroid)

running = True
while running:

    # Rendering
    for gameObj in gameObjects:
        gameObj.update()
        screen.blit(gameObj.image, (gameObj.rect.x, gameObj.rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    pygame.display.flip()
    clock.tick(framerate)
