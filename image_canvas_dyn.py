"""
program: image_canvas_dyn.py

purpose: Display an image in a canvas, and allow resizing
         as window dimensions change.

comments: based on image_disp_ncanvas.py
kb shortcuts:
    command-L                  - select whole line
    command-D                  - select next instance of selection (to edit both)
    command-SHIFT-ENTER        - create new line and position curson on it

author: Russell Folks

history:
-------
01-31-2024  creation
02-08-2024  Make structure similar to image_disp_1canvas.py.
02-21-2024  Use type-hinting in function signatures.
02-21-2024  Structure the code like image_disp_1canvas.py (non-resizable canvas).
"""
# TODO: could add frame below the canvas, for other widgets,
#       so the root geometry can be calculated accurately.

from PIL import Image
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

import canvas_ui as cnv

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def reset_window_size(dims: str) -> None:
    root.geometry(dims)


# app window
default_dims = "420x460"

root = tk.Tk()
root.geometry(default_dims)
root.minsize(420, 460)
root.resizable(1, 1)
root.title("image, ttk, pack")

style2 = styles_ttk.CreateStyles()

viewport = {'w': 400, 'h': 300, 'gutter': 10}
my_pady = 10

lab = ttk.Label(root, text="resizable image in a canvas",
                style="MyLabel.TLabel")
lab.pack(pady=my_pady)

image_path = "images/parapsycho_1.png"
im1 = Image.open(image_path)

canv_dyn1 = tk.Canvas(root,
                      width=viewport['w'],
                      height=viewport['h'],
                      highlightthickness=0,
                      background='green')

print(f'viewport h, w: {viewport["h"]}, {viewport["w"]}')

# canv_dyn1.bind('<Configure>', lambda ev, im=im1, vp=viewport, canv=canv_dyn1: cnv.resize_images(ev, im, vp, canv))
canv_dyn1.bind('<Configure>', lambda ev, im=im1, canv=canv_dyn1: cnv.resize_images(ev, im, canv))
canv_dyn1.pack(fill='both', expand=True)


# other UI elements ----------
but_reset_size = ttk.Button(root, text="reset image size",
                            command=lambda dims=default_dims: reset_window_size(dims),
                            style="MyButton1.TButton")
but_reset_size.pack(padx=5, pady=10)

# or: command=root.destroy
btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.pack(side="top", fill='x', padx=10)

# print(f'but ht: {but_reset_size.winfo_height()}')
# print(f'butq ht: {btnq.winfo_height()}')
geometry_ht = viewport['h'] + (my_pady * 2) + 130  # other widgets
geometry_wd = 408

default_dims = str(geometry_wd) + 'x' + str(geometry_ht)

if __name__ == "__main__":
    root.mainloop()
