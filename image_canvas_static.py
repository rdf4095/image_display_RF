"""
program: image_canvas_static.py

purpose: Display up to 4 images in one canvas, with constant size.

comments: Image viewports are set to a height-width ratio of 4:3.

author: Russell Folks

history:
-------
07-24-2024  creation
07-30-2024  Add buttons to change image placement.
08-03-2024  Combine image-move functions into one fxn.
08-06-2024  Calculate the window geometry needed after images are displayed, and
            use this to control window minimum and reset.
08-08-2024  Test canvas: actual size is slightly larger than configured size.
08-14-2024  Add function find_largest_objs to re-order the list of image paths
            according to image size.
"""
"""
TODO: - copy the logic for re-configuring canvas size to image_canvas_dyn.py.
      - test find_largest_objs for list of 3 and list of 2
"""

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

import canvas_ui as cnv

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

def reset_window_size(dims: str) -> None:
    root.geometry(dims)


def set_top_left():
    """Move an image to the top-left of the canvas."""
    print('in set_top_left')
    posn = cnv.get_posn(viewport1, heights, widths, 'left', 'top')
    canv_static1.moveto(imid_list[0], posn[0].x, posn[0].y)


def set_all_posn(vert, horiz):
    posn = cnv.get_posn(viewport1, heights, widths, horiz, vert)
    
    canv_static1.moveto(1, posn[0].x, posn[0].y)
    canv_static1.moveto(2, posn[1].x, posn[1].y)
    if len(heights) > 2:
        canv_static1.moveto(3, posn[2].x, posn[2].y)
    if len(heights) > 3:
        canv_static1.moveto(4, posn[3].x, posn[3].y)


def find_largest_objs(dims: list, paths: list) -> list:
    """Find the 2 images of greatest dimension.
    
    dims specifies the dimension, as width or height.
    This function should only be called if len(dims) > 2.
    For 1 or 2 images, there's little-to-no choice of display arrangement.
    """
    num_items = len(dims)
    sort_w = sorted(dims)
    largest_2 = sort_w[num_items - 2:]
    newpaths = []
    
    w1 = dims.index(largest_2[0])

    # Mask the location of the first "large" image, to find the second.
    dims_mod = dims.copy()
    dims_mod[w1] = -1
    w2 = dims_mod.index(largest_2[1])

    indices_all = [*range(len(dims))]

    indices_largest = [w1, w2]

    indices_smallest = [n for n in indices_all if n not in indices_largest]

    newpaths = [paths[w1], paths[w2]]
    newpaths.insert(1, paths[indices_smallest[0]])
    print(f'num_items: {num_items}')
    if num_items > 3:
        newpaths.insert(2, paths[indices_smallest[1]])

    return newpaths


# app window
default_dims = ""

root = tk.Tk()
root.resizable(1, 1)
root.title("image, ttk, pack")

style2 = styles_ttk.CreateStyles()

viewport1 = {'w': 200, 'h': 150, 'gutter': 10}
# viewport1 = {'w': 400, 'h': 300, 'gutter': 10}
my_pady = 10

canvas_reconfig = {'w': viewport1['w'] * 2 + viewport1['gutter'],
                   'h': viewport1['h'] * 2 + viewport1['gutter']}

lab = ttk.Label(root, text="up to 4 fixed-size images",
                style="MyLabel.TLabel")
lab.pack(pady=my_pady)

# image_paths = ['four moods_2.png',
#                'forest of death_1.png',
#                'parapsycho_1.png',
#                'four moods_1.png',
#                ]
image_paths = ['forest of death_1.png',
               'parapsycho_1.png',
               'four moods_1.png',
               ]
"""
image_paths = ['four moods_2.png',      tall
               'forest of death_1.png', tall
               'parapsycho_1.png',      wide
               'four moods_1.png',      wide
               ]
"""
myPhotoImages = []
heights = []
widths = []

# print('static images, native w,h and resized w,h:')
# print(f'starting path list: {image_paths}')
# print()
# print('sizes of 4 ims:')

for i, n in enumerate(image_paths):
    im_path = 'images/' + n
    im = Image.open(im_path)
    imsize = cnv.init_image_size(im, viewport1)
    heights.append(imsize['h'])
    widths.append(imsize['w'])
#     im_resize = im.resize((imsize['w'], imsize['h']))
#     im_tk = ImageTk.PhotoImage(im_resize)
#     myPhotoImages.append(im_tk)
#     print(f"  im {i} ({n}), {widths[i]}, {heights[i]}")
# for i, n in enumerate(image_paths):
#     im_path = 'images/' + n
#     im = Image.open(im_path)
#     imsize = cnv.init_image_size(im, viewport1)
    # heights.append(imsize['h'])
    # widths.append(imsize['w'])

    # im_resize = im.resize((imsize['w'], imsize['h']))
    # im_tk = ImageTk.PhotoImage(im_resize)
    # myPhotoImages.append(im_tk)
    # print(f"  im {i} ({n}), {widths[i]}, {heights[i]}")

