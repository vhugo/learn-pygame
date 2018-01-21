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
    acceleration = (0.25, 0.25)

    def __init__(self, image, scale, area):
        self.image = imageLoader(image, scale, area)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def position(self, dest):
        self.rect.x = dest[0]
        self.rect.y = dest[1]

    def update(self):
        vx = self.velocity[0] + self.acceleration[0]
        vy = self.velocity[1] + self.acceleration[1]
        self.velocity = (vx, vy)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


class Player(GameAsset):

    def __init__(self, image, scale, area):
        self.acceleration = (0.50, 0.50)
        super().__init__(image, scale, area)


class Enemy(GameAsset):
    pass


class Asteroid(GameAsset):
    pass
