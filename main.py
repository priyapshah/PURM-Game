import pygame
from sprites import *
from config import *
from wall import *
from graph import *
from path import *
from characters import *
import sys

class Game:

    def __init__(self):

        # create game window
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # load images 
        self.character_spritesheet = Spritesheet('img/ch3.png')
        self.terrain_spritesheet = Spritesheet('img/mapchip.gif')
    
        # start game with BFS traversal 
        self.mode = 'b'

    # Read in tilemap and create the tiles on the game screen
    def createTileMap(self, tilemap):
        self.currMap = tilemap
        self.graph = Graph(tilemap, self)
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == 'P':
                    self.createTile(tilemap[i][j+1], i, j)
                    Player(self, j, i)
                    continue
                elif column == 'K':
                    self.createTile(tilemap[i][j+1], i, j)
                    Character(self, j, i, 0, 6)
                    continue
                else:
                    self.createTile(column, i, j)

    # Call the correct tile class
    def createTile(self, char, i, j):
        if char == 'W':
            Wall(self, j, i)
        elif char == 'G':
            Ground(self, j, i, 96, 0)
        elif char == 'F':
            Ground(self, j, i, 124, 0)
        elif char == 'D':
            Ground(self, j, i, 64, 64)
        else:
            Ground(self, j, i, 0, 0)
        return


    # Adds background music
    def playMusic(self, int):
        if (int == 2):
            pygame.mixer.init()
            soundObj = pygame.mixer.Sound('sound/door.wav')
            soundObj.play()

            pygame.mixer.music.load('sound/bgm/castle.mid')
            pygame.mixer.music.play(-1)
        else: 
            pygame.mixer.init()
            pygame.mixer.music.load('sound/bgm/castle.mid')
            pygame.mixer.music.play(-1)

        #"Déjà Vu" by Mort Garson
              
    # Initialize a new game
    def newGame(self):
        self.playing = True

        # define group of sprites

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.hero = pygame.sprite.LayeredUpdates()
        self.path = pygame.sprite.LayeredUpdates()
        self.characters = pygame.sprite.LayeredUpdates()

    # Clear the current game screen
    def clearBoard(self):
        for sprite in self.all_sprites:
            sprite.kill()

    # Handle player events
    def events(self):
        # for event in pygame.event.get():
        #     if pygame.key.get_pressed()[pygame.K_SPACE]:
        #         print(event)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            # Click to move
            if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # move only the first sprite
                    Player.clickMovement(self.hero.get_sprite(0), pos, self.mode)

                    for sprite in self.path:
                         sprite.kill()

            # Change screens
            if pygame.key.get_pressed()[pygame.K_SPACE] and event.type != 771 and self.DoorEvent(self.hero.get_sprite(0)):
                self.clearBoard()
                self.createTileMap(self.nextMap)
                continue
                # self.playMusic(2)

            # Switch to DFS Traversal
            if pygame.key.get_pressed()[pygame.K_d]:
                self.mode = 'd'

            # Switch to BFS Traversal
            if pygame.key.get_pressed()[pygame.K_b]:
                self.mode = 'b'

            # Switch to A* Traversal
            if pygame.key.get_pressed()[pygame.K_a]:
                self.mode = 'a'

                
    # Check if player at door
    def DoorEvent(self, Player):
        if self.currMap == tilemap1:
            y = self.hero.get_sprite(0).getYPosition()
            x = self.hero.get_sprite(0).getXPosition()
            if y >= 608 and x >= 544 and x <= 576:
                self.nextMap = tilemap2
                return 1
            if y >= 96 and y <= 128 and x >= 608:
                self.nextMap = tilemap3
                return 1
        if self.currMap == tilemap2:
            y = self.hero.get_sprite(0).getYPosition()
            x = self.hero.get_sprite(0).getXPosition()
            if y <= 32 and x >= 544 and x <= 576:
                self.nextMap = tilemap1
                return 1
        return 0

    def update(self):
        self.all_sprites.update()

    def draw(self):
        # draw sprite
        self.all_sprites.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

game = Game()
game.newGame()

game.createTileMap(tilemap1)
# game.playMusic(1)


while game.running:
    game.main()

pygame.quit()
sys.exit()