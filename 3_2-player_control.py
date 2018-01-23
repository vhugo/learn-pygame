import sys
import pygame

from lib.gameobjects import Background, Player, Enemy, Asteroid
from lib.gameobjects import setUniqueRandomPosition
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

# player
player = Player("images/player.bmp", 2, (25, 1, 23, 23), (w, h))
player.spawning((int(w / 2), int(h / 2)))
gameObjects.append(player)

# enemies
for i in range(3):
    enemy = Enemy("images/enemy.bmp", 1, (101, 13, 91, 59), (w, h))
    setUniqueRandomPosition(enemy, w, h, False, gameObjects)
    gameObjects.append(enemy)
    player.collisionGroup.append(enemy)

# asteroids
for i in range(5):
    asteroid = Asteroid("images/asteroid.bmp", 1, (6, 3, 80, 67), (w, h))
    asteroid.velocity = (4, 4)
    setUniqueRandomPosition(asteroid, w, h, True, gameObjects)
    gameObjects.append(asteroid)
    player.collisionGroup.append(asteroid)


running = True
while running:

    # Rendering
    screen.blit(background.image, (background.rect.x, background.rect.y))

    for gameObj in gameObjects:
        gameObj.update()

        if hasattr(gameObj, 'collision'):
            if gameObj.collision:
                screen.fill((255, 0, 0))

        screen.blit(gameObj.image, (gameObj.rect.x, gameObj.rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    pygame.display.flip()
    clock.tick(framerate)
