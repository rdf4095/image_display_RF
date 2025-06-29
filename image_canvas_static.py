"""
program: image_canvas_static.py

purpose: Display up to 4 images in one canvas, with constant size.

comments: Display viewports are set to a height-width ratio of 4:3.
          Control widgets allow the images to be horizontally and
          vetically justified different ways within their viewports.

author: Russell Folks

history:
-------
07-24-2024  creation
...
09-03-2024  Test align_images and align_images_2 with a list of values slightly
            different from 'widths'. This works, but should the code prevent
            images from overflowing the viewport?
09-05-2024  Type-hint the event parameter in align_images, add comments.
            Remove the button to align images.
09-07-2024  Test canvas_ui.py/get_1_posn, to set image positions individually.
09-12-2024  Use canvas_ui,py/get_positions to get 1-4 image positions.
            get_1_posn is not directly called in this module. Remove most
            comments around align_images().
09-16-2024  Disable reset_window_size() and its button: this app does not use
            resizable canvas.
10-22-2024  Update module header, remove old commented code.
10-24-2024  Add button to center images in the whole canvas.
10-26-2024  Add functionality for the centering button.
11-25-2024  Address function parameter warnings (default None in align_images, names
            that shadow the enclosing scope, etc.) Load and use ttkthemes.
11-26-2024  Simplify order_by_size() by using zip().
11-27-2024  Recommit.
11-28-2024  Update README file. Rename styles_ttk to sttk to conform with other
            projects.
06-25-2025  Rewrite docstring for order_by_size. Begin implementing custom
            object for image attributes. Rewrite order_by_size().
"""
"""
TODO: 
    1. Replace the two custui/FramedCombo with tool_classes/ComboboxFrame.
    2. If only two images, need option to display side-by-side or 1st-over-2nd.
    3. Refactor some variable names (like in enumerate statements) for clarity.
    4. Move lengthy comments to a 'notes' file, if still needed.
"""

import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from ttkthemes import ThemedTk
from PIL import Image, ImageTk

sttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()
# custui = SourceFileLoader("custui", "../pandas_data_RF/rf_custom_ui.py").load_module()
cnv_ui = SourceFileLoader("cnv", "../canvas/canvas_ui.py").load_module()
tc = SourceFileLoader("tc", "../utilities/tool_classes.py").load_module()

def set_all_posn(canvas: object,
                 img_positions: list,
                 wd: list) -> None:
    """Set position for up to four images in a canvas."""
    canvas.moveto(1, img_positions[0].x, img_positions[0].y)

    if len(wd) >= 2:
        canvas.moveto(2, img_positions[1].x, img_positions[1].y)

    if len(wd) >= 3:
        canvas.moveto(3, img_positions[2].x, img_positions[2].y)

    if len(wd) == 4:
        canvas.moveto(4, img_positions[3].x, img_positions[3].y)


def order_by_size(dims: list, paths: list) -> list:
    """Find the 2 images of greatest dimension.

    argument dims specifies the dimension, as image widths or heights.
    If heights are passed, the display arrangement is given by diagram (1),
    if widths are passed, the display arrangement is given by diagram (2).
    (1)                            (2)
    tallest-----x                  widest-----x
       |         |           OR:     |        |
       x----next_tallest             x----next_widest

    This function should only be called if len(dims) > 2. For 1 or 2
    images, this function does not manage display arrangement.
    """
    num_items = len(dims)

    sizes_paths = zip(dims, paths)
    sizes_paths_tuple = tuple(sizes_paths)
    s_p_t_sorted = sorted(sizes_paths_tuple)

    if num_items == 4:
        newpaths = [s_p_t_sorted[3][1], s_p_t_sorted[0][1], s_p_t_sorted[1][1], s_p_t_sorted[2][1]]
    else:
        if num_items == 3:
            newpaths = [s_p_t_sorted[2][1], s_p_t_sorted[1][1], s_p_t_sorted[0][1]]
        else:
            newpaths = [s_p_t_sorted[1][1], s_p_t_sorted[0][1]]

    # print(f'old: newpaths: {newpaths}')
    return newpaths


