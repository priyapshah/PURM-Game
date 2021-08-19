import pygame
from sprites import *
from config import *
from wall import *
from graph import *
from path import *
from characters import *
from enemy import *
from instructions import *
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
        self.font = pygame.font.Font('font.ttf', 32)
        self.intro_background = pygame.image.load('bg.jpeg').convert()

        self.mode = 'n'
        self.iter = 1

    ''' Reads tilemap line by line to create a matching tile onto the game board. Tiles under characters are set to the adjacent tile and the character is placed on a level above. Inputs:
    - tilemap: the design of the screen. Should be declared in config.py'''

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
                elif column == 'E':
                    self.createTile(tilemap[i][j+1], i, j)
                    Enemy(self, j, i)
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

    '''Uses pygame.mixer to run an audio clip for background music throughout game play. Inputs: 
    - int: the number of the audio clip to be played on the screen.'''
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

    '''Handle player events. Controls the display of the instructions as well as navigating between screens.'''
    def events(self):
        if self.iter == 2:
            self.text_screen("Click on a door and press space to enter.")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            # Click to move
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # move only the first sprite
                Player.clickMovement(self.hero.get_sprite(
                    0), pos, self.mode, self.currMap)

                for sprite in self.path:
                    sprite.kill()

            # Change screens
            if pygame.key.get_pressed()[pygame.K_SPACE] and event.type != 771 and self.DoorEvent(self.hero.get_sprite(0)):
                self.clearBoard()
                if (self.nextMap == tilemap4):
                    self.createMaze()
                else:
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

            # Switch to I-DFS Traversal
            if pygame.key.get_pressed()[pygame.K_i]:
                self.mode = 'i'

            if pygame.key.get_pressed()[pygame.K_n]:
                self.mode = 'n'

            self.iter += 1

    '''Checks if player's position corresponds to door coordinates and sets the next map to load.'''

    def DoorEvent(self, Player):
        if self.currMap == tilemap1:
            y = self.hero.get_sprite(0).getYPosition()
            x = self.hero.get_sprite(0).getXPosition()
            if y >= 608 and x >= 544 and x <= 576:
                self.nextMap = tilemap2
                return 1
            if y >= 96 and y <= 128 and x >= 608:
                self.nextMap = tilemap4
                return 1
        if self.currMap == tilemap2:
            y = self.hero.get_sprite(0).getYPosition()
            x = self.hero.get_sprite(0).getXPosition()
            if y <= 32 and x >= 544 and x <= 576:
                self.nextMap = tilemap1
                return 1
        if self.currMap == self.tilemap5:
            y = self.hero.get_sprite(0).getYPosition()
            x = self.hero.get_sprite(0).getXPosition()
            if y <= 32 and x <= 32:
                self.nextMap = tilemap1
                return 1
        return 0

    ''' Used to create tilemap based off of randomely generated maze algorithm in graph.py. '''
    def createMaze(self):
        self.createTileMap(tilemap4)
        mazePath = self.graph.mazeDFS(0, 0)
        mP = []
        for m in mazePath:
            mP.append([m.gridX, m.gridY])

        self.tilemap5 = []

        for i, row in enumerate(tilemap4):
            r = []
            for j, column in enumerate(row):
                if [i, j] == [0, 0]:
                    r.append('D')
                elif [i, j] == [1, 0]:
                    r.append('P')
                elif [i, j] == [1, 1]:
                    r.append('.')
                elif [i, j] in mP:
                    r.append('.')
                else:
                    r.append('W')
            self.tilemap5.append(r)

        self.createTileMap(self.tilemap5)

    ''' Defines the introduction screen with title and instructions. '''
    def intro_screen(self):
        intro = True

        title = self.font.render('Castle Escape', True, WHITE)
        title_rect = title.get_rect(x=170, y=25)
        ins = Text(75, 200, 500, 25, WHITE, ' Instructions ', 16, True)
        ins1 = Text(75, 225, 500, 50, WHITE,
                    ' Escape the castle! Click to move and avoid enemies. ', 12, True)
        ins2 = Text(75, 275, 500, 25, WHITE,
                    ' Press the \'b\' key for BFS  ', 16, False)
        ins3 = Text(75, 300, 500, 25, WHITE,
                    ' Press the \'d\' key for DFS  ', 16, False)
        ins4 = Text(75, 325, 500, 25, WHITE,
                    ' Press the \'a\' key for A*  ', 16, False)
        ins5 = Text(75, 350, 500, 25, WHITE,
                    ' Press the \'i\' key for Iterative DFS  ', 16, False)
        ins6 = Text(75, 375, 500, 25, WHITE,
                    ' Press the \'n\' key for Default View ', 16, False)
        play_button = Button(75, 500, 500, 50, BLACK,
                             WHITE, ' Accept Challenge ', 16)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                del(play_button)
                intro = False
                return

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(ins.image, ins.rect)
            self.screen.blit(ins1.image, ins1.rect)
            self.screen.blit(ins2.image, ins2.rect)
            self.screen.blit(ins3.image, ins3.rect)
            self.screen.blit(ins4.image, ins4.rect)
            self.screen.blit(ins5.image, ins5.rect)
            self.screen.blit(ins6.image, ins6.rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def text_screen(self, text):
        tik = time.perf_counter()
        tok = time.perf_counter()

        screen_text = Text(75, 500, 500, 50, WHITE, text, 16, True)

        while tok-tik <= 1:
            self.screen.blit(screen_text.image, screen_text.rect)
            self.clock.tick(FPS)
            pygame.display.update()

            tok = time.perf_counter()

        del(screen_text)
        return

    def update(self):
        self.all_sprites.update()

    def draw(self):
        # draw sprite
        self.all_sprites.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self, iter):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False


game = Game()
game.intro_screen()
game.newGame()

game.createTileMap(tilemap1)
game.playMusic(1)


while game.running:
    game.main(1)

pygame.quit()
sys.exit()
