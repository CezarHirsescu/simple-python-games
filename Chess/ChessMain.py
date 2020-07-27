""" The ChessMain class is responsible for getting user input and
displaying the state of the game (the frontend).
"""

import pygame as py
import ChessEngine
import os
import tkinter as tk
from tkinter import messagebox

# declaring constants for visuals
py.init()
WIDTH = HEIGHT = 520
GRID_LENGTH = 8
SQR_SIZE = WIDTH // GRID_LENGTH
MAX_FPS = 15
IMAGES = {}


# load the images into pygame, is only done once
def load_images():
    for file in os.listdir('images'):
        name = file.split('.')[0]
        IMAGES[name] = py.transform.scale(py.image.load('images\\' + file),
                                          (SQR_SIZE, SQR_SIZE))


# main method for the program, will handle user input and updating the screen
def main():
    screen = py.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    py.display.set_caption('Chess')
    clock = py.time.Clock()
    gamestate = ChessEngine.GameState()
    valid_moves = gamestate.get_valid_moves()
    load_images()
    mouse_history = []  # a list containing the players click[(x1, y1), (x2, y2)]
    # first tuple is the click that selected the piece,
    # second tuple is the click that placed the following piece
    show_suggested_moves = []  # stores possible moves for a given piece

    run = True
    while run:

        for event in py.event.get():

            if event.type == py.QUIT:  # close window event handler
                run = False
                break
            elif event.type == py.MOUSEBUTTONDOWN:  # mouse-clicked event handler
                position = py.mouse.get_pos()
                x = position[0] // SQR_SIZE
                y = position[1] // SQR_SIZE
                sq_selected = (x, y)

                # because gameboard is a list, x and y are flipped
                # (x, y) becomes [y][x]
                # if the player is trying to move an empty square or an opponent piece
                turn_color = 'w' if gamestate.whiteTurn else 'b'
                if not (len(mouse_history) == 0 and
                        (gamestate.gameboard[y][x] == '--' or gamestate.gameboard[y][x][0] != turn_color)):
                    mouse_history.append(sq_selected)  # append for 1st or 2nd click

                if len(mouse_history) == 1:  # the user has selected a piece
                    # add move to show_suggested_moves if the move is for the piece selected by the mouse
                    show_suggested_moves = [move for move in valid_moves if
                                            (move.start_col, move.start_row) == mouse_history[0]]
                else:
                    show_suggested_moves = []

                # if user clicks same square twice
                if len(mouse_history) == 2 and mouse_history[0] == mouse_history[1]:
                    mouse_history = []  # clear mouse history
                elif len(mouse_history) == 2:  # if the user wants to move a piece
                    # create the move to send to the engine
                    move = ChessEngine.Move(mouse_history[0], mouse_history[1],
                                            gamestate.gameboard)

                    # check if the move is good
                    move_is_valid = False
                    for m in valid_moves:
                        if ((m.start_row, m.start_col) == (move.start_row, move.start_col) and
                                (m.end_row, m.end_col) == (move.end_row, move.end_col)):
                            move_is_valid = True
                            break

                    if move_is_valid:  # if the move is valid
                        if move.isPawnPromotion:    # if move is pawn promotion
                            move = ChessEngine.Move(mouse_history[0], mouse_history[1],
                                                    gamestate.gameboard, promotion_piece=choose_pawn_promo())
                        elif ((move.end_row, move.end_col) == gamestate.enpassantSquare
                              and move.pieceMoved[1] == 'P'):   # if move is enpassant
                            move = ChessEngine.Move(mouse_history[0], mouse_history[1], gamestate.gameboard, enpassant_move=True)
                        # if move is castle
                        elif abs(move.end_col - move.start_col) == 2 and move.pieceMoved[1] == 'K':
                            move = ChessEngine.Move(mouse_history[0], mouse_history[1], gamestate.gameboard, is_castle=True)
                        gamestate.move_piece(move)  # move the piece
                        gamestate.enpassantSquare = ()  # reset the enpassant square after every move
                        # create an enpassant square if necessary
                        if move.pieceMoved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
                            step = 1 if move.pieceMoved[0] == 'b' else -1
                            gamestate.enpassantSquare = (move.start_row + step, move.start_col)
                        print(move.get_chess_pos())  # move log
                        mouse_history = []  # clear full move history
                        valid_moves = gamestate.get_valid_moves()
                    else:  # if the user tried an invalid move
                        mouse_history = []  # assume the player has de-selected their piece

            elif event.type == py.KEYDOWN:  # keystroke event handler
                # undo when 'z' or 'u' are pressed
                if event.key == py.K_z or event.key == py.K_u:
                    if gamestate.moveLog[-1].isCastle:  # if the last move is a castle
                        # we need to manually remove the first castleRights.
                        gamestate.castleRightsLog.pop()
                    gamestate.undo_move()   # undo the move
                    # after you undo a move, you must update the current valid moves
                    valid_moves = gamestate.get_valid_moves()
                    mouse_history = []


        draw_gamestate(screen, gamestate, mouse_history, show_suggested_moves)
        clock.tick(MAX_FPS)
        py.display.flip()

        if len(valid_moves) == 0:
            if gamestate.in_check():
                # checkmate
                display_messagebox('Black' if gamestate.whiteTurn else 'White')
            else:
                # stalemate
                display_messagebox()
            # after the game is finished, reset the board and regenerate valid moves
            gamestate.reset_gamestate()
            valid_moves = gamestate.get_valid_moves()