def order_by_size_new(objects, dim='width') -> list:
    """Find the images of greatest dimension.

    argument dims specifies the dimension, as image widths or heights.
    If heights are passed, the display arrangement is given by diagram (1),
    if widths are passed, the display arrangement is given by diagram (2).
    (1)                            (2)
    tallest-----x                  widest-----x
       |         |           OR:     |        |
       x----next_tallest             x----next_widest

    This function should only be called if len(dims) > 2. For 1 or 2
    images, this function does not manage display arrangement.
    """
    num_items = len(objects)
    # if not sorting in place:
    # objects_new = []

    # print(f'before:\n{objects}')
    if dim == 'width':
        objects.sort(key=lambda x: x.width)
    else:
        # can we subscript instead of using dot notation?
        objects.sort(key=lambda x: x.height)
    # print(f'after:\n{objects}')

    # interleave the larger and smaller dim
    if num_items == 4:
        newpaths = [objects[3].path, objects[1].path, objects[0].path, objects[2].path]
    else:
        if num_items == 3:
            newpaths = [objects[2].path, objects[0].path, objects[1].path]
        else:
            newpaths = [objects[1].path, objects[0].path]

    return newpaths


"""
Callback function executed when a Combobox item is selected in class
FramedCombobox. See the FramedCombo instance below.
"""
# method 1
# --------
def align_images(ev: tk.Event,
                 vp: dict,
                 img_widths: list,
                 img_heights: list) -> None:
    """Set user-selected image alignment."""
    h = horizontal_align.get()
    v = vertical_align.get()

    img_positions = cnv_ui.get_positions(vp, img_widths, img_heights, (h, v))
    set_all_posn(canv_static1, img_positions, img_widths)


def show_vp_borders(canv: object, vp: dict) -> None:
    """Display rectangles to show the viewport (vp) borders within a canvas.

    Calculation of rectangle size and location is independent of vp size,
    but as an example calculation, assume viewports 200-wide, 150-high, and
    gutter between viewports of 10.
    vp_wd   = 200
    vp_wd_z = 199 = vp_wd - 1
    vp_wdx2_z = 399 = (vp_wd * 2) - 1

    vp_ht   = 150
    vp_ht_z = 149 = vp_ht - 1
    vp_htx2 = 300 = vp_ht * 2
    """
    gutter = vp['gutter']
    width_pixel = vp['w']-1
    widthx2_pixel = (vp['w'] * 2) - 1
    height_pixel = vp['h']-1
    heightx2 = vp['h'] * 2

    # Left Upper and Right Lower coordinates
    v1_LU = 0, 0
    v1_RL = width_pixel, height_pixel

    v2_LU = vp['w'] + gutter, 0 
    v2_RL = widthx2_pixel + gutter, height_pixel

    v3_LU = 0, vp['h'] + gutter
    v3_RL = width_pixel, heightx2 + gutter

    v4_LU = vp['w'] + gutter, vp['h'] + gutter
    v4_RL = widthx2_pixel + gutter, heightx2 + gutter

    canv.create_rectangle(v1_LU + v1_RL)
    canv.create_rectangle(v2_LU + v2_RL)
    canv.create_rectangle(v3_LU + v3_RL)
    canv.create_rectangle(v4_LU + v4_RL)


