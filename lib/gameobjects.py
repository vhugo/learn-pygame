import pygame
import random
import math

from lib.imageloader import imageLoader

DELAYTIME = 120


class Background(pygame.sprite.Sprite):

    def __init__(self, image, width, height):
        self.OriginalAssetImage = pygame.image.load(image)
        self.image = pygame.transform.scale(
            self.OriginalAssetImage, (width, height))
        self.rect = self.image.get_rect()


class Animation():

    currentFrame = 0
    currentLoop = 0
    loop = 0

    def __init__(self, image, frames, framesPerImage, frameSize):
        self.frames = []
        self.framesPerImage = framesPerImage
        self.totalFrames = frames
        self.frameSize = frameSize
        self.image = image

        self.loadFrames()

    def loadFrames(self):
        pass

    def getFrame(self):
        frame = self.frames[self.currentFrame]

        self.currentLoop += 1
        if self.currentLoop % self.framesPerImage == 0:
            self.currentFrame += 1

        if self.currentFrame >= self.totalFrames:
            self.currentFrame = 0
            self.loop += 1

        if self.loop > 0:
            frame = pygame.Surface((0, 0))

        return frame

    def reset(self):
        self.currentFrame = 0
        self.currentLoop = 0
        self.loop = 0


class Explosion(Animation):

    def __init__(self):
        super().__init__("images/explode.bmp", 6, 15, (24, 25))

    def loadFrames(self):
        startX = 0
        for i in range(self.totalFrames):
            image = imageLoader(
                self.image,
                1,
                (startX, 0, self.frameSize[0], self.frameSize[1])
            )
            image.set_colorkey(image.get_at((0, 0)))
            self.frames.append(image)
            startX += self.frameSize[0]


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
    targetState = 1
    collisionCause = None
    collisionAnimation = None

    def __init__(self, image, scale, area, bounds):
        self.image = self.asset = imageLoader(image, scale, area)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.bounds = bounds
        self.collision = False
        self.collisionGroup = []
        self.animation = []

        self.loadAnimations()
        self.spawning()

    def loadAnimations(self):
        self.collisionAnimation = Explosion()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.asset, angle)

    def spawning(self, position=None):
        if position is None:
            self.randomPosition()
        else:
            self.spawnPosition = position
            self.position(position)

        self.onSpawn()

    def respawning(self):
        self.spawning(self.spawnPosition)

    def reset(self):
        self.collisionCause = None
        self.targetState = 1

        if self.spawnPosition is None:
            self.randomPosition()
        else:
            self.position(self.spawnPosition)

    def onSpawn(self):
        pass

    def onCollision(self):
        self.image = self.collisionAnimation.getFrame()
        pass

    def onDeath(self):
        self.collisionAnimation.reset()
        if self.collisionCause is not None:
            self.collisionCause.onDeath()

        self.reset()

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

        # Collision detection
        self.checkForCollisions()

        # Update the physics
        self.updatePhysics()

    def checkBoundaries(self):
        if self.rect.x > self.bounds[0] or self.rect.y > self.bounds[1]:
            self.reset()

    def checkForCollisions(self):
        for asset in self.collisionGroup:
            self.collision = self.rect.colliderect(asset.rect)
            if self.collision:
                self.collisionCause = asset
                print("COLLISION", self.collisionCause.__class__.__name__)
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


class Player(GameAsset):

    def __init__(self, image, scale, area, bounds):
        # Set defaults for Player
        self.thrust = 0.5
        self.damping = self.thrust * 0.6  # 60% of thurst

        super().__init__(image, scale, area, bounds)

    def spawning(self, position=None):
        position = (int(self.bounds[0] / 2), int(self.bounds[1] / 2))
        super().spawning(position)

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
        self.delayEvents = DELAYTIME  # delay event 120 cycles
        super().onCollision()

    def onDeath(self):
        self.angle = 0
        self.rotate(0)
        self.velocity = (0, 0)

        self.respawning()
        super().onDeath()


