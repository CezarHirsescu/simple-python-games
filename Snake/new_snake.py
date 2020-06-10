import pygame as py
from random import randint
import tkinter as tk
from tkinter import messagebox

width = 600
grid_length = 25
size = width // grid_length


class Cube(object):
    global size

    def __init__(self, pos_x, pos_y, dir_x, dir_y, color=(255, 0, 0), eyes=False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.color = color
        self.eyes = eyes

    def draw_cube(self, window):
        py.draw.rect(window, self.color, (self.pos_x, self.pos_y, size, size))
        if self.eyes:
            pass


class Snake(object):
    global size

    def __init__(self, window):
        self.window = window
        self.head = Cube(5 * size, 5 * size, 1, 0, eyes=True)
        self.body = []
        self.body.append(self.head)
        self.moves = []

    def draw_snake(self):
        for cube in self.body:
            cube.draw_cube(self.window)

    def move_snake(self):
        keys = py.key.get_pressed()
        change = False
        if keys[py.K_UP]:
            dir_x = 0
            dir_y = -1
            change = True
        elif keys[py.K_DOWN]:
            dir_x = 0
            dir_y = 1
            change = True
        elif keys[py.K_RIGHT]:
            dir_x = 1
            dir_y = 0
            change = True
        elif keys[py.K_LEFT]:
            dir_x = -1
            dir_y = 0
            change = True

        if change:
            self.head.dir_x = dir_x
            self.head.dir_y = dir_y
        self.moves.insert(0, (self.head.dir_x, self.head.dir_y))


    def update_snake(self):
        for i in range(len(self.body)):
            self.body[i].dir_x = self.moves[i][0]
            self.body[i].dir_y = self.moves[i][1]

        for cube in self.body:
            cube.pos_x += cube.dir_x * size
            cube.pos_y += cube.dir_y * size

    def add_cube(self):
        past_cube = self.body[len(self.body) - 1]
        x = past_cube.pos_x - (past_cube.dir_x * size)
        y = past_cube.pos_y - (past_cube.dir_y * size)
        self.body.append(Cube(x, y, past_cube.dir_x, past_cube.dir_y))
        self.moves.append((past_cube.dir_x, past_cube.dir_y))


def generate_snack(snake):
    # draw the snack, return the position
    rand_x = int
    rand_y = int
    try_again = True
    while try_again:
        try_again = False
        rand_x = randint(0, grid_length - 1) * size
        rand_y = randint(0, grid_length - 1) * size
        for cube in snake:
            if rand_x == cube.pos_x or rand_y == cube.pos_y:
                try_again = True
                break
    return rand_x, rand_y


def draw_snack(window, x, y):
    py.draw.rect(window, (0, 255, 0), (x, y, size, size))


def display_messagebox(score, best_score):
    window = tk.Tk()
    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
    window.withdraw()

    result = messagebox.askokcancel('Score', f'Your score was {score} \n Your highscore is {best_score}')

    window.deiconify()
    window.destroy()
    window.quit()
    return result


def main():
    global width
    global grid_length
    global size

    py.init()
    window = py.display.set_mode((width, width))
    py.display.set_caption('Snake')
    best_score = 0

    while True:
        snake = Snake(window)
        snack_x, snack_y = generate_snack(snake.body)
        clock = py.time.Clock()

        play = True
        while play:
            py.time.delay(40)
            clock.tick(10)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return

            window.fill((0, 0, 0))

            snake.move_snake()
            snake.update_snake()
            snake.draw_snake()
            draw_snack(window, snack_x, snack_y)

            if snake.head.pos_x == snack_x and snake.head.pos_y == snack_y:
                snake.add_cube()
                snack_x, snack_y = generate_snack(snake.body)

            if snake.head.pos_x < 0 or snake.head.pos_x > width - size\
                    or snake.head.pos_y < 0 or snake.head.pos_y > width - size:
                play = False

            x_head = snake.body[0].pos_x
            y_head = snake.body[0].pos_y
            for cube in snake.body:
                if cube.pos_x == x_head and cube.pos_y == y_head and snake.body.index(cube) != 0:
                    play = False
                    break

            py.display.update()

        score = len(snake.body)
        if score > best_score:
            best_score = score

        if not display_messagebox(score, best_score):
            py.quit()
            return


if __name__ == '__main__':
    main()
