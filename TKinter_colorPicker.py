import tkinter as tk
from tkinter import colorchooser

def pick_color():
    color = colorchooser.askcolor(title="Pick a color")
    if color[1]:  # If a color is selected
        root.clipboard_clear()
        root.clipboard_append(color[1])  # copy the hex value to the clipboard
        color_label.config(text=f"Selected color: {color[1]}", bg=color[1])

root = tk.Tk()
root.title("Color Picker")

btn = tk.Button(root, text="Pick a Color", command=pick_color)
btn.pack(pady=20)

color_label = tk.Label(root, text="Selected color will be shown here.", padx=10, pady=10)
color_label.pack(pady=20)

root.mainloop()
