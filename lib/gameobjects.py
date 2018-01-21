import pygame

from lib.imageloader import imageLoader


class Background(pygame.sprite.Sprite):

    def __init__(self, image, width, height):
        self.OriginalAssetImage = pygame.image.load(image)
        self.image = pygame.transform.scale(
            self.OriginalAssetImage, (width, height))
        self.rect = self.image.get_rect()


class GameAsset(pygame.sprite.Sprite):

    def __init__(self, image, scale, area):
        self.image = imageLoader(image, scale, area)
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def colorkey(self, color):
        self.image.set_colorkey(color)

    def position(self, dest):
        self.rect.x = dest[0]
        self.rect.y = dest[1]


class Player(GameAsset):
    pass


class Enemy(GameAsset):
    pass


class Asteroid(GameAsset):
    pass
