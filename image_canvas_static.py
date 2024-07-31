"""
program: image_canvas_static.py

purpose: Display up to 4 images in one canvas, with constant size.

comments: Image viewports are set to a height-width ratio of 4:3.

author: Russell Folks

history:
-------
07-24-2024  creation
07-30-2024  Add buttons to change image placement.
"""
"""
TODO: - add top level frame for UI.
      - ...calculate window geometry based on top level frame.
      - fix image arrangement options 2-4 (left-top works.)
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


def set_top_center():
    print('in set_top_center')


def set_bottom_left():
    print('in set_bottom_left')


def set_bottom_center():
    print('in set_bottom_center')
    posn = cnv.get_posn(viewport1, heights, widths, 'center', 'bottom')
    print()
    print('new positions of 4 ims:')
    print(f"  im 0: {posn[0].x}, {posn[0].y}")
    print(f"  im 1: {posn[1].x}, {posn[1].y}")
    print(f"  im 2: {posn[2].x}, {posn[2].y}")
    print(f"  im 3: {posn[3].x}, {posn[3].y}")
    print()
    print(f'id of im 1: {id(imid_list[0])}')
    print(f'config of im 1: {canv_static1.itemconfigure(imid_list[0])}')

    # im1 = canv_static1.itemcget(imid_list[0])
    # print(im1)

    # print(f'x,y of im 1: {id(imid_list[0])}')


# app window
default_dims = "520x550"

root = tk.Tk()
root.geometry (default_dims)
root.minsize(520, 550)
root.resizable(1, 1)
root.title("image, ttk, pack")

style2 = styles_ttk.CreateStyles()

viewport1 = {'w': 200, 'h': 150, 'gutter': 10}
# viewport1 = {'w': 400, 'h': 300, 'gutter': 10}
my_pady = 10

# canvas_reconfig = {'w': viewport1['w'] * 2 + viewport1['gutter'],
#                    'h': viewport1['h']}
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
    # print(f"im {i} ({n}), {widths[i]}, {heights[i]}")

canv_static1 = tk.Canvas(root, background="green")

# print(f'canv_static1 id: {id(canv_static1)}')

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

canv_static1.pack(pady=10)
canv_static1.update()

# Scale the canvas to hold the images with no extra space.
# canvas_config_ht = max(sum(heights[0::2]), sum(heights[1::2])) + viewport['gutter']
# print(f'final gutter: {viewport1["gutter"]}')
# canvas_reconfig['h'] = max(sum(heights[0::2]) + viewport1['gutter'],
#                            sum(heights[1::2]) + viewport1['gutter'])
# print(f'canvas_reconfig h: {canvas_reconfig["h"]}')
# canvas_reconfig['h'] += (viewport1['gutter'])
# print(f'canvas_reconfig h: {canvas_reconfig["h"]}')

# print()
# print(f"static canv reconfig w,h: {canvas_reconfig['w']}, {canvas_reconfig['h']}")

canv_static1.configure(width=canvas_reconfig['w'], height=canvas_reconfig['h'])
# canv_static1.configure(width=410, height=310)

# other UI elements ----------
button_fr_1 = ttk.Frame(root, relief='groove')

but_top_left = ttk.Button(button_fr_1,
                          text='top-left',
                          command=set_top_left,
                          style="MyButton1.TButton")
but_top_left.pack(side='left', padx=5, pady=5)

but_top_center = ttk.Button(button_fr_1,
                           text='top-center',
                           command=set_top_center,
                           style="MyButton1.TButton")
but_top_center.pack(side='left', padx=5, pady=5)

but_bottom_left = ttk.Button(button_fr_1,
                             text='bottom-left',
                             command=set_bottom_left,
                             style="MyButton1.TButton")
but_bottom_left.pack(side='left', padx=5, pady=5)

but_bottom_center = ttk.Button(button_fr_1,
                              text='bottom-center',
                              command=set_bottom_center,
                              style="MyButton1.TButton")
but_bottom_center.pack(side='left', padx=5, pady=5)

button_fr_1.pack(side='top')

button_fr_1.update()
# geometry: w h x y
# print(f'button_fr_1 geometry: {button_fr_1.winfo_geometry()}')
# print(f'button_fr_1 w,h: {button_fr_1.winfo_width()}, {button_fr_1.winfo_height()}')

but_reset_size = ttk.Button(root,
                            text="reset window size",
                            command=lambda dims=default_dims: reset_window_size(dims),
                            style="MyButton1.TButton")
but_reset_size.pack(side='top', padx=5, pady=10)



# or: command=root.destroy
btnq = ttk.Button(root,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.pack(side="top", fill='x', padx=10)

if __name__ == "__main__":
    root.mainloop()
