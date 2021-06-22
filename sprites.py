import pygame
from config import *
import math
import random 
from graph import *
from asyncio.tasks import sleep
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.hero
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'DOWN'

        # sprite looks
        self.image = self.game.character_spritesheet.get_sprite(85, 5, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'RIGHT'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'RIGHT'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'UP'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'DOWN'

    # def movement(self, dir):
    #     keys = pygame.key.get_pressed()
    #     if dir == 'L':
    #         self.x_change -= PLAYER_SPEED
    #         self.facing = 'RIGHT'
    #     if dir == 'R':
    #         self.x_change += PLAYER_SPEED
    #         self.facing = 'RIGHT'
    #     if dir == 'U':
    #         self.y_change -= PLAYER_SPEED
    #         self.facing = 'UP'
    #     if dir == 'D':
    #         self.y_change += PLAYER_SPEED
    #         self.facing = 'DOWN'
    
    # click to move
    def clickMovement(self, pos):
        currX = self.rect.x
        currY = self.rect.y
        newX = pos[0]
        newY = pos[1]
        self.getPath(currX, currY, newX, newY)

    def getPath(self, currX, currY, newX, newY):
        # Implement algorithm here
        path = self.game.graph.bfs(int(currX/32), int(currY/32), int(newX/32), int(newY/32))
        for i in path:
            self.rect.x = i.x
            self.rect.y = i.y
            self.game.draw()
            time.sleep(.10)
        return None

    def collide_blocks(self, direction):
        if direction == 'x':
            # last param is bool to delete sprite on collision
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def getXPosition(self):
        return self.rect.x
    
    def getYPosition(self):
        return self.rect.y

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