def align_images_canv_centered(var):
    """Center images relative to the canvas as a whole."""
    v = var.get()
    if v == 1:
        # centered = True
        img_positions = cnv_ui.get_positions(viewport1, widths, heights, ('cc', 'cc'))
        set_all_posn(canv_static1, img_positions, widths)

        # Disable alignment Comboboxes
        # This method works, but is a little verbose
        # It could be a function if there is a need to find a
        #  particular type of child widget.
        v_cb_widgets = [c for c in v_choice.winfo_children() if isinstance(c, tk.ttk.Combobox)]
        v_cb_widgets[0].configure(state='disabled')
        h_cb_widgets = [c for c in h_choice.winfo_children() if isinstance(c, tk.ttk.Combobox)]
        h_cb_widgets[0].configure(state='disabled')

    else:
        # centered = False
        # enable alignment Comboboxes
        v_cb_widgets = [c for c in v_choice.winfo_children() if isinstance(c, tk.ttk.Combobox)]
        v_cb_widgets[0].configure(state='readonly')
        h_cb_widgets = [c for c in h_choice.winfo_children() if isinstance(c, tk.ttk.Combobox)]
        h_cb_widgets[0].configure(state='readonly')

        # align images as specified by the Comboboxes
        noev = tk.Event()    # TODO: is this necessary?
        align_images(noev, viewport1, widths, heights)


# root = ThemedTk(theme='elegance')    # spacing a little off with styles_ttk.py, unchecked cb looks gray
# root = ThemedTk(theme='radiance')    # 'for ubuntu', okay
root = ThemedTk()                    # better

root.resizable(True, True)
root.title("static canvas, ttk")

default_dims = ""
style2 = sttk.create_styles()

viewport1 = {'w': 200, 'h': 150, 'gutter': 10}
my_pady = 10

centered = False
show_layout = True
conform_canvas_to_images = False

canvas_reconfig = {'w': viewport1['w'] * 2 + viewport1['gutter'],
                   'h': viewport1['h'] * 2 + viewport1['gutter']}

lab = ttk.Label(root, text="up to 4 images in a fixed-size canvas",
                style="MyLabel.TLabel")
lab.pack(pady=my_pady)

image_paths = ['four moods_2.png',      # tall
               'forest of death_1.png', # tall
               'parapsycho_1.png',      # wide
               'four moods_1.png',      # wide
               ]
# test with 3 images
# image_paths = ['four moods_2.png',
#                'forest of death_1.png',
#                'parapsycho_1.png'
#                ]

# test with 2 images
# image_paths = ['forest of death_1.png',
#                'parapsycho_1.png'
#                ]
myPhotoImages_start = []
myPhotoImages = []
# heights_start = []
# widths_start = []
# heights = []
# widths = []

# try
class ImageObject():
    def __init__(self,
                 path='',
                 width=0,
                 height=0):
        self.path = path
        self.width = width
        self.height = height

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}(path={self.path}, width={self.width!r}, height={self.height!r})'

object_list = []
# end try

for i, n in enumerate(image_paths):
    im_path = 'images/' + n
    im = Image.open(im_path)
    imsize = cnv_ui.init_image_size(im, viewport1)
    # widths_start.append(imsize['w'])
    # heights_start.append(imsize['h'])

    im_resize = im.resize((imsize['w'], imsize['h']))
    im_tk = ImageTk.PhotoImage(im_resize)
    myPhotoImages_start.append(im_tk)
    # print(f'    im_tk: ({im_tk.width()}, {im_tk.height()})')

    # try
    animage = ImageObject(n, imsize['w'], imsize['h'])
    object_list.append(animage)
    # end try

new_image_paths = order_by_size_new(object_list, 'width')

# new_image_paths = order_by_size(widths_start, image_paths)

for i, n in enumerate(new_image_paths):
    orig = image_paths.index(n)
    # widths.append(widths_start[orig])
    # heights.append(heights_start[orig])
    myPhotoImages.append(myPhotoImages_start[orig])

canv_static1 = tk.Canvas(root, background="green")
canv_static1.pack(padx=10, pady=10)

if centered:
    arrangement = ('cc', 'cc')
else:
    arrangement = ('left', 'top')

# positions = cnv_ui.get_positions(viewport1, widths, heights, arrangement)
positions = cnv_ui.get_positions(viewport1, object_list, arrangement)

