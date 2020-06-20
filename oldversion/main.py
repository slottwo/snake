# Imports
import pygame
from random import randint

# Boot
pygame.init()

# Window
screen_size = (320, 320)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake")

# Game's presets
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)

# Variables
HIValue = 0
scoreValue = 0
temp1 = screen_size[1] // 2
temp2 = (screen_size[0] - 32) // 2
initialPos = [(temp1+16, temp2), (temp1+8, temp2), (temp1, temp2)]
del temp1, temp2

# Snake
snake = {
    "pos": initialPos,
    "skin": pygame.Surface((8, 8)),
    "dir": 'right'
}
snake['skin'].fill((255, 255, 255))

# Apple
apple = {
    "pos": (randint(0, 39) * 8, randint(4, 39) * 8),
    "skin": pygame.Surface((8, 8))
}
apple['skin'].fill((255, 0, 0))


def new_apple():
    x, y = randint(0, 39) * 8, randint(4, 39) * 8
    while (x, y) in snake['pos']:
        x, y = randint(0, 39) * 8, randint(4, 39) * 8
    apple['pos'] = (x, y)


# Inputs
def up():
    snake['dir'] = 'UP' if snake['dir'] != 'DOWN' else snake['dir']


def down():
    snake['dir'] = 'DOWN' if snake['dir'] != 'UP' else snake['dir']


def right():
    snake['dir'] = 'RIGHT' if snake['dir'] != 'LEFT' else snake['dir']


def left():
    snake['dir'] = 'LEFT' if snake['dir'] != 'RIGHT' else snake['dir']


# Movement
def RIGHT():
    body_move()
    if snake['pos'][0][0] > 39 * 8:
        snake['pos'][0] = (0, snake['pos'][0][1])
    else:
        snake['pos'][0] = (snake['pos'][0][0] + 8, snake['pos'][0][1])


def LEFT():
    body_move()
    if snake['pos'][0][0] < 0:
        snake['pos'][0] = (312, snake['pos'][0][1])  # 39 * 8
    else:
        snake['pos'][0] = (snake['pos'][0][0] - 8, snake['pos'][0][1])


def UP():
    body_move()
    if snake['pos'][0][1] < 5 * 8:
        snake['pos'][0] = (snake['pos'][0][0], 312)  # 39 * 8
    else:
        snake['pos'][0] = (snake['pos'][0][0], snake['pos'][0][1] - 8)


def DOWN():
    body_move()
    if snake['pos'][0][1] > 39 * 8:
        snake['pos'][0] = (snake['pos'][0][0], 32)  # 4 * 8
    else:
        snake['pos'][0] = (snake['pos'][0][0], snake['pos'][0][1] + 8)


def body_move():
    for i, pos in enumerate(snake['pos'][-2::-1]):
        snake['pos'][-i-1] = pos
    # snake['pos'][2] = snake['pos'][1]
    # snake['pos'][1] = snake['pos'][0]


# Collisions
def eat_apple():
    global scoreValue
    if apple["pos"] in snake["pos"]:
        scoreValue += 1
        print("eat!")
        snake['pos'].append(snake['pos'][-1])
        new_apple()


def self_collision():
    return snake['pos'][0] in snake['pos'][1:]


def wall_collision():
    pass


# Re-spawn
def re_spawn():
    global HIValue, scoreValue, snake
    while len(snake['pos']) > 3:
        snake['pos'].pop()
    snake['pos'] = initialPos
    snake['dir'] = 'right'
    new_apple()
    HIValue = max(scoreValue, HIValue)
    scoreValue = 0


# Game
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
        if event.type == pygame.KEYDOWN:
            try:
                eval(str(pygame.key.name(event.key)) + "()")
            except SyntaxError:
                pass

    # Moving
    eval(snake['dir'] + "()")

    # Collisions
    eat_apple()
    if self_collision():
        re_spawn()

    # Render
    screen.fill((0, 0, 0))

    for pos in snake['pos']:
        screen.blit(snake['skin'], pos)

    screen.blit(apple['skin'], apple['pos'])

    # Score Viewer
    score = font.draw(f"Score: {scoreValue}", True, (255, 0, 0))
    HI = font.draw(f"HI: {HIValue}", True, (0, 255, 0))

    panel = pygame.Surface((320, 32))
    panel.fill((255, 255, 255))
    screen.blit(panel, (0, 0))

    screen.blit(score, (8, 8))
    screen.blit(HI, (128, 8))

    pygame.display.update()
