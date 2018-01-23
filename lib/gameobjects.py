import pygame
import random

from lib.imageloader import imageLoader


def setUniqueRandomPosition(gameAsset, w, h, gameAssetList):
    xy = (
        random.randrange(0, w - gameAsset.image.get_width()),
        random.randrange(0, h - gameAsset.image.get_height()))
    gameAsset.position(xy)

    for asset in gameAssetList:
        if gameAsset.rect.colliderect(asset.rect):
            return setUniqueRandomPosition(gameAsset, w, h, gameAssetList)


class Background(pygame.sprite.Sprite):

    def __init__(self, image, width, height):
        self.OriginalAssetImage = pygame.image.load(image)
        self.image = pygame.transform.scale(
            self.OriginalAssetImage, (width, height))
        self.rect = self.image.get_rect()


class GameAsset(pygame.sprite.Sprite):

    acceleration = (0, 0)
    angle = 0
    damping = 0
    thrust = 0
    velocity = (0, 0)
    velocityMax = 8

    def __init__(self, image, scale, area):
        self.image = self.asset = imageLoader(image, scale, area)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()

        self.collision = False
        self.collisionGroup = []

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.asset, angle)

    def position(self, dest):
        self.rect.x = dest[0]
        self.rect.y = dest[1]

    def update(self):
        # Collision detection
        self.checkForCollisions()

        # Update the physics
        self.updatePhysics()

    def checkForCollisions(self):
        for asset in self.collisionGroup:
            self.collision = self.rect.colliderect(asset.rect)
            if self.collision:
                break

    def updatePhysics(self):
        # Apply acceleration
        self.applyAcceleration()

        # Apply damping
        self.applyDamping()

        # Apply velocity cap (max velocity)
        self.applyVelocityCap()

        # Set player location
        self.setAssetLocation()

    def applyAcceleration(self):
        vx = self.velocity[0] + self.acceleration[0]
        vy = self.velocity[1] + self.acceleration[1]
        self.velocity = (vx, vy)

    def applyDamping(self):
        vx = self.velocity[0]
        vy = self.velocity[1]

        # Horizontal
        if vx < self.damping * -1:
            vx += self.damping
        elif vx > self.damping:
            vx -= self.damping
        else:
            vx = 0

        # Vertical
        if vy < self.damping * -1:
            vy += self.damping
        elif vy > self.damping:
            vy -= self.damping
        else:
            vy = 0

        self.velocity = (vx, vy)

    def applyVelocityCap(self):
        vx = self.velocity[0]
        vy = self.velocity[1]

        if vx > self.velocityMax:
            vx = self.velocityMax

        if vx < self.velocityMax * -1:
            vx = self.velocityMax * -1

        if vy > self.velocityMax:
            vy = self.velocityMax

        if vy < self.velocityMax * -1:
            vy = self.velocityMax * -1

        self.velocity = (vx, vy)

    def setAssetLocation(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


class Player(GameAsset):

    def __init__(self, image, scale, area):
        # Set defaults for Player
        self.thrust = 0.5
        self.damping = self.thrust * 0.6  # 60% of thurst

        super().__init__(image, scale, area)

    def update(self):
        # Process player Input
        controls = self.getPlayerInput()
        self.setPlayerMotion(controls)
        self.setPlayerAngle(controls)
        self.rotate(self.angle)

        # Continue update
        super().update()

    def getPlayerInput(self):
        up = pygame.key.get_pressed()[pygame.K_UP]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        left = pygame.key.get_pressed()[pygame.K_LEFT]

        return (up, right, down, left)

    def setPlayerMotion(self, controls):
        accX = self.thrust * (controls[1] - controls[3])
        accY = self.thrust * (controls[2] - controls[0])
        self.acceleration = (accX, accY)

    def setPlayerAngle(self, controls):
        # up
        if controls == (1, 0, 0, 0):
            self.angle = 0

        # right + up
        elif controls == (1, 1, 0, 0):
            self.angle = 315

        # right
        elif controls == (0, 1, 0, 0):
            self.angle = 270

        # right + down
        elif controls == (0, 1, 1, 0):
            self.angle = 225

        # down
        elif controls == (0, 0, 1, 0):
            self.angle = 180

        # left + down
        elif controls == (0, 0, 1, 1):
            self.angle = 135

        # left
        elif controls == (0, 0, 0, 1):
            self.angle = 90

        # left + up
        elif controls == (1, 0, 0, 1):
            self.angle = 45


class Enemy(GameAsset):
    pass


class Asteroid(GameAsset):
    pass