imid_list = []
for i, n in enumerate(new_image_paths):
    tagname = "tag_im" + str(i)
    # print(f'position {i}: {positions[i].x}, {positions[i].y}')
    imid = canv_static1.create_image(positions[i].x, positions[i].y, anchor=tk.NW, image=myPhotoImages[i],
                                     tag = tagname)
    imid_list.append(imid)

canv_static1.update()

# print(f'widths: {widths}')
# print(f'heights: {heights}')
# print(f"reconfig w,h: {canvas_reconfig['w']}, {canvas_reconfig['h']}")

canv_static1.configure(width=canvas_reconfig['w'], height=canvas_reconfig['h'])



"""
Scale the canvas to hold images with no extra space.
This is to handle future situations like:
  1) all imgs smaller than the viewport width, with no re-scaling
  2) all imgs smaller than the viewport height, with no re-scaling
  3) after re-scaling, all img widths or heights smaller than corresponding
     canvas dimension.
In all 3 cases, remove "extra" canvas width or height. The purpose is to allow
other objects to be positioned closer to the canvas.
"""
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

if show_layout:
    show_vp_borders(canv_static1, viewport1)

verticals = ['top', 'center', 'bottom']
horizontals = ['left', 'center', 'right']
vertical_align = tk.StringVar()
horizontal_align = tk.StringVar()

widths = [w.width for w in object_list]
heights = [h.height for h in object_list]

# v_choice = custui.FramedCombo(ui_fr,
v_choice = tc.ComboboxFrame(ui_fr,
                              cb_values=verticals,
                              display_name='vertical',
                              name='v_choice',
                              var=vertical_align,
                              callb=lambda ev, 
                                           vp=viewport1,
                                           ws=widths,
                                           hs=heights: align_images(ev, vp, ws, hs),
                              posn=[0,0])

# h_choice = custui.FramedCombo(ui_fr,
h_choice = tc.ComboboxFrame(ui_fr,
                              cb_values=horizontals,
                              display_name='horizontal',
                              name='h_choice',
                              var=horizontal_align,
                              callb=lambda ev,
                                           vp=viewport1,
                                           ws=widths,
                                           hs=heights: align_images(ev, vp, ws, hs),
                              posn=[0,1])

ui_fr.pack(side='top', ipadx=10, ipady=10, padx=5, pady=5)
ui_fr.update()

cbvar1 = tk.IntVar(value=0)
canv_centered = ttk.Checkbutton(ui_fr,
                                text='canvas centered',
                                variable=cbvar1,
                                name='canvas_centered',
                                command=lambda var=cbvar1: align_images_canv_centered(var))
canv_centered.grid(row=3, column=0, columnspan=2)

btnq = ttk.Button(ui_fr,
                  text="Quit",
                  command=root.quit,
                  style="MyButton1.TButton")
btnq.grid(row=4, column=0, columnspan=2, pady=10)

# report some layout dimensions
# ------
# print(f'canv_static1 h,w: {canv_static1.winfo_height()}, {canv_static1.winfo_width()}')
# print(f'ui_fr h,w: {ui_fr.winfo_height()}, {ui_fr.winfo_width()}')
# print(f'lab h,w: {lab.winfo_height()}, {lab.winfo_width()}')

total_ht = lab.winfo_height() + canv_static1.winfo_height() + ui_fr.winfo_height()
total_wd = max(lab.winfo_width(), canv_static1.winfo_width(), ui_fr.winfo_width())
default_dims = f'{total_wd}x{total_ht}'
# print(f'default_dims: {default_dims}')
# print(f'    {lab.winfo_height()}, {canv_static1.winfo_height()}, {ui_fr.winfo_height()}')

# optional: report function signatures.
# import inspect

# print('align_images:')
# sig = (inspect.signature(align_images))
# print(f'   signature: {sig}')

root.minsize(total_wd, total_ht)

if __name__ == "__main__":
    root.mainloop()
