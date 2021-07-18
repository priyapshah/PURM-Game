import pygame
from config import *
import random
import time

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 500

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.character_spritesheet.get_sprite(82, 180, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -=1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop +=1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'
        if self.game.currMap[int (self.rect.y/32)][int (self.rect.x/32)] == 'W':
            if self.facing == 'right':
                self.facing = 'left'
                self.rect.x -= 9
            else: 
                self.facing = 'right'
                self.rect.x += 9
                