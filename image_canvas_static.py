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

def reset_window_size(dims: str) -> None:
    root.geometry(dims)


def set_top_left():
    print('in set_top_left')
    posn = cnv.get_posn(viewport1, heights, widths, 'left', 'top')
    canv_static1.moveto(imid_list[0], posn[0].x, posn[0].y)
    canv_static1.moveto(imid_list[1], posn[1].x, posn[1].y)
    canv_static1.moveto(imid_list[2], posn[2].x, posn[2].y)
    canv_static1.moveto(imid_list[3], posn[3].x, posn[3].y)


def set_top_center():
    print('in set_top_center')
    posn = cnv.get_posn(viewport1, heights, widths, 'center', 'top')
    canv_static1.moveto(imid_list[0], posn[0].x, posn[0].y)
    canv_static1.moveto(imid_list[1], posn[1].x, posn[1].y)
    canv_static1.moveto(imid_list[2], posn[2].x, posn[2].y)
    canv_static1.moveto(imid_list[3], posn[3].x, posn[3].y)


def set_bottom_left():
    print('in set_bottom_left')
    posn = cnv.get_posn(viewport1, heights, widths, 'left', 'bottom')
    canv_static1.moveto(imid_list[0], posn[0].x, posn[0].y)
    canv_static1.moveto(imid_list[1], posn[1].x, posn[1].y)
    canv_static1.moveto(imid_list[2], posn[2].x, posn[2].y)
    canv_static1.moveto(imid_list[3], posn[3].x, posn[3].y)


def set_bottom_center_ORIG():
    print('in set_bottom_center')
    posn = cnv.get_posn(viewport1, heights, widths, 'center', 'bottom')
    print()
    print('new positions of 4 ims:')
    print(f"  im 0: {posn[0].x}, {posn[0].y}")
    print(f"  im 1: {posn[1].x}, {posn[1].y}")
    print(f"  im 2: {posn[2].x}, {posn[2].y}")
    print(f"  im 3: {posn[3].x}, {posn[3].y}")
    print()
    
    # move images

    # method 1: move objects using canvas methods
    # --------
    # relative
    # canv_static1.move(id1, 25, 0)

    # absolute
    # canv_static1.moveto(imid_list[0], posn[0].x, posn[0].y)
    # canv_static1.moveto(imid_list[1], posn[1].x, posn[1].y)
    # canv_static1.moveto(imid_list[2], posn[2].x, posn[2].y)
    # canv_static1.moveto(imid_list[3], posn[3].x, posn[3].y)
    canv_static1.moveto(1, posn[0].x, posn[0].y)
    canv_static1.moveto(2, posn[1].x, posn[1].y)
    canv_static1.moveto(3, posn[2].x, posn[2].y)
    canv_static1.moveto(4, posn[3].x, posn[3].y)

    # method 2: recreate the entire canvas
    # --------
    # for j in imid_list:
    #     canv_static1.delete(j)

    # imid_list.clear()

    # for i, n in enumerate(image_paths):
    #     tagname = "tag_im" + str(i)
    #     imid = canv_static1.create_image(posn[i].x, posn[i].y, anchor=tk.NW, image=myPhotoImages[i],
    #                                 tag = tagname)
    #     imid_list.append(imid)


def set_all_posn(vert, horiz):
    posn = cnv.get_posn(viewport1, heights, widths, horiz, vert)
    
    canv_static1.moveto(1, posn[0].x, posn[0].y)
    canv_static1.moveto(2, posn[1].x, posn[1].y)
    canv_static1.moveto(3, posn[2].x, posn[2].y)
    canv_static1.moveto(4, posn[3].x, posn[3].y)


# app window
default_dims = ""

root = tk.Tk()
# root.geometry (default_dims)
# root.minsize(520, 550)
root.resizable(1, 1)
root.title("image, ttk, pack")

style2 = styles_ttk.CreateStyles()

viewport1 = {'w': 200, 'h': 150, 'gutter': 10}
# viewport1 = {'w': 400, 'h': 300, 'gutter': 10}
my_pady = 10

canvas_reconfig = {'w': viewport1['w'] * 2 + viewport1['gutter'],
                   'h': viewport1['h'] * 2 + viewport1['gutter']}
# print(f'starting config w,h: {canvas_reconfig["w"]}, {canvas_reconfig["h"]}')

lab = ttk.Label(root, text="up to 4 fixed-size images",
                style="MyLabel.TLabel")
lab.pack(pady=my_pady)

image_paths = ['four moods_1.png',
               'forest of death_1.png',
               'four moods_2.png',
               'parapsycho_1.png']
# image_paths = ['four moods_2.png',
#                'forest of death_1.png',
#                'four moods_2.png',
#                'forest of death_1.png']
myPhotoImages = []
heights = []
widths = []

# print('static images, native w,h and resized w,h:')
for i, n in enumerate(image_paths):
    im_path = 'images/' + n
    im = Image.open(im_path)
    imsize = cnv.init_image_size(im, viewport1)
    heights.append(imsize['h'])
    widths.append(imsize['w'])
    im_resize = im.resize((imsize['w'], imsize['h']))
    im_tk = ImageTk.PhotoImage(im_resize)
    myPhotoImages.append(im_tk)
    print(f"im {i} ({n}), {widths[i]}, {heights[i]}")

canv_static1 = tk.Canvas(root, background="green")

canv_static1.configure(width=canvas_reconfig['w'], height=canvas_reconfig['h'],
                       borderwidth=0)

posn = cnv.get_posn(viewport1, heights, widths, 'left', 'top')
# print()
print('positions of 4 ims:')
print(f"  im 0: {posn[0].x}, {posn[0].y}")
print(f"  im 1: {posn[1].x}, {posn[1].y}")
print(f"  im 2: {posn[2].x}, {posn[2].y}")
print(f"  im 3: {posn[3].x}, {posn[3].y}")

imid_list = []
for i, n in enumerate(image_paths):
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
# In the future, we may handle images in these additional situations:
#   1) all imgs smaller than the viewport width, with no re-scaling
#   2) all imgs smaller than the viewport height, with no re-scaling
#   3) after re-scaling, img widths or heights smaller than corresponding
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
