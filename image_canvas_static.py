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
"""
"""
TODO: - Consider another arrangement option: group around canvas center.
      - If only two images, need option to dispay side-by-side or 1st-over-2nd.
      - Future: for conform_canvas_to_images(), handle images displayed 
        side-by-side (shrink to viewport height) vs 1st-above-2nd
        (shrink to viewport width.) This isn't needed if we're using
        order_by_size().
"""

import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

from ttkthemes import ThemedTk
from PIL import Image, ImageTk

import canvas_ui as cnv

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()
custui = SourceFileLoader("custui", "../pandas_data_RF/rf_custom_ui.py").load_module()

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


def sort_image_sizes(dims: list):
    pass


def order_by_size_ORIG(dims: list, paths: list) -> list:
    """Find the 2 images of greatest dimension.
    
    argument dims specifies the dimension, as image widths or heights.
    This function should only be called if len(dims) > 2. For 1 or 2
    images, the function does not manage display arrangement.
    """
    num_items = len(dims)
    sort_w = sorted(dims)
    largest_2 = sort_w[num_items - 2:]
    # newpaths = []
    
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


def order_by_size(dims: list, paths: list) -> list:
    """Find the 2 images of greatest dimension.

    argument dims specifies the dimension, as image widths or heights.
    This function should only be called if len(dims) > 2. For 1 or 2
    images, the function does not manage display arrangement.
    """
    num_items = len(dims)

    sizes_paths = zip(dims, paths)
    sizes_paths_tuple = tuple(sizes_paths)
    s_p_t_sorted = sorted(sizes_paths_tuple)
    # print(f'size-path tuples, sorted: {s_p_t_sorted}')

    """
    tallest-----x                  widest-----x
       |         |           OR:     |        |
       x----next_tallest             x----next_widest
    """
    if num_items == 4:
        newpaths = [s_p_t_sorted[3][1], s_p_t_sorted[0][1], s_p_t_sorted[1][1], s_p_t_sorted[2][1]]
    else:
        if num_items == 3:
            newpaths = [s_p_t_sorted[2][1], s_p_t_sorted[1][1], s_p_t_sorted[0][1]]
        else:
            newpaths = [s_p_t_sorted[1][1], s_p_t_sorted[0][1]]

    # print(f'old: newpaths: {newpaths}')
    return newpaths


"""
Callback function executed when a Combobox item is selected
in class FramedCombobox. See the FramedCombo instance below.
"""
# method 1
# --------
def align_images(ev: tk.Event,
                 vp: dict,
                 img_widths: list,
                 img_heights: list) -> None:
    """Set user-selected image alignment."""
    # print('in align_images')
    h = horizontal_align.get()
    v = vertical_align.get()

    img_positions = cnv.get_positions(vp, img_widths, img_heights, (h, v))
    set_all_posn(canv_static1, img_positions, img_widths)


# method 2
# simpler calling syntax; probably won't use this because it assumes
# variable names in the module, instead of accepting them as arguments.
# --------
def align_images_2(ev: tk.Event) -> None:
    """Set user-selected image alignment."""
    h = horizontal_align.get()
    v = vertical_align.get()

    img_positions = cnv.get_positions(viewport1, widths, heights, (h, v))
    # set_all_posn(canv_static1, positions, widths, (h, v))
    set_all_posn(canv_static1, img_positions, widths)


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
    # print('in align_images_canv_centered')
    v = var.get()
    if v == 1:
        # centered = True
        # apply centering relative to the canvas as a whole
        img_positions = cnv.get_positions(viewport1, widths, heights, ('cc', 'cc'))
        set_all_posn(canv_static1, img_positions, widths)

        # disable alignment Comboboxes

        # method 1
        # works but not ideal: uses a semi-private variable
        # (that only exists in a class method). See method 4
        # v_choice.cb.configure(state='disabled')
        # h_choice.cb.configure(state='disabled')

        # method 2
        # works but still not ideal: caller must know order of children
        # v_choice.winfo_children()[1].configure(state='disabled')
        # h_choice.winfo_children()[1].configure(state='disabled')

        # method 3
        # works, but a little verbose; could be a function if there is a
        # need to find a particular type of child widget.
        v_cb_widgets = [c for c in v_choice.winfo_children() if isinstance(c, tk.ttk.Combobox)]
        v_cb_widgets[0].configure(state='disabled')
        h_cb_widgets = [c for c in h_choice.winfo_children() if isinstance(c, tk.ttk.Combobox)]
        h_cb_widgets[0].configure(state='disabled')

        # method 4
        # works, by using new class variable (created after method 1 above)
        # print(f'FramedCombo doc: {custui.FramedCombo.__doc__}')
        # print()
        # print(f'__init__ doc: {custui.FramedCombo.__init__.__doc__}')
        # v_choice.cb.configure(state='disabled')
        # h_choice.cb.configure(state='disabled')

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


# app window
# root = tk.Tk()
# root = ThemedTk(theme='radiance')    # 'for ubuntu', okay
# root = ThemedTk(theme='elegance')    # spacing a little off with styles_ttk.py, unchecked cb looks gray
root = ThemedTk(theme='clearlooks')    # clean, good spacing with styles_ttk.py

root.resizable(True, True)
root.title("static canvas, ttk, pack")

default_dims = ""
style2 = styles_ttk.create_styles()

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
heights_start = []
widths_start = []
myPhotoImages = []
heights = []
widths = []

for i, n in enumerate(image_paths):
    im_path = 'images/' + n
    im = Image.open(im_path)
    imsize = cnv.init_image_size(im, viewport1)
    widths_start.append(imsize['w'])
    heights_start.append(imsize['h'])

    im_resize = im.resize((imsize['w'], imsize['h']))
    im_tk = ImageTk.PhotoImage(im_resize)
    myPhotoImages_start.append(im_tk)
    # print(f'    im_tk: ({im_tk.width()}, {im_tk.height()})')

# alternative layouts:
new_image_paths = order_by_size(widths_start, image_paths)
# new_image_paths = order_by_size(heights_start, image_paths)

for i, n in enumerate(new_image_paths):
    orig = image_paths.index(n)
    # print(i, n, orig)
    widths.append(widths_start[orig])
    heights.append(heights_start[orig])
    myPhotoImages.append(myPhotoImages_start[orig])

canv_static1 = tk.Canvas(root, background="green")
canv_static1.pack(padx=10, pady=10)

if centered:
    arrangement = ('cc', 'cc')
else:
    arrangement = ('left', 'top')

positions = cnv.get_positions(viewport1, widths, heights, arrangement)

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

# doesn't yet work correctly
if conform_canvas_to_images:
    canv_static1.configure(width=canvas_reconfig['w'], height=viewport1['h'])


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

v_choice = custui.FramedCombo(ui_fr,
                              cb_values=verticals,
                              display_name='vertical',
                              name='v_choice',
                              var=vertical_align,
                              callb=lambda ev, 
                                           vp=viewport1,
                                           ws=widths,
                                           hs=heights: align_images(ev, vp, ws, hs),
                            #   callb=align_images_2,
                              posn=[0,0])
# noinspection PyDefaultArgument
h_choice = custui.FramedCombo(ui_fr,
                              cb_values=horizontals,
                              display_name='horizontal',
                              name='h_choice',
                              var=horizontal_align,
                              callb=lambda ev,
                                           vp=viewport1,
                                           ws=widths,
                                           hs=heights: align_images(ev, vp, ws, hs),
                            #   callb=align_images_2,
                              posn=[0,1])
# print(f'v state: {v_choice.state()}')
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
btnq.grid(row=4, column=0, columnspan=2)

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
