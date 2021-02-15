# Imports
from random import randint
import pygame
import sys


# Functions
def null():
    """
    This function does nothing, but it's useful to somethings
    :return: None
    """
    pass


def iterable(obj):
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True


# Boot and game proprieties
pygame.init()
print(" Initting ".center(80, "="))
clock = pygame.time.Clock()  # Game Tick Speed controller
FPS = 12
initial_difficult = 1

# Window and Canvas Properties
resolution = 480  # Use numbers in form: 160x
game_size = 2  # 1: 16 blocks; 2: 32 blocks; 3: 48 blocks...


def block_size():
    global resolution, game_size
    return resolution // (game_size * 16)


pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((resolution, resolution))

# Language load

# Wait a moment


# Font
def main_font(size):
    return pygame.font.SysFont("consolas", size*8)


# Scoring, Checks (and creates if necessary) and opens score file
score: int = 0
HI: int


def load_score():
    global HI
    try:
        a = open(file_name, "rt")
        a.close()
    except FileNotFoundError:
        a = open(file_name, "wt+")
        a.write("0")
        a.close()
    finally:
        a = open(file_name, "rt")
        scoreboard = a.read()
        HI = int(scoreboard)
        a.close()


def save_score():
    print("Saving...")
    saved = True
    try:
        file = open(file_name, "rt")
        file.close()
    except FileNotFoundError:
        print("The score save was lost")
        file = open(file_name, "wt+")
        file.write("0")
        saved = False
    finally:
        file = open(file_name, "wt")
        file.write(str(HI))
        file.close()
    return saved


file_name = "scoreboard.txt"
load_score()


# Entities

