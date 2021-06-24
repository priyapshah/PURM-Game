import pygame
from config import *

class Path(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PATH_LAYER
        self.groups = self.game.all_sprites, self.game.path
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE + (TILESIZE/8)
        self.y = y * TILESIZE + (TILESIZE/8)
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width/2, self.height/2])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class ExpandPath(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PATH_LAYER
        self.groups = self.game.all_sprites, self.game.path
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE + (TILESIZE/8)
        self.y = y * TILESIZE + (TILESIZE/8)
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width/2, self.height/2])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 