# function to choose a piece for pawn promotion
def choose_pawn_promo():
    window = tk.Tk()
    window.title('Choose which piece you want to promote')
    window.configure(background='white')
    window.resizable(False, False)
    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())

    pieces = [
        ('Queen', 'Q'),
        ('Bishop', 'B'),
        ('Rook', 'R'),
        ('Knight', 'K')
    ]
    v = tk.StringVar()
    v.set('Q')  # set default value

    label = tk.Label(window, text='Select which piece you would like to have the pawn promote to',
                     background='white')
    label.pack(anchor='center')
    for text, piece in pieces:
        tk.Radiobutton(window, text=text, variable=v, value=piece).pack(anchor='w')
    tk.Button(window, text='OK', command=window.destroy).pack(anchor='center')

    tk.mainloop()

    return v.get()


# function to display the end game result as a tkinter messagebox
def display_messagebox(winner=None):
    window = tk.Tk()
    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
    window.withdraw()

    if winner is None:
        messagebox.showinfo('Game Over', "Stalemate: it's a tie")
    else:
        messagebox.showinfo('Game Over', f'Checkmate: {winner} won')

    window.deiconify()
    window.destroy()
    window.quit()


# function to update the screen
def draw_gamestate(screen, gamestate, mouse_history, suggested_moves):
    draw_squares(screen)
    if len(gamestate.moveLog) > 0:
        draw_last_move(screen, gamestate.moveLog[len(gamestate.moveLog) - 1])
    if gamestate.in_check():
        if gamestate.whiteTurn:
            y, x = gamestate.wKLocation
            x, y = x * SQR_SIZE, y * SQR_SIZE
            py.draw.rect(screen, (255, 0, 0), (x, y, SQR_SIZE, SQR_SIZE))
        else:
            y, x = gamestate.bKLocation
            x, y = x * SQR_SIZE, y * SQR_SIZE
            py.draw.rect(screen, (255, 0, 0), (x, y, SQR_SIZE, SQR_SIZE))
    if len(mouse_history) == 1:
        draw_selected_square(screen, mouse_history[0])
        draw_move_suggestions(screen, suggested_moves)
    draw_file_and_rank(screen)
    draw_pieces(screen, gamestate.gameboard)
    py.display.update()


# draws the last move that happened in game
def draw_last_move(screen, move):
    start_y, start_x = move.start_row, move.start_col
    draw_selected_square(screen, (start_x, start_y))
    end_y, end_x = move.end_row, move.end_col
    draw_selected_square(screen, (end_x, end_y), trans=True)


# draws all possible moves for any given piece
def draw_move_suggestions(screen, suggested_moves):
    for move in suggested_moves:  # drawing move suggestions
        y, x = move.end_row, move.end_col
        draw_selected_square(screen, (x, y), trans=True)


# draws the file and rank symbols
def draw_file_and_rank(screen):
    light = (238, 240, 201)  # light beige
    dark = (111, 153, 87)  # brown
    font = py.font.Font('freesansbold.ttf', 14)
    light_color = False

    # rank is 8-1
    rank = '8'
    for i in range(GRID_LENGTH):
        if light_color:
            text = font.render(rank, True, dark, light)
        else:
            text = font.render(rank, True, light, dark)
        light_color = not light_color
        text_rect = text.get_rect()
        text_rect.center = (WIDTH - 6, (i * SQR_SIZE) + 10)
        screen.blit(text, text_rect)
        rank = str(int(rank) - 1)

    # file is A-H
    file = 'A'
    for i in range(GRID_LENGTH):
        if light_color:
            text = font.render(file, True, dark, light)
        else:
            text = font.render(file, True, light, dark)
        light_color = not light_color
        text_rect = text.get_rect()
        text_rect.center = ((i * SQR_SIZE) + 7, HEIGHT - 9)
        screen.blit(text, text_rect)
        file = chr(ord(file) + 1)


# draws the square tiles
def draw_squares(screen):
    light = (238, 240, 201)  # light beige
    dark = (111, 153, 87)  # brown

    white_first = False
    # the top-left square is always light
    for i in range(GRID_LENGTH):
        white_first = False if white_first else True
        for j in range(GRID_LENGTH):
            if white_first:
                py.draw.rect(screen, light, (j * SQR_SIZE, i * SQR_SIZE, SQR_SIZE, SQR_SIZE))
                white_first = False
            else:
                py.draw.rect(screen, dark, (j * SQR_SIZE, i * SQR_SIZE, SQR_SIZE, SQR_SIZE))
                white_first = True


# highlights the square under the piece that the user wants to move
def draw_selected_square(screen, position, trans=False):
    color = (255, 253, 130)
    x, y = position
    x *= SQR_SIZE
    y *= SQR_SIZE
    if trans:  # if the highlight is to be slightly transparent
        s = py.Surface((SQR_SIZE, SQR_SIZE))
        s.set_alpha(140)
        s.fill(color)
        screen.blit(s, (x, y))
    else:  # the highlight is a solid yellow
        py.draw.rect(screen, color, (x, y, SQR_SIZE, SQR_SIZE))


# draws the pieces
def draw_pieces(screen, gameboard):
    # because gameboard is a list, x and y are flipped
    # position (i, j) becomes [j][i]
    for i in range(GRID_LENGTH):  # x
        for j in range(GRID_LENGTH):  # y
            piece = gameboard[j][i]  # [y][x]
            if piece != '--':
                screen.blit(IMAGES[piece],
                            (i * SQR_SIZE, j * SQR_SIZE, SQR_SIZE, SQR_SIZE))


if __name__ == '__main__':
    main()