# Apple
class Apple:
    pos: tuple
    size: int
    canvas: pygame.Surface = screen

    def __init__(self, size=block_size(), color: tuple = (255, 0, 0)):
        self.color = color
        self.skin = pygame.Surface((size, size))
        self.skin.fill(color)
        self.size = size

    def set_canvas(self, canvas: pygame.Surface = screen):
        self.canvas = canvas

    def new_apple(self):
        self.pos = (randint(0, (self.canvas.get_width() // self.size - 1)) * self.size,
                    randint(0, (self.canvas.get_height() // self.size - 1)) * self.size)
        # Range of randint: 0 to screen size - apple size, but with step equal size

    def resize(self):
        self.size = block_size()
        self.skin = pygame.Surface((block_size(), block_size()))
        self.skin.fill(self.color)

    def draw(self, canvas: pygame.display.set_mode):
        canvas.blit(self.skin, self.pos)


# Snake
class Snake:
    head: tuple
    body: list
    direction: tuple

    def __init__(self, size=block_size(), color: tuple = (255, 255, 255)):
        self.color = color
        self.size = size
        self.skin = pygame.Surface((size, size))
        self.skin.fill(color)

    def spawn(self, x_ratio: float = 2, y_ratio: float = 2, canvas: pygame.Surface = screen):
        global score, HI
        if score > HI:
            HI = score
        score = 0
        self.head = canvas.get_width() // x_ratio, canvas.get_height() // y_ratio  # tuple(map(lambda x: x//2, winSize))
        self.body = [(self.head[0] - self.size, self.head[1]), (self.head[0] - self.size * 2, self.head[1])]
        self.direction = (1, 0)

    def resize(self):
        self.size = block_size()
        self.skin = pygame.Surface((block_size(), block_size()))
        self.skin.fill(self.color)

    # Collisions

    def apple_collision(self, a: Apple, score_update=True):
        global score
        for pos in [self.head] + list(self.body):
            if pos == a.pos:
                if score_update:
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
    
    def edge_collision(self, canvas_size: tuple = (resolution, resolution)):
        # Deadly Edge Mode
        # for coordinate in self.head:
        #     if coordinate in (-self.size, resolution):
        #         self.spawn()
        # The warped edge mode still has flaws...

        # Warped Edge Mode
        if self.head[0] == -self.size:
            self.head = canvas_size[0] - self.size, self.head[1]  # Se eu
        elif self.head[0] == canvas_size[0]:
            self.head = 0, self.head[1]

        if self.head[1] == -self.size:
            self.head = self.head[0], canvas_size[1] - self.size
        elif self.head[1] == canvas_size[1]:
            self.head = self.head[0], 0

    # Movement

    def go_to_apple(self, a: Apple):
        if self.head[0] > a.pos[0]:
            self.left()
        if self.head[0] < a.pos[0]:
            self.right()
        if self.head[0] == a.pos[0]:
            if self.head[1] > a.pos[1]:
                self.up()
            if self.head[1] < a.pos[1]:
                self.down()

    def move_body(self):
        """
        The movement of the body is to follow the head; so, when the head moves, the second square of the snake (which
        is the first of the body) assumes the position of the head, and the second of the body, the first, and so on

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
        try:
            eval("self." + str(pygame.key.name(key)) + "()")
        except AttributeError:
            pass

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

    def draw(self, canvas: pygame.display.set_mode):

        canvas.blit(self.skin, self.head)
        for pos in self.body:
            canvas.blit(self.skin, pos)


# Objects instancing

snake = Snake(color=(0, 255, 0))
apple = Apple()
phantomSnake = Snake(color=(0, 255, 0))
phantomApple = Apple()


# GUI and Scenes
def render(*objects, background=(0, 0, 0), canvas=screen, canvas_pos=(0, 0)):

    """
    Draws and animates objects, sprites and texts on the screen, cleaning and updating

    :param objects: objects to be drawn, it can be a iterable type with objects drawable
    :param background: background color
    :param canvas: window or surface where the objects will be "blitted" (drawn)
    :param canvas_pos: Canvas position in the screen
    :return: None
    """

    if canvas != screen:
        screen.blit(canvas, canvas_pos)

    canvas.fill(background)  # Clears the screen at each frame

    for obj in objects:
        if type(obj) == dict:
            pygame.draw.rect(canvas, obj['color'], obj['rect'])
        elif iterable(obj):
            for o in obj:
                o.draw(canvas)
        else:
            obj.draw(canvas)

    pygame.display.update()


class Label:
    def __init__(self, lbl_msg: str, pos: tuple,
                 font: pygame.font.Font = main_font(2), color: tuple = (0, 0, 0),
                 has_rect: bool = False, rect_color: tuple = (255, 255, 255)):
        self.lbl_obj = font.render(lbl_msg, 0, color)
        self.lbl_box = self.lbl_obj.get_rect()
        self.lbl_box.topleft = pos
        self.has_rect = has_rect
        self.rect_color = rect_color

    def move(self, vector: tuple = (0, 0)):
        self.lbl_box.topleft = tuple(map(lambda x, y: x + y, self.lbl_box.topleft, vector))

    def draw(self, canvas: pygame.Surface):
        if self.has_rect:
            pygame.draw.rect(canvas, self.rect_color, self.lbl_box)
        canvas.blit(self.lbl_obj, self.lbl_box)


class Button:
    def __init__(self, x: int, y: int, width: int, height: int,
                 color: tuple = (255, 255, 255), evt_clk=null, label: str = None):
        """
        :param x: integer left position
        :param y: integer top position
        :param width: rectangle width size
        :param height: rectangle height size
        :param color: rectangle color
        :param evt_clk: function for when the button is clicked
        :param label: string with the button text, if any
        """
        self.pos = x, y
        self.rect = pygame.Rect(x, y, width, height)
        self.default_color = color
        self.color = color
        self.label = Label(label, (x, y))
        self.event_click = evt_clk
        self.event_highlight = self.event_highlight

    def draw(self, canvas: pygame.Surface):
        pygame.draw.rect(canvas, self.color, self.rect)
        if self.label:
            self.label.draw(canvas)

    def move(self, vector: tuple = (0, 0)):
        self.pos = tuple(map(lambda x, y: x + y, self.pos, vector))
        self.label.move(vector)

    def event_highlight(self, highlight: bool):
        if highlight:
            self.color = (0, 255, 0)
        else:
            self.color = self.default_color

    def set_event_click(self, event):
        self.event_click = event

    def set_event_highlight(self, event):
        self.event_highlight = event

    def collision(self, mouse_x: int, mouse_y: int, mouse_click: bool):
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.event_highlight(True)
            if mouse_click:
                self.event_click()
        else:
            self.event_highlight(False)


# Menus
def main_menu():
    menu_screen = pygame.Surface((resolution, resolution))

    # Animation

    phantomSnake.spawn(x_ratio=2, y_ratio=4/3)
    phantomApple.new_apple()

    # Title
    title1 = Label("Snake", (resolution * 4//32, resolution * 3//32), main_font(4),
                   has_rect=True, rect_color=(0, 255, 0))
    title2 = Label("A Minimalist Game", (resolution * 4//32, resolution * 6//32), main_font(2),
                   has_rect=True, rect_color=(0, 255, 0))

    # Buttons
    playBtn = Button(resolution * 4//32, resolution * 12//32, 60, 16, label="> Play", evt_clk=game)
    optionsBtn = Button(resolution * 4//32, resolution * 14//32, 92, 16, label="> Options", evt_clk=options)
    creditsBtn = Button(resolution * 4//32, resolution * 16//32, 92, 16, label="> Credits", evt_clk=credits_game)
    exitBtn = Button(resolution * 4//32, resolution * 18//32, 60, 16, label="> Exit", evt_clk=exit_game)

    buttons = (playBtn, optionsBtn, creditsBtn, exitBtn)

    # Mouse variable declarations
    mx, my = (0, 0)
    mClick = False
    while True:
        # FPS
        clock.tick(FPS*5)

        # Inputting
        for event in pygame.event.get():

            # Exit
            if event.type == pygame.QUIT:
                exit_game()

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mClick = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mClick = False
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

        # Collision
        for button in buttons:
            button.collision(mx, my, mClick)
        phantomSnake.edge_collision()
        phantomSnake.apple_collision(phantomApple, False)
        phantomSnake.self_collision()

        # Animation

        phantomSnake.go_to_apple(phantomApple)
        phantomSnake.move_head()

        # Render
        render(phantomSnake, phantomApple, title1, title2, buttons, canvas=menu_screen)


pause = False


def exit_game():
    if save_score():
        print("Score saved successfully.")
    pygame.quit()
    sys.exit()


def un_pause():
    global pause
    pause = False


def pause_menu():
    global pause
    pause = True

    canvas_size = resolution * 12//16, resolution * 10//16
    canvas_pos = tuple(map(lambda x: (resolution - x)//2, canvas_size))
    pause_screen = pygame.Surface(canvas_size)

    frame1 = {'color': (255, 255, 255), 'rect': pygame.Rect(0, 0, canvas_size[0], canvas_size[1])}
    frame2 = {'color': (0, 0, 0),
              'rect': pygame.Rect(resolution // 32, resolution // 32, canvas_size[0] * 11//12, canvas_size[1] * 7//8)}

    title = Label("Paused", (canvas_size[0] * 1 // 12, canvas_size[1] * 3//24), main_font(3), color=(0, 255, 0))

    continueBtn = Button(canvas_size[0] * 1//12, canvas_size[1] * 6//16, 92, 16, label="> Continue", evt_clk=un_pause)
    optionsBtn = Button(canvas_size[0] * 1//12, canvas_size[1] * 8//16, 82, 16, label="> Options", evt_clk=options)
    menuBtn = Button(canvas_size[0] * 1//12, canvas_size[1] * 10//16, 100, 16, label="> Main Menu", evt_clk=main_menu)
    exitBtn = Button(canvas_size[0] * 1//12, canvas_size[1] * 12//16, 56, 16, label="> Exit", evt_clk=exit_game)

    buttons = (continueBtn, optionsBtn, menuBtn, exitBtn)

    # Mouse variable declarations
    mx, my = (0, 0)
    
    while pause:
        mClick = False
        # FPS
        clock.tick(FPS)  # Difficult Progress

        # Inputting
        for event in pygame.event.get():

            # Exit
            if event.type == pygame.QUIT:
                exit_game()

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mClick = True
            if event.type == pygame.MOUSEMOTION:
                mx, my = map(lambda x, y: x-y, event.pos, canvas_pos)

            # Keyboard
            if event.type == pygame.KEYDOWN:  # If a key is pressed

                # Play
                if pygame.key.name(event.key) in ("escape", "space"):
                    pause = False

        # Collision
        for button in buttons:
            button.collision(mx, my, mClick)

        # Render
        render(frame1, frame2, title, buttons, canvas=pause_screen, canvas_pos=canvas_pos)


back = False


def go_back():
    global back
    back = True


def options():
    global back

    # Buttons
    backBtn = Button(0, 0, 0, 0, evt_clk=go_back)

    buttons = (backBtn, )

    # Mouse variable declarations
    mx, my = (0, 0)
    mClick = False

    while not back:
        # Inputting
        for event in pygame.event.get():

            # Exit
            if event.type == pygame.QUIT:
                exit_game()

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mClick = True
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

            # Keyboard
            if event.type == pygame.KEYDOWN:  # If a key is pressed

                # Play
                if pygame.key.name(event.key) == "escape":
                    back = True

        for button in buttons:
            button.collision(mx, my, mClick)

        # Render
        render(backBtn)


def credits_game():  # the credits function already exits
    return None


# Game
def game():
    score_screen = pygame.Surface((resolution, resolution * 1//16))
    game_screen = pygame.Surface((resolution, resolution * 15//16))

    snake.spawn()
    apple.set_canvas(game_screen)
    apple.new_apple()

    # Pause Button (Não funciona!!!)
    pauseBtn = Button(score_screen.get_width() * 15//16, score_screen.get_height() * 1//4,
                      20, 16, label="II", evt_clk=pause_menu)

    # Mouse variable declarations
    mx, my = (0, 0)
    mClick = False

    # pause_game = False
    run_game = True
    while run_game:
        # FPS
        clock.tick(FPS + (initial_difficult + score-1))

        # Score
        scoreLbl = Label("Score: " + str(score), (score_screen.get_width() * 1//16, score_screen.get_height() * 1//4),
                         color=(0, 255, 0))
        hiScoreLbl = Label("HI: " + str(HI), (score_screen.get_width() * 6//16, score_screen.get_height() * 1//4),
                           color=(255, 0, 0))

        # Inputting
        for event in pygame.event.get():

            # Exit
            if event.type == pygame.QUIT:
                exit_game()

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mClick = True
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

            # Keyboard
            if event.type == pygame.KEYDOWN:  # If a key is pressed

                # print(pygame.key.name(event.key))

                # Pause
                if pygame.key.name(event.key) in ("escape", "space"):
                    # pause_game = not pause_game
                    # print("pause" if pause_game else "play")
                    pause_menu()

                # Moves
                try:  # Because not all keys are being used
                    snake.move_direction(event.key)
                except SyntaxError:
                    pass

        # Move
        snake.move_head()

        # Collisions
        snake.apple_collision(apple)
        snake.self_collision()
        snake.edge_collision((game_screen.get_width(), game_screen.get_height()))
        pauseBtn.collision(mx, my, mClick)

        # Reset mouse pos and click
        mClick = False

        # Render
        render(scoreLbl, hiScoreLbl, pauseBtn, canvas=score_screen, background=(255, 255, 255))
        render(snake, apple, canvas=game_screen, canvas_pos=(0, resolution*1//16))


# Run!
if __name__ == "__main__":
    main_menu()
