import pygame
from config import *

class Button: 
    def __init__(self, x, y, width, height, fg_color, bg_color, content, fontsize):
        self.font = pygame.font.Font('font.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg_color = fg_color
        self.bg_color = bg_color

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg_color)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Text: 
    def __init__(self, x, y, width, height, fg_color, content, fontsize, center):
        self.font = pygame.font.Font('font.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg_color = fg_color

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg_color)
        if center:
            self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        else: 
            self.text_rect = self.text.get_rect()
        self.image.blit(self.text, self.text_rect)