"""
re-order the images to position them for display according to this logic:
display order:
im_0  im_1
im_2  im_3

using widths, shapes:
-- |
|  --

using heights, shapes:
|  --
-- |  
"""
new_image_paths = find_largest_objs(widths, image_paths)
print(f'reordered path list: {new_image_paths}')

heights = []
widths = []

for i, n in enumerate(new_image_paths):
    im_path = 'images/' + n
    im = Image.open(im_path)
    imsize = cnv.init_image_size(im, viewport1)
    heights.append(imsize['h'])
    widths.append(imsize['w'])
    im_resize = im.resize((imsize['w'], imsize['h']))
    im_tk = ImageTk.PhotoImage(im_resize)
    myPhotoImages.append(im_tk)
    # print(f"  im {i} ({n}), {widths[i]}, {heights[i]}")




canv_static1 = tk.Canvas(root, background="green")
canv_static1.configure(width=canvas_reconfig['w'], height=canvas_reconfig['h'],
                       borderwidth=0)

posn = cnv.get_posn(viewport1, heights, widths, 'left', 'top')
# print()
# print('positions of 4 ims:')
# print(f"  im 0: {posn[0].x}, {posn[0].y}")
# print(f"  im 1: {posn[1].x}, {posn[1].y}")
# print(f"  im 2: {posn[2].x}, {posn[2].y}")
# print(f"  im 3: {posn[3].x}, {posn[3].y}")

imid_list = []
# for i, n in enumerate(image_paths):
for i, n in enumerate(new_image_paths):
    tagname = "tag_im" + str(i)
    imid = canv_static1.create_image(posn[i].x, posn[i].y, anchor=tk.NW, image=myPhotoImages[i],
                                  tag = tagname)
    imid_list.append(imid)

canv_static1.pack(ipadx=0, ipady=0, pady=10)
canv_static1.update()
# print(f'canv conf w,h: {canv_static1["width"]}, {canv_static1["height"]}')
# print(f'canv  req w,h: {canv_static1.winfo_reqwidth()}, {canv_static1.winfo_reqheight()}')
# print(f'canv      w,h: {canv_static1.winfo_width()}, {canv_static1.winfo_height()}')

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

button_fr_1 = ttk.Frame(ui_fr, relief='raised')

but_top_left = ttk.Button(button_fr_1,
                          text='top-left',
                          command=lambda v='top', h='left': set_all_posn(v, h),
                          style="MyButton1.TButton")
but_top_left.pack(side='left', padx=5, pady=5)

but_top_center = ttk.Button(button_fr_1,
                           text='top-center',
                           command=lambda v='top', h='center': set_all_posn(v, h),
                           style="MyButton1.TButton")
but_top_center.pack(side='left', padx=5, pady=5)

but_top_right = ttk.Button(button_fr_1,
                           text='top-right',
                           command=lambda v='top', h='right': set_all_posn(v, h),
                           style="MyButton1.TButton")
but_top_right.pack(side='left', padx=5, pady=5)

but_bottom_left = ttk.Button(button_fr_1,
                             text='bottom-left',
                             command=lambda v='bottom', h='left': set_all_posn(v, h),
                             style="MyButton1.TButton")
but_bottom_left.pack(side='left', padx=5, pady=5)

but_bottom_center = ttk.Button(button_fr_1,
                              text='bottom-center',
                              command=lambda v='bottom', h='center': set_all_posn(v, h),
                              style="MyButton1.TButton")
but_bottom_center.pack(side='left', padx=5, pady=5)

but_bottom_right = ttk.Button(button_fr_1,
                             text='bottom-right',
                             command=lambda v='bottom', h='right': set_all_posn(v, h),
                             style="MyButton1.TButton")
but_bottom_right.pack(side='right', padx=5, pady=5)

button_fr_1.pack(side='top')

button_fr_1.update()
# geometry: w h x y
# print(f'button_fr_1 geometry: {button_fr_1.winfo_geometry()}')
# print(f'button_fr_1 w,h: {button_fr_1.winfo_width()}, {button_fr_1.winfo_height()}')

but_reset_size = ttk.Button(ui_fr,
                            text="reset window size",
                            command=lambda dims=default_dims: reset_window_size(dims),
                            style="MyButton1.TButton")
but_reset_size.pack(side='top', padx=5, pady=10)


# or: command=root.destroy
btnq = ttk.Button(ui_fr,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.pack(side="top", fill='x', padx=5, pady=5)

ui_fr.pack(side='top', padx=5, pady=5)
ui_fr.update()

# print(f'canv_static1 h,w: {canv_static1.winfo_height()}, {canv_static1.winfo_width()}')
# print(f'ui_fr h,w: {ui_fr.winfo_height()}, {ui_fr.winfo_width()}')
# print(f'lab h,w: {lab.winfo_height()}, {lab.winfo_width()}')

total_ht = lab.winfo_height() + canv_static1.winfo_height() + ui_fr.winfo_height() + 50
total_wd = max(lab.winfo_width(), canv_static1.winfo_width(), ui_fr.winfo_width())
default_dims = f'{total_wd}x{total_ht}'
# print(f'total_wd, total_ht: {total_wd}, {total_ht}')
root.minsize(total_wd, total_ht)


if __name__ == "__main__":
    root.mainloop()
