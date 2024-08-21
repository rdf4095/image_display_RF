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
08-21-2024  Handle list of 2 images.
"""
"""
TODO: - copy the logic for re-configuring canvas size to image_canvas_dyn.py.
"""

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

import canvas_ui as cnv

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()
custui = SourceFileLoader("custui", "../../development/python/pandas_02/rf_custom_ui.py").load_module()

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
    if num_items >= 3:
        newpaths.insert(1, paths[indices_smallest[0]])
        if num_items >= 4:
            newpaths.insert(2, paths[indices_smallest[1]])

    return newpaths


def align_images():
    v = vertical_align.get()
    h = horizontal_align.get()
    # cnv.get_posn(viewport1, heights, widths, h, v)
    set_all_posn(v, h)


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

"""
image_paths = ['four moods_2.png',      tall
               'forest of death_1.png', tall
               'parapsycho_1.png',      wide
               'four moods_1.png',      wide
               ]
"""
# image_paths = ['four moods_2.png',
#                'forest of death_1.png',
#                'parapsycho_1.png',
#                'four moods_1.png',
#                ]
image_paths = ['forest of death_1.png',
               'parapsycho_1.png'
               ]
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

# button_fr_1 = ttk.Frame(ui_fr, relief='raised')

# but_top_left = ttk.Button(button_fr_1,
#                           text='top-left',
#                           command=lambda v='top', h='left': set_all_posn(v, h),
#                           style="MyButton1.TButton")
# but_top_left.pack(side='left', padx=5, pady=5)

# but_top_center = ttk.Button(button_fr_1,
#                            text='top-center',
#                            command=lambda v='top', h='center': set_all_posn(v, h),
#                            style="MyButton1.TButton")
# but_top_center.pack(side='left', padx=5, pady=5)

# but_top_right = ttk.Button(button_fr_1,
#                            text='top-right',
#                            command=lambda v='top', h='right': set_all_posn(v, h),
#                            style="MyButton1.TButton")
# but_top_right.pack(side='left', padx=5, pady=5)

# but_bottom_left = ttk.Button(button_fr_1,
#                              text='bottom-left',
#                              command=lambda v='bottom', h='left': set_all_posn(v, h),
#                              style="MyButton1.TButton")
# but_bottom_left.pack(side='left', padx=5, pady=5)

# but_bottom_center = ttk.Button(button_fr_1,
#                               text='bottom-center',
#                               command=lambda v='bottom', h='center': set_all_posn(v, h),
#                               style="MyButton1.TButton")
# but_bottom_center.pack(side='left', padx=5, pady=5)

# but_bottom_right = ttk.Button(button_fr_1,
#                              text='bottom-right',
#                              command=lambda v='bottom', h='right': set_all_posn(v, h),
#                              style="MyButton1.TButton")
# but_bottom_right.pack(side='right', padx=5, pady=5)

# button_fr_1.pack(side='top')

# button_fr_1.update()

# canv_static1.create_rectangle(0, 0, viewport1['w']-1, viewport1['h']-1)
# canv_static1.create_rectangle(viewport1['w'], 0, viewport1['w']-1, viewport1['h']-1)
# canv_static1.create_rectangle(0, viewport1['h'], viewport1['w']-1, viewport1['h']-1)
# canv_static1.create_rectangle(viewport1['w'], viewport1['h'], viewport1['w']-1, viewport1['h']-1)
"""
vp_wd_z = 149 = 150 - 1
vp_wd   = 150
vp_ht_z = 199 = 200 - 1
vp_ht   = 200
vp_htx2 = 300 = 150 * 2
vp_wdx2_z = 399 = (200 * 2) - 1
"""
width_pixels = viewport1['w']-1
height_pixels = viewport1['h']-1
gutter = viewport1['gutter']
v1_LU = 0, 0
v1_RL = width_pixels, height_pixels
v2_LU = width_pixels + 1 + gutter, 0, 
v2_RL = 0, 0
v3_LU = 0, 0
v3_RL = 0, 0
v4_LU = 0, 0
v4_RL = 0, 0
canv_static1.create_rectangle(0, 0, 199, 149)
canv_static1.create_rectangle(200+10, 0, 399+10, 149)
canv_static1.create_rectangle(0, 150+10, 199, 300+10)
canv_static1.create_rectangle(200+10, 150+10, 399+10, 300+10)

"""
example:
line_x_fr = custui.FramedCombo(plotting_main,
                               cb_values=data_columns,
                               display_name=x_text,
                               name='line_x',
                               var=line_data_x,
                               posn=[0,1])
"""
verticals = ['top', 'center', 'bottom']
horizontals = ['left', 'center', 'right']
vertical_align = tk.StringVar()
horizontal_align = tk.StringVar()

v_choice = custui.FramedCombo(ui_fr,
                              cb_values=verticals,
                              display_name='vertical',
                              name='v_choice',
                              var=vertical_align,
                              posn=[0,0])
h_choice = custui.FramedCombo(ui_fr,
                              cb_values=horizontals,
                              display_name='horizontal',
                              name='h_choice',
                              var=horizontal_align,
                              posn=[0,1])


# geometry: w h x y
# print(f'button_fr_1 geometry: {button_fr_1.winfo_geometry()}')
# print(f'button_fr_1 w,h: {button_fr_1.winfo_width()}, {button_fr_1.winfo_height()}')

but_align_images = ttk.Button(ui_fr,
                              text="realign",
                              command=align_images,
                              style="MyButton1.TButton")
but_align_images.grid(row=1, column=0)
but_reset_size = ttk.Button(ui_fr,
                            text="reset window size",
                            command=lambda dims=default_dims: reset_window_size(dims),
                            style="MyButton1.TButton")
# but_reset_size.pack(side='top', padx=5, pady=10)
but_reset_size.grid(row=2, column=0)

# or: command=root.destroy
btnq = ttk.Button(ui_fr,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
# btnq.pack(side="top", fill='x', padx=5, pady=5)
btnq.grid(row=3, column=0)

ui_fr.pack(side='top', ipadx=10, ipady=10, padx=5, pady=5)
ui_fr.update()

# print(f'canv_static1 h,w: {canv_static1.winfo_height()}, {canv_static1.winfo_width()}')
# print(f'ui_fr h,w: {ui_fr.winfo_height()}, {ui_fr.winfo_width()}')
# print(f'lab h,w: {lab.winfo_height()}, {lab.winfo_width()}')

total_ht = lab.winfo_height() + canv_static1.winfo_height() + ui_fr.winfo_height() + 50
total_wd = max(lab.winfo_width(), canv_static1.winfo_width(), ui_fr.winfo_width())
default_dims = f'{total_wd}x{total_ht}'

root.minsize(total_wd, total_ht)

if __name__ == "__main__":
    root.mainloop()
