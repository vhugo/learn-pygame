import sys
import pygame

from lib.gameobjects import Background, Player, Enemy, Asteroid, WaveManager, ScoreBoard
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
gameObjects.append(player)


# Score
score = ScoreBoard()

# enemies
enemyWave = WaveManager(3, score)
for i in range(3):
    enemy = Enemy("images/enemy.bmp", 1, (101, 13, 91, 59), (w, h), enemyWave)
    enemy.setTarget(player)
    gameObjects.append(enemy)
    player.collisionGroup.append(enemy)

# asteroids
for i in range(5):
    asteroid = Asteroid("images/asteroid.bmp", 1, (6, 3, 80, 67), (w, h))
    gameObjects.append(asteroid)
    player.collisionGroup.append(asteroid)

delayEvents = 0
delayEventsCaller = None
running = True
while running:

    # Rendering
    screen.blit(background.image, (background.rect.x, background.rect.y))

    # print(delayEvents)
    for idx, gameObj in enumerate(gameObjects):

        if enemyWave.delayEvents > 0:
            enemyWave.delayEvents -= 1
            screen.fill((0, 100, 0))
            break

        if delayEvents == 0:
            gameObj.update()

            if gameObj.delayEvents != 0:
                delayEventsCaller = idx
                delayEvents = gameObj.delayEvents
                break
        else:
            if idx == delayEventsCaller:
                gameObj.image = gameObj.collisionAnimation.getFrame()
                delayEvents -= 1
                gameObj.delayEvents = delayEvents

        if gameObj.collision:
            if delayEvents == 0:
                gameObj.onDeath()
                for everybody in gameObj.collisionGroup:
                    everybody.reset()
            screen.fill((30, 0, 0))

        screen.blit(gameObj.image, (gameObj.rect.x, gameObj.rect.y))

    # Render score
    screen.blit(score.getScore(), (0, 0))
    # Render wave
    wavePanel = score.getWave()
    screen.blit(wavePanel, ((w - wavePanel.get_width()), 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    pygame.display.flip()
    clock.tick(framerate)
