# Imports
import pygame
from random import randint

# Boot
pygame.init()

# Window
resolution = 160
screen = pygame.display.set_mode((resolution, resolution))

pygame.display.set_caption("Snake")

# Game presets
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)

# Score

file_name = "scoreboard.txt"

# Checks (and creates if necessary) and opens score file

score = 0

try:
    a = open(file_name, "rt")
    a.close()
except:
    a = open(file_name, "wt+")
    a.write("0")
    a.close()
finally:
    a = open(file_name, "rt")
    scoreboard = a.read()
    HI = int(scoreboard)
    a.close()

# Scenes and Gui

'''
# Play
# - pause
#   - return to game
#   - options
#   - initial screen
#   - quit

# Ranking
# - back

# Options
# - resolution
# - sound?
# - back

# Credits
# - back

# Quit
'''


# Apple

class Apple:
    pos: tuple
    size: int

    def __init__(self, size=resolution//20, color: tuple = (255, 0, 0)):
        self.skin = pygame.Surface((size, size))
        self.skin.fill(color)
        self.size = size
        self.new_apple()

    def new_apple(self):
        global resolution
        self.pos = (randint(0, (resolution // self.size - 1)) * self.size,
                    randint(0, (resolution // self.size - 1)) * self.size)
        # Range of randint: 0 to screen size - apple size, but with step equal size

    def render(self, canvas: pygame.display.set_mode):
        canvas.blit(self.skin, self.pos)


# Snake

class Snake:
    head: tuple
    body: list
    direction: tuple

    def __init__(self, size=resolution//20, color: tuple = (255, 255, 255)):
        self.color = color
        self.size = size
        self.skin = pygame.Surface((size, size))
        self.skin.fill(color)
        self.spawn()

    def spawn(self):
        global score, HI
        if score > HI:
            HI = score
        score = 0
        self.head = (resolution // 2, resolution // 2)  # tuple(map(lambda x: x//2, winSize))
        self.body = [(self.head[0] - self.size, self.head[1]),
                     (self.head[0] - self.size * 2, self.head[1])]
        self.direction = (1, 0)

    # Collisions

    def apple_collision(self, a: Apple):
        global score
        if self.head == a.pos:
            score += 1
            self.body.append(self.body[-1])
            a.new_apple()

    def self_collision(self):
        if self.head in self.body:
            self.spawn()

    # def wall_collision(self):  # , walls: tuple
    #     # if self.head in walls:
    #     #     self.spawn()
    #     pass
    def edge_collision(self):
        global resolution
        # Deadly Edge Mode
        # for coordinate in self.head:
        #     if coordinate in (-self.size, resolution):
        #         self.spawn()
        # The warped edge mode still has flaws...
        # Warped Edge Mode
        if self.head[0] == -self.size:
            self.head = resolution-self.size, self.head[1]  # Se eu
        elif self.head[0] == resolution:
            self.head = 0, self.head[1]

        if self.head[1] == -self.size:
            self.head = self.head[0], resolution-self.size
        elif self.head[1] == resolution:
            self.head = self.head[0], 0

    # Movement

    def move_body(self):
        # The movement of the body is to follow the head; so, when the head moves, the second square of the snake (which
        # is the first of the body) assumes the position of the head, and the second of the body, the first, and so on

        """

        :return: None
        """

        # self.body = [self.body[0]] + self[0:-2]  # e.g. [a, b, c, d, e] -> [a, a, b, c, d]
        for k, pos in enumerate(self.body[-2::-1]):  # Its take from the penultimate element to the first
            self.body[-k - 1] = pos  # body[-1] <- body[-2] ; body[-2] <- body[-3] ; ...
        self.body[0] = self.head

    def move_head(self):
        self.move_body()
        self.head = tuple(map(lambda x, y: x + y * self.size, self.head, self.direction))

    # Input

    def move_direction(self, key: int):
        """
        Take a key index to get the name of key, then call the Snake method with the same name

        :param key: A integer that represent the key pressed
        :return: None
        """
        eval("self." + str(pygame.key.name(key)) + "()")

    def up(self):
        if self.direction != (0, 1):
            self.direction = (0, -1)

    def down(self):
        if self.direction != (0, -1):
            self.direction = (0, 1)

    def left(self):
        if self.direction != (1, 0):
            self.direction = (-1, 0)

    def right(self):
        if self.direction != (-1, 0):
            self.direction = (1, 0)

    def render(self, canvas: pygame.display.set_mode):

        canvas.blit(self.skin, self.head)
        for pos in self.body:
            canvas.blit(self.skin, pos)


# Objects

snake = Snake()

apple = Apple()

# Game

pauseGame = False
runGame = True
while runGame:
    # FPS
    clock.tick(6)

    # Inputting
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            runGame = False
        # Moves
        if event.type == pygame.KEYDOWN:  # If a key is pressed
            try:  # Because not all keys are being used
                snake.move_direction(event.key)
            except AttributeError:
                pass
            if pygame.key.name(event.key) == "space":
                pauseGame = not pauseGame
                print("pause" if pauseGame else "play")

    if not pauseGame:
        # Move
        snake.move_head()

        # Collisions
        snake.apple_collision(apple)
        snake.self_collision()
        snake.edge_collision()

    # Render
    screen.fill((0, 0, 0))  # Clears the screen at each frame

    snake.render(screen)

    apple.render(screen)

    pygame.display.update()

print("Code finished. Bye!")
print(score)
print(HI)
a = open(file_name, "wt+")
a.write(str(HI))
