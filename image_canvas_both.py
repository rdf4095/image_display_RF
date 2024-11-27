"""
program: image_canvas_both.py

purpose: Display up to 4 images in one canvas, with constant size.
         Display 1 image in another canvas, resizable by dragging.

comments: 

author: Russell Folks

history:
-------
03-04-2024  creation
10-13-2024  Debug the new approach to sizing static images.
"""
"""
TODO: - add frame below the canvas, for other widgets, so the
        root geometry can be calculated accurately.
      - consider calculating default_dims instead of hardcoding it.
        It's more complex here than in image_canvas_static.py because
        there is more than one canvas here.
"""

import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from PIL import Image, ImageTk

import canvas_ui as cnv

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def reset_window_size(dims: str) -> None:
    root.geometry(dims)


# app window
default_dims = "600x800"

root = tk.Tk()
root.geometry (default_dims)
root.minsize(480, 600)
root.resizable(1, 1)
root.title("image, ttk, pack")

style2 = styles_ttk.CreateStyles()

viewport1 = {'w': 200, 'h': 150, 'gutter': 10}
# viewport2 = {'w': 400, 'h': 300, 'gutter': 10}
my_pady = 10

canvas_reconfig = {'w': viewport1['w'] * 2 + viewport1['gutter'],
                   'h': viewport1['h']}

lab = ttk.Label(root, text="canvas 1: multiple fixed images\n canvas 2: one image, resizable",
                style="MyLabel.TLabel")
lab.pack(pady=my_pady)

image_paths = ['four moods_1.png',
               'forest of death_1.png',
               'four moods_2.png',
               'parapsycho_1.png']
myPhotoImages = []
heights = []
widths = []

print('static images, native w,h and resized w,h:')
for i, n in enumerate(image_paths):
    im_path = 'images/' + n
    im = Image.open(im_path)
    imsize = cnv.init_image_size(im, viewport1)
    heights.append(imsize['h'])
    widths.append(imsize['w'])
         
    im_resize = im.resize((imsize['w'], imsize['h']))
    im_tk = ImageTk.PhotoImage(im_resize)
    myPhotoImages.append(im_tk)
#    print(f"{im.width}, {im.height}")
#    print(f"    {imsize['w']}, {imsize['h']}")
#    print()

canv_static1 = tk.Canvas(root, background = "green")

arrangement = ('left', 'top')
positions = cnv.get_positions(viewport1, widths, heights, arrangement)

imid_list = []
for i, n in enumerate(image_paths):
    tagname = "tag_im" + str(i)
    imid = canv_static1.create_image(positions[i].x, positions[i].y, anchor=tk.NW, image=myPhotoImages[i],
                                  tag = tagname)
    imid_list.append(imid)

canv_static1.pack(pady=10)
canv_static1.update()

# Scale the canvas to hold the images with no extra space.
# canvas_config_ht = max(sum(heights[0::2]), sum(heights[1::2])) + viewport['gutter']
# original:
canvas_reconfig['h'] = max(sum(heights[0::2]) + viewport1['gutter'], sum(heights[1::2]) + viewport1['gutter']) + (viewport1['gutter'] * 2)
# LOCAL:
# canvas_reconfig['h'] = max(sum(heights[0::2]), sum([heights[1], heights[3]]) + viewport1['gutter'])

print(f"static canv reconfig w,h: {canvas_reconfig['w']}, {canvas_reconfig['h']}")

canv_static1.configure(width=canvas_reconfig['w'], height=canvas_reconfig['h'])
# ----------


im_dyn = Image.open('images/' + image_paths[3])

viewport2 = {'w': 400, 'h': 300, 'gutter': 10}

canv_dyn1 = tk.Canvas(root,
                      width=viewport2['w'],
                      height=viewport2['h'],
                      highlightthickness=0,
                      background='green')

print(f'viewport h, w: {viewport2["h"]}, {viewport2["w"]}')

# canv_dyn1.bind('<Configure>', lambda ev, im=im_dyn, vp=viewport2, canv=canv_dyn1: cnv.resize_images(ev, im, vp, canv))
canv_dyn1.bind('<Configure>', lambda ev, im=im_dyn, canv=canv_dyn1: cnv.resize_images(ev, im, canv))
canv_dyn1.pack(fill="both", expand=True)


# ----------
but_reset_size = ttk.Button(root,
                            text="reset window size",
                            command=lambda dims=default_dims: reset_window_size(dims),
                            style="MyButton1.TButton")
but_reset_size.pack(side='top', padx=5, pady=10)

btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.pack(side="top", fill='x', padx=10)

if __name__ == "__main__":
    root.mainloop()
