from GameWindow import GameWindow
import tkinter as tk
from tkinter import font


def play_tic_tac_toe(ai):
    """ Command function for the buttons to play one round of tic tac toe.
        Each time a game is played, a new instance of GameWindow should
        be created.
    """
    game_window = GameWindow()
    if ai == 0:
        game_window.run()
    elif ai == 1:
        game_window.run(game_window.easy_ai)
    elif ai == 2:
        game_window.run(game_window.hard_ai)


# Creating the main window
main_window = tk.Tk()
main_window.title('Tic Tac Toe')
main_window.geometry('480x360+100+100')
main_window.configure(background='white')
main_window.resizable(False, False)

# fonts
helv20 = font.Font(family='Helvetica', size=20, weight='bold', underline=True)
helv10 = font.Font(family='Helvetica', size=10, weight='bold')

# Title label that says Tic Tac Toe Game!!!
title_frame = tk.Frame(main_window, background='white')
title_frame.place(x=240, y=50, anchor='center')
title_label = tk.Label(title_frame, text='Tic Tac Toe Game!!!', font=helv20, background='white')
title_label.pack()

# Canvas purely for visual reasons, its like a picture
canvas = tk.Canvas(main_window, width=120, height=120, background='white')
canvas.place(x=240, y=140, anchor='center')
for i in range(1, 3):
    canvas.create_line(0, 40 * i, 120, 40 * i, width=2)
    canvas.create_line(40 * i, 0, 40 * i, 120, width=2)
canvas.create_line(5, 5, 35, 35, width=2)
canvas.create_line(35, 5, 5, 35, width=2)
canvas.create_oval(45, 45, 75, 75, width=2)

button_frame = tk.Frame(main_window, background='white')
button_frame.place(y=260, x=240, anchor='center')
multi_player_button = tk.Button(button_frame, text='Multi Player', font=helv10, command=lambda: play_tic_tac_toe(0))
multi_player_button.grid(row=0, column=0, padx=15)
easy_player_button = tk.Button(button_frame, text='Easy Single Player', font=helv10, command=lambda: play_tic_tac_toe(1))
easy_player_button.grid(row=0, column=1, padx=15)
hard_player_button = tk.Button(button_frame, text='Hard Single Player', font=helv10, command=lambda: play_tic_tac_toe(2))
hard_player_button.grid(row=0, column=2, padx=15)


main_window.mainloop()
