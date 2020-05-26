import GameWindow
import tkinter as tk


window = tk.Tk()
window.title('Tic Tac Toe')
window.geometry('480x480+100+100')
window.configure(background='white')

title_frame = tk.Frame(window).place(width=240, height=100)
title_label = tk.Label(title_frame, text='Tic Tac Toe Game!!!')
title_label.pack()

window.mainloop()
