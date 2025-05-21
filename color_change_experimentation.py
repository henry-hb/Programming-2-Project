import tkinter as tk

def change_color(dummy_e):
    canvas.configure(bg='cyan')

root = tk.Tk()
canvas = tk.Canvas(root, bg='red')
canvas.pack()
canvas.bind('<1>', change_color)

root.mainloop()