import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from pygame.locals import *

global rows, width, snake, snack, start
canMoveTime = 0


class Cube(object):

    def __init__(self, start, dirnx=0, dirny=0, color=(0, 255, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, head=False):
        dis = width // rows
        i = self.pos[0]
        j = self.pos[1]

        if head:
            self.color = (255, 0, 0)

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 1, dis - 1))


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

    def check_dead(self):
        global start
        c = self.body[0]
        if c.pos[0] > rows - 1 or c.pos[1] > rows - 1 or c.pos[0] < 0 or c.pos[1] < 0:
            score = "Score: " + str(len(snake.body) - 1)
            message_box('You lost!', score)
            snake.reset((10, 10))
            start = False
        if c.pos in list(map(lambda z: z.pos, self.body[1:])):
            score = "Score: " + str(len(snake.body) - 1)
            message_box('You lost!', score)
            snake.reset((10, 10))
            start = False

    def move(self, k):

        key = k

        if key == 'right' and self.dirnx == 0:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif key == 'left' and self.dirnx == 0:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif key == 'up' and self.dirny == 0:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif key == 'down' and self.dirny == 0:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 0

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        if dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        if dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        if dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface)


def draw_grid(w, r, surface):
    size_between = w // r

    x = 0
    y = 0

    for num in range(r):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface):
    global width, rows, snake
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface, True)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(r, s):
    positions = s.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # snack_pos = (x, y)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global rows, width, snake, snack, start
    width = 500
    rows = 20
    snake = Snake((0, 255, 0), (10, 10))
    win = pygame.display.set_mode((width, width))
    snack = Cube(random_snack(rows, snake))
    start = False

    clock = pygame.time.Clock()

    while True:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        start = pygame.key.get_pressed()[pygame.K_SPACE]

        switcher = {
            0: "right",
            1: "left",
            2: "up",
            3: "down"
        }

        output = switcher.get(random.randint(0, 3))

        if start:
            print(output)
            snake.move(output)

        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(rows, snake))
        snake.check_dead()
        redraw_window(win)


if __name__ == '__main__':
    main()
