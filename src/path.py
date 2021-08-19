import pygame
from config import *

''' Defines the objects that makeup the colored tiles representing the path of the player. '''
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
    def __init__(self, game, x, y, color):
        self.game = game
        self._layer = PATH_LAYER
        self.groups = self.game.all_sprites, self.game.path
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE - (TILESIZE/8)
        self.height = TILESIZE - (TILESIZE/8)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 
