import pygame

from lib.imageloader import imageLoader


class Background(pygame.sprite.Sprite):

    def __init__(self, image, width, height):
        self.OriginalAssetImage = pygame.image.load(image)
        self.image = pygame.transform.scale(
            self.OriginalAssetImage, (width, height))
        self.rect = self.image.get_rect()


class GameAsset(pygame.sprite.Sprite):

    velocity = (0, 0)
    acceleration = (0.025, 0.025)
    speed = 1

    def __init__(self, image, scale, area):
        self.image = self.asset = imageLoader(image, scale, area)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.asset, angle)

    def position(self, dest):
        self.rect.x = dest[0]
        self.rect.y = dest[1]

    def update(self):
        # Update the physics
        self.updatePhysics()

    def updatePhysics(self):
        vx = self.velocity[0] + self.acceleration[0]
        vy = self.velocity[1] + self.acceleration[1]
        self.velocity = (vx, vy)
        self.rect.x += self.velocity[0] * self.speed
        self.rect.y += self.velocity[1] * self.speed


class Player(GameAsset):

    def __init__(self, image, scale, area):
        self.acceleration = (0, 0)
        self.speed = 5
        super().__init__(image, scale, area)

    def update(self):
        # Process player Input
        controls = self.getPlayerInput()
        angle = self.getShipMotion(controls)
        if angle is not None:
            self.rotate(angle)

        # Continue update
        super().update()

    def getPlayerInput(self):
        up = pygame.key.get_pressed()[pygame.K_UP]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        left = pygame.key.get_pressed()[pygame.K_LEFT]

        return (up, right, down, left)

    def getShipMotion(self, controls):
        # up
        if controls == (1, 0, 0, 0):
            self.velocity = (0, -1)
            return 0

        # right + up
        elif controls == (1, 1, 0, 0):
            self.velocity = (1, -1)
            return 315

        # right
        elif controls == (0, 1, 0, 0):
            self.velocity = (1, 0)
            return 270

        # right + down
        elif controls == (0, 1, 1, 0):
            self.velocity = (1, 1)
            return 225

        # down
        elif controls == (0, 0, 1, 0):
            self.velocity = (0, 1)
            return 180

        # left + down
        elif controls == (0, 0, 1, 1):
            self.velocity = (-1, 1)
            return 135

        # left
        elif controls == (0, 0, 0, 1):
            self.velocity = (-1, 0)
            return 90

        # left + up
        elif controls == (1, 0, 0, 1):
            self.velocity = (-1, -1)
            return 45

        else:
            self.velocity = (0, 0)
            return None


class Enemy(GameAsset):
    pass


class Asteroid(GameAsset):
    pass