class GameHazard(GameAsset):

    def __init__(self, image, scale, area, bounds, waveManager):
        self.waveManager = waveManager

        super().__init__(image, scale, area, bounds)

    def spawning(self, position=None):
        if self.waveManager.allowSpawn():
            super().spawning(position)

    def onSpawn(self):
        self.waveManager.hazardSpawned()
        super().onSpawn()

    def onDeath(self):
        self.waveManager.hazardDied()
        super().onDeath()

    def update(self):
        # wave progression
        self.waveManager.update()

        # Behavior based on target
        self.followTarget()
        super().update()

    def setTarget(self, target):
        self.target = target

    def followTarget(self):
        if self.target is None:
            return

        pursuitRange = math.sqrt(
            (self.rect.x - self.target.rect.x) ** 2 +
            (self.rect.y - self.target.rect.y) ** 2
        )

        # State 1 - Search
        if self.targetState == 1:
            if pursuitRange < self.targetRange:
                self.targetState = 2
            else:
                self.velocity = (
                    self.velocity[0] + self.thrust,
                    self.velocity[1] + self.thrust
                )

        # State 2 - Pursuit target
        elif self.targetState == 2:
            if pursuitRange >= self.targetRange:
                self.targetState = 3
            else:
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

        # State 3 - Disengage pursuit
        elif self.targetState == 3:
            self.velocity = (
                self.velocity[0] + self.thrust,
                self.velocity[1] + self.thrust
            )


class Enemy(GameHazard):

    def __init__(self, image, scale, area, bounds, waveManager):
        # Set defaults for Enemy
        self.spawnOutOfView = True
        self.thrust = 0.25
        self.damping = self.thrust * 0.6  # 60% of thurst
        self.velocityMax = 4

        super().__init__(image, scale, area, bounds, waveManager)

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


class WaveManager():

    def __init__(self, hazardsPerWave, scoreBoard):
        self.currentWave = 1
        self.hazardSpawnedCount = 0
        self.hazardDeathCount = 0
        self.hazardsPerWave = hazardsPerWave
        self.delayEvents = 0
        self.scoreBoard = scoreBoard

    def allowSpawn(self):
        return self.hazardSpawnedCount <= self.hazardsPerWave

    def hazardSpawned(self):
        self.hazardSpawnedCount += 1

    def hazardDied(self):
        self.hazardDeathCount += 1
        self.scoreBoard.points += 1

        if self.hazardDeathCount == self.hazardsPerWave:
            self.nextWave()

    def nextWave(self):
        self.hazardSpawnedCount = 0
        self.hazardDeathCount = 0
        self.hazardsPerWave += 3
        self.currentWave += 1
        self.delayEvents = DELAYTIME
        self.scoreBoard.waves = self.currentWave

    def update(self):
        pass
        # print(
        #     "Wave: %3d " % self.currentWave,
        #     "PerWave: %3d " % self.hazardsPerWave,
        #     "Spawed: %3d " % self.hazardSpawnedCount,
        #     "Died: %3d " % self.hazardDeathCount)


class Sprite():

    def __init__(self, image):
        self.sprite = []
        self.image = image
        self.loadSprite()

    def loadSprite(self):
        pass


class ScoreBoard(Sprite):

    def __init__(self):
        self.points = 0
        self.waves = 0
        super().__init__("images/numbers.bmp")

    def loadSprite(self):
        for i in range(0, 10):
            image = imageLoader(
                self.image,
                1,
                ((30 * i), 0, 30, 49)
            )
            image.set_colorkey(image.get_at((0, 0)))
            self.sprite.append(image)

    def getNumber(self, number):
        numbers = [int(n) for n in str(number)]
        total = len(numbers)
        nSurface = pygame.Surface(((30 * total), 49))
        nSurface.set_colorkey((0, 0, 0))

        for idx, n in enumerate(numbers):
            xy = (30 * idx, 0)
            nSurface.blit(self.sprite[n], xy)

        return nSurface

    def getScore(self):
        return self.getNumber(self.points)

    def getWave(self):
        return self.getNumber(self.waves)
