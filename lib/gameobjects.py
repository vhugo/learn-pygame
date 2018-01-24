import pygame
import random
import math

from lib.imageloader import imageLoader


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
    spawnPosition = None
    spawnOutOfView = False
    delayEvents = 0
    speed = 2
    target = None
    targetRange = 300

    def __init__(self, image, scale, area, bounds):
        self.image = self.asset = imageLoader(image, scale, area)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.bounds = bounds
        self.collision = False
        self.collisionGroup = []

        self.onSpawn()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.asset, angle)

    def spawning(self, position=None):
        if position is None:
            self.randomPosition()
        else:
            self.spawnPosition = position
            self.position(position)

    def respawning(self):
        self.spawning(self.spawnPosition)

    def onSpawn(self):
        self.spawning()

    def onCollision(self):
        pass

    def onDeath(self):
        self.respawning()

    def position(self, dest):
        self.rect.x = dest[0]
        self.rect.y = dest[1]

    def randomPosition(self):
        xy = (
            random.randrange(0, self.bounds[0] - self.image.get_width()),
            random.randrange(0, self.bounds[1] - self.image.get_height()))

        if self.spawnOutOfView:
            xy = (xy[0] * -1, xy[1] * -1, )

        self.position(xy)

        # Checking for overlaping objects that collides, if collision group is
        # empty the following lines will be ignored
        for asset in self.collisionGroup:
            if self.rect.colliderect(asset.rect):
                self.randomPosition()

    def update(self):
        # Boundaries
        self.checkBoundaries()

        # Behavior based on target
        self.followTarget()

        # Collision detection
        self.checkForCollisions()

        # Update the physics
        self.updatePhysics()

    def checkBoundaries(self):
        if self.rect.x > self.bounds[0] or self.rect.y > self.bounds[1]:
            self.spawning()

    def checkForCollisions(self):
        for asset in self.collisionGroup:
            self.collision = self.rect.colliderect(asset.rect)
            if self.collision:
                self.onCollision()
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

    def setTarget(self, target):
        self.target = target

    def followTarget(self):
        if self.target is None:
            return

        pursuitRange = math.sqrt(
            (self.rect.x - self.target.rect.x) ** 2 +
            (self.rect.y - self.target.rect.y) ** 2
        )

        # Check if target is in range, engage pursuit
        if pursuitRange < self.targetRange:

            targetDistance = (
                self.target.rect.x - self.rect.x,
                self.target.rect.y - self.rect.y
            )

            distance = math.sqrt(
                (0 - targetDistance[0]) ** 2 +
                (0 - targetDistance[1]) ** 2
            )

            trackingVelocity = (
                ((targetDistance[0] / distance) * self.speed),
                ((targetDistance[1] / distance) * self.speed)
            )

            moveDistance = (
                self.rect.x + trackingVelocity[0],
                self.rect.y + trackingVelocity[1]
            )

            self.velocity = trackingVelocity
            self.position(moveDistance)


class Player(GameAsset):

    def __init__(self, image, scale, area, bounds):
        # Set defaults for Player
        self.thrust = 0.5
        self.damping = self.thrust * 0.6  # 60% of thurst

        super().__init__(image, scale, area, bounds)

    def onSpawn(self):
        self.spawning((int(self.bounds[0] / 2), int(self.bounds[1] / 2)))

    def update(self):
        # Process player Input
        controls = self.getPlayerInput()
        self.setPlayerMotion(controls)
        self.setPlayerAngle(controls)
        self.rotate(self.angle)

        # Continue update
        super().update()

    def checkBoundaries(self):
        boundx = self.bounds[0] - self.image.get_width()
        boundy = self.bounds[1] - self.image.get_height()

        if self.rect.x >= boundx:
            self.rect.x = boundx

        if self.rect.x <= 0:
            self.rect.x = 0

        if self.rect.y >= boundy:
            self.rect.y = boundy

        if self.rect.y <= 0:
            self.rect.y = 0

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

    def onCollision(self):
        self.delayEvents = 120  # delay event 120 cycles
        super().onCollision()

    def onDeath(self):
        self.angle = 0
        self.rotate(0)
        self.velocity = (0, 0)

        super().onDeath()


class Enemy(GameAsset):

    def __init__(self, image, scale, area, bounds):
        # Set defaults for Enemy
        self.spawnOutOfView = True
        self.thrust = 0.25
        self.damping = self.thrust * 0.6  # 60% of thurst
        self.velocityMax = 4

        super().__init__(image, scale, area, bounds)

    def update(self):
        self.setEnemyMotion()
        super().update()

    def setEnemyMotion(self):
        self.acceleration = (self.thrust, self.thrust)


class Asteroid(GameAsset):

    def __init__(self, image, scale, area, bounds):
        # Set defaults for Asteroid
        self.spawnOutOfView = True
        self.velocity = (1, 1)

        super().__init__(image, scale, area, bounds)
