import pygame
from config import *

class Character(pygame.sprite.Sprite):
   def __init__(self, game, x, y, xV, yV):
        self.game = game
        self._layer = CHARACTER_LAYER
        self.groups = self.game.all_sprites, self.game.characters
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.character_spritesheet.get_sprite(xV, yV, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y  