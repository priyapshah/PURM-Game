import pygame
from config import *
import math
import random 
from graph import *
from path import *
from asyncio.tasks import sleep
import time

''' This class corresponds to the main character that is controlled by the user. '''
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
        self.image = self.game.character_spritesheet.get_sprite(85, 10, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.collide_enemy()
        
        self.x_change = 0
        self.y_change = 0
    
    '''Click to move.'''
    def clickMovement(self, pos, mode, tilemap):
        self.walls = ['W', 'F']
        currX = self.rect.x
        currY = self.rect.y
        newX = pos[0]
        newY = pos[1]
        if tilemap[int (newY/TILESIZE)][int (newX/TILESIZE)] in self.walls:
            return
        self.getPath(currX, currY, newX, newY, mode)

    '''Animate movement along path.'''
    def getPath(self, currX, currY, newX, newY, mode):
        # Call algorithm here
        if (mode == 'd'):
            path = self.game.graph.dfs(int(currX/32), int(currY/32), int(newX/32), int(newY/32))
        elif (mode == 'a'):
            path = self.game.graph.aStar(int(currX/32), int(currY/32), int(newX/32), int(newY/32))
        elif (mode == 'i'):
            path = self.game.graph.iddfs(int(currX/32), int(currY/32), int(newX/32), int(newY/32)) 
        elif (mode == 'b'):
            path = self.game.graph.bfs(int(currX/32), int(currY/32), int(newX/32), int(newY/32), True)    
        else: 
            path = self.game.graph.bfs(int(currX/32), int(currY/32), int(newX/32), int(newY/32), False)
        for i in path:
            self.rect.x = i.x
            self.rect.y = i.y
            Path(self.game, int(i.x/32), int(i.y/32))
            self.game.draw()
            time.sleep(.10)
        return None

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def getXPosition(self):
        return self.rect.x
    
    def getYPosition(self):
        return self.rect.y

''' Load images for characters. '''
class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
