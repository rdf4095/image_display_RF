"""
program: image_canvas_dyn.py

purpose: Display an image in a canvas, and allow resizing
         as window dimensions change.

comments: 

author: Russell Folks

history:
-------
01-31-2024  creation
02-08-2024  Make structure similar to image_disp_1canvas.py.
02-21-2024  Use type-hinting in function signatures.
02-21-2024  Structure the code like image_disp_1canvas.py (non-resizable canvas).
08-26-2024  Added code (disabled) to scale the canvas to smaller images.
08-27-2024  Update the handling of geometry: calculate size of canvas and UI.
            Reorganize code, using image_canvas_static.py as a model.
10-22-2024  Minor whitespace and other order-of-steps changes for consistency
            with image_canvas_static.py.
11-27-2024  Remove unused function(s) and paramter(s). Use ThemedTk for widgets.
"""
"""
TODO: - 
"""
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from ttkthemes import ThemedTk
from PIL import Image

# import canvas_ui as cnv

sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()
cnv_ui = SourceFileLoader("cnv", "../canvas/canvas_ui.py").load_module()

def reset_window_size(dims: str) -> None:
    # print(f'geometry: {root.geometry()}')
    root.geometry(dims)
    # print(f'geometry: {root.geometry()}')


# app window
root = ThemedTk()
root.resizable(True, True)
root.title("dynamic canvas, ttk, pack")

default_dims = ""
style2 = sttk.create_styles()

viewport = {'w': 400, 'h': 300, 'gutter': 10}
my_pady = 10

lab = ttk.Label(root, text="image in a resizable canvas",
                style="MyLabel.TLabel")
lab.pack(pady=my_pady)

image_path = "images/parapsycho_1.png"
im1 = Image.open(image_path)
imsize = cnv_ui.init_image_size(im1, viewport)

canv_dyn1 = tk.Canvas(root,
                      width=viewport['w'],
                      height=viewport['h'],
                      highlightthickness=0,
                      background='green')
canv_dyn1.pack(fill='both', expand=True)

params = cnv_ui.calc_resize_to_vp(viewport, im1)
print(params)

canv_dyn1.configure(width=viewport['w'], height=viewport['h'])
canv_dyn1.bind('<Configure>', lambda ev, im=im1, canv=canv_dyn1: cnv_ui.resize_images(ev, im, canv))
canv_dyn1.addtag_all("all")

# UI elements ----------
ui_fr = ttk.Frame(root, relief='groove')

but_reset_size = ttk.Button(ui_fr, text="reset image size",
                            command=lambda dims=default_dims: reset_window_size(dims),
                            style="MyButton1.TButton")
but_reset_size.pack(padx=5, pady=10)

ui_fr.pack(side='top', ipadx=10, ipady=10, padx=5, pady=5)
ui_fr.update()

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.pack(side="top")#, fill='x', padx=10)

# show some layout dimensions
# ----
# print(f'canv_static1 h,w: {canv_static1.winfo_height()}, {canv_static1.winfo_width()}')
# print(f'ui_fr h,w: {ui_fr.winfo_height()}, {ui_fr.winfo_width()}')
# print(f'lab h,w: {lab.winfo_height()}, {lab.winfo_width()}')

total_ht = canv_dyn1.winfo_height() + ui_fr.winfo_height()
total_wd = max(lab.winfo_width(), canv_dyn1.winfo_width(), ui_fr.winfo_width())
default_dims = f'{total_wd}x{total_ht}'

root.minsize(total_wd, total_ht)

if __name__ == "__main__":
    root.mainloop()
