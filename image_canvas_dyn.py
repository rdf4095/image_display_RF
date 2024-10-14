"""
program: image_canvas_dyn.py

purpose: Display an image in a canvas, and allow resizing
         as window dimensions change.

comments: based on image_disp_ncanvas.py

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
"""
"""
TODO: - 
"""

from PIL import Image
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

import canvas_ui as cnv

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def reset_window_size(dims: str) -> None:
    print(f'geometry: {root.geometry()}')
    root.geometry(dims)
    print(f'geometry: {root.geometry()}')

def resize_root(ev: tk.Event,
                  im: object,
                  canv: object) -> None:
    params1 = cnv.calc_resize(ev, im)
    print(f'params1: {params1}')


# app window
default_dims = ""

root = tk.Tk()
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

imsize = cnv.init_image_size(im1, viewport)
print(f'imsize: {imsize}')

canv_dyn1 = tk.Canvas(root,
                      width=viewport['w'],
                      height=viewport['h'],
                      highlightthickness=0,
                      background='green')
canv_dyn1.pack(fill='both', expand=True)

params = cnv.calc_resize_to_vp(viewport, im1)
print(params)

canv_dyn1.configure(width=400, height=300)

canv_dyn1.bind('<Configure>', lambda ev, im=im1, canv=canv_dyn1: resize_images(ev, im, canv))

canv_dyn1.addtage_all("all")

# Scale the canvas to hold the images with no extra space.
# This is to handle future situations like:
#   1) all imgs smaller than the viewport width, with no re-scaling
#   2) all imgs smaller than the viewport height, with no re-scaling
#   3) after re-scaling, all img widths or heights smaller than corresponding
#      canvas dimension.
# In all 3 cases, remove "extra" canvas width or height. The purpose is to allow
# other objects to be positioned closer to the canvas.

# canvas_config_ht = max(sum(heights[0::2]), sum(heights[1::2])) + viewport['gutter']
# print(f'final gutter: {viewport1["gutter"]}')
# canvas_reconfig['h'] = max(sum(heights[0::2]) + viewport1['gutter'],
#                            sum(heights[1::2]) + viewport1['gutter'])
# print(f'canvas_reconfig h: {canvas_reconfig["h"]}')
# canvas_reconfig['h'] += (viewport1['gutter'])
# print(f'canvas_reconfig h: {canvas_reconfig["h"]}')

# print()
# print(f"static canv reconfig w,h: {canvas_reconfig['w']}, {canvas_reconfig['h']}")

# canv_static1.configure(width=canvas_reconfig['w'], height=canvas_reconfig['h'])

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
btnq.pack(side="top", fill='x', padx=10)

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
