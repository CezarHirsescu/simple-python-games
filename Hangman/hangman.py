import random
import tkinter as tk
from tkinter import font
# Import to create a command with a parameter for buttons
from functools import partial


def get_random_word():
    word_list = []
    with open('words.txt', 'r') as word_file:
        for txt_word in word_file:
            if 4 < len(txt_word) < 14:
                word_list.append(txt_word.strip('\n'))

    return word_list[random.randint(0, len(word_list) - 1)]


def draw_gallows():
    canvas.create_line(60, 350, 300, 350, width=2)
    canvas.create_line(105, 350, 105, 20, width=2)
    canvas.create_line(105, 20, 240, 20, width=2)
    canvas.create_line(240, 20, 240, 50, width=2)
    canvas.create_line(105, 85, 170, 20, width=2)
    canvas.create_line(105, 95, 180, 20, width=2)


def draw_body_part(mistakes):
    if mistakes <= 1:
        canvas.create_oval(209, 50, 269, 110, width=2)
    elif mistakes <= 2:
        canvas.create_line(240, 110, 240, 260, width=2)
    elif mistakes <= 3:
        canvas.create_line(240, 180, 190, 120, width=2)
    elif mistakes <= 4:
        canvas.create_line(240, 180, 290, 120, width=2)
    elif mistakes <= 5:
        canvas.create_line(240, 260, 200, 330, width=2)
    elif mistakes <= 6:
        canvas.create_line(240, 260, 280, 330, width=2)


def draw_dashes(word, x):
    for i in word:
        canvas.create_line(x, 260, x + 25, 260)
        x += 36


def draw_letters(word, letter, x):
    helv20 = font.Font(family='Helvetica', size=20, weight='bold')
    for l in word:
        if letter == l:
            canvas.create_text(x + 10, 249, text=letter, font=helv20)
        x += 36


def end_condition(has_won):

    def new_game_button_command():
        end_window.destroy()
        new_game()

    end_window = tk.Tk()
    end_window.geometry('250x180+400+200')
    end_window.title('Game Over!')
    end_message_frame = tk.Frame(end_window)
    end_message_frame.grid(row=0, column=0)
    end_button_frame = tk.Frame(end_window)
    end_button_frame.grid(row=1, column=0)

    new_game_button = tk.Button(end_button_frame, text='Play new game',
                                command=new_game_button_command)
    new_game_button.grid(row=0, column=0)

    if has_won:
        end_message = tk.Label(end_message_frame,
                               text='Congratulations!! You won!!!', font=helv17)
    else:
        end_message = tk.Label(end_message_frame,
                               text=f'You Lost! The word was "{word}"', font=helv17)
    end_message.pack()

    end_window.mainloop()


def new_game():
    global word
    global correct_guesses
    global mistakes
    global x
    global total_guesses
    global canvas

    canvas.destroy()
    canvas = tk.Canvas(main_window, background='white', width=800, height=360)
    canvas.grid(row=0, column=0)
    draw_gallows()
    word = get_random_word()
    correct_guesses = []
    mistakes = 0
    total_guesses = []

    x = (700 // len(word)) + 260
    draw_dashes(word, x)


def key_input(char):
    global word
    global correct_guesses
    global mistakes
    global x
    global total_guesses

    guess = char

    if guess not in total_guesses:
        for letter in word:
            if guess == letter:
                correct_guesses.append(guess)
                draw_letters(word, guess, x)
        if guess not in word:
            mistakes += 1
            draw_body_part(mistakes)
    total_guesses.append(guess)

    if mistakes == 6:
        end_condition(has_won=False)
    elif len(correct_guesses) == len(word):
        end_condition(has_won=True)


# creating the window, canvas and buttons
main_window = tk.Tk()
main_window.title('Hangman')
main_window.geometry('800x580+240+30')
main_window.resizable(False, False)

canvas = tk.Canvas(main_window, background='white', width=800, height=360)
canvas.grid(row=0, column=0)


keyboard_panel = tk.Frame(main_window)
keyboard_panel.grid(row=1, column=0)

helv17 = font.Font(family='Helvetica', size=17, weight='bold')
helv12 = font.Font(family='Helvetica', size=12)


for i in range(ord('a'), ord('z') + 1):
    if i < ord('j'):
        column = ord('a')
        row = 0
    elif i < ord('s'):
        column = ord('j')
        row = 1
    else:
        column = ord('s')
        row = 2

    # the partial keyword allows you to have a command with a parameter
    button = tk.Button(keyboard_panel, text=chr(i), font=helv17,
                       command=partial(key_input, chr(i)), width=4)
    button.grid(row=row, column=i - column, padx=10, pady=10)

reset_button = tk.Button(keyboard_panel, text='New Game', font=helv12, command=new_game)
reset_button.grid(row=2, column=8)

draw_gallows()

word = get_random_word()
correct_guesses = []
mistakes = 0
total_guesses = []

x = (700 // len(word)) + 260
draw_dashes(word, x)

main_window.mainloop()
