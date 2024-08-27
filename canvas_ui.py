"""
module: canvas_ui.py

purpose: types and functions for canvas to contain images.

comments: To display images at their native size(s) when img dimensions
          are smaller than both the viewport height and width, a new routine 
          should be written, to replace compare_ratios.
          Alternatively, init_image_size wouldn't be needed in the calling
          module; native sizes would be used directly. That approach is not
          transparent to the caller however.
          Note: this hasn't been tested.

author: Russell Folks

history:
-------
03-04-2024  creation
03-14-2024  Add a section for utility functions.
07-28-2024  Update function docstrings.
08-03-2024  Added comments section to module header.
08-16-2024  Edit get_posn to handle 2 or 3 images.
08-19-2024  Add alignment options: vertical center, horizontal right.
08-24-2024  Add function handle_extra to calculate position for images if
            there are more than two of them. Add type hinting for functions
            that don't have it.
"""
from PIL import ImageTk
import tkinter as tk

# -------
# utility
# -------
def compare_ratios(vp: dict,
                   im: object,
                   w: int,
                   h: int) -> dict:
    """Set new image height and/or width based on viewport shape.

    Images will be scaled up or down to match viewport height or width.
    """
    if vp > im:
        ht_new = h
        wid_new = int(ht_new * im)
    else:
        wid_new = w
        ht_new = int(wid_new / im)

    return {"h":ht_new, "w": wid_new}


# -------------
# static canvas: canvas and conatained objects are fixed size
# -------------
def Posn_init(self, x: int, y: int): 
    self.x = x
    self.y = y

Posn = type('Posn', (), {"__init__": Posn_init})


def handle_extra(vp: dict,
                 lis: list,
                 dim: str,
                 posn='edge') -> tuple:
    """If there are more than 2 images, position extra ones.

    arguments:
    vp = viewport shape
    lis = image heights or widths
    dim = 'h' for horizontal or 'v' for vertical arrangement
    posn = whether viewport space is split (space on either side of image.)
    """
    adjust = 2 if posn == 'split' else 1
    num = len(lis)
    match dim:
        case 'h':
            if num > 2:
                v3 = vp[dim] + vp['gutter'] + ((vp[dim] - lis[2]) / adjust)
            if num > 3:
                v4 = vp[dim] + vp['gutter'] + ((vp[dim] - lis[3]) / adjust)
        case 'w':
            if num > 2:
                v3 = (vp[dim] - lis[2]) / adjust
            if num > 3:
                v4 = vp[dim] + vp['gutter'] + ((vp[dim] - lis[3]) / adjust)

    return v3,v4


def get_posn(vp: dict,
             heights: list,
             widths: list,
             hjust: str = 'center',
             vjust: str = 'bottom') -> list:
    """Assign image locations within a canvas.

       arguments:
       vp = viewport width, height, gutter size
       heights, widths = sizes of up to four images
       hjust, vjust = type of justification for image positioning
    """
    imp1 = Posn(0, 0)
    imp2 = Posn(0, 0)
    imp3 = Posn(0, 0)
    imp4 = Posn(0, 0)

    # print(f'{vjust}, {hjust}')
    match vjust:
        case 'top':
            imp1.y, imp2.y = 0, 0
            imp3.y, imp4.y = vp['h'] + vp['gutter'], vp['h'] + vp['gutter']
        case 'center':
            # (vp ht - im ht) / 2
            imp1.y = (vp['h'] - heights[0]) / 2
            imp2.y = (vp['h'] - heights[1]) / 2
            # imp3.y, imp4.y = handle_extra(num_items, vp, heights, 'h', posn='split')
            imp3.y, imp4.y = handle_extra(vp, heights, 'h', posn='split')
        case 'bottom':
            imp1.y = vp['h'] - heights[0]
            imp2.y = vp['h'] - heights[1]
            # imp3.y, imp4.y = handle_extra(num_items, vp, heights, 'h')
            imp3.y, imp4.y = handle_extra(vp, heights, 'h')

    match hjust:
        case 'left':
            imp1.x, imp3.x = 0, 0
            imp2.x, imp4.x = vp['w'] + vp['gutter'], vp['w'] + vp['gutter']
        case 'center':
            imp1.x = (vp['w'] - (widths[0])) / 2
            imp2.x = vp['w'] + vp['gutter'] + ((vp['w'] - (widths[1])) / 2)
            # xvals = handle_extra(num_items, vp, widths, 'w', posn='split')
            # imp3.x = xvals[0]
            # imp4.x = xvals[1]
            # imp3.x, imp4.x = handle_extra(num_items, vp, widths, 'w', posn='split')
            imp3.x, imp4.x = handle_extra(vp, widths, 'w', posn='split')
        case 'right':
            # vp wd - im wd
            imp1.x = vp['w'] - widths[0]
            imp2.x = vp['w'] + vp['gutter'] + (vp['w'] - widths[1])
            # xvals = handle_extra(num_items, vp, widths, 'w')
            # imp3.x = xvals[0]
            # imp4.x = xvals[1]
            # imp3.x, imp4.x = handle_extra(num_items, vp, widths, 'w')
            imp3.x, imp4.x = handle_extra(vp, widths, 'w')

    return [imp1, imp2, imp3, imp4]


def init_image_size(im: object,
                    vp: dict) -> dict:
    """Set image display size and shape, based on the defined viewport size."""
    vp_ratio = vp['w'] / vp['h']
    im_ratio = im.width / im.height

    newsize = compare_ratios(vp_ratio, im_ratio, vp['w'], vp['h'])

    return newsize


# --------------
# dynamic canvas: canvas and contained objects can be resized.
# --------------
def resize_images(ev: tk.Event,
                  im: object,
                #   vp: dict,
                  canv: object) -> None:
    """Create image object for display at a calculated size."""
    global im_tk_new1 
    params1 = calc_resize(ev, im)

    im_tk_new1 = ImageTk.PhotoImage(params1['im_resize_new'])
    canv.create_image(0, 0,
                      anchor=tk.NW,
                      image=im_tk_new1)


def calc_resize(ev: tk.Event,
                im: object) -> object:
    """Calculate new size for a dynamically resizable canvas."""
    this_canv = ev.widget
    canv_width = ev.width
    canv_height = ev.height

    canv_ratio = canv_width / canv_height
    im_ratio = im.width / im.height
    # print(f"ratios: canv, im, cw, ch: {canv_ratio}, {im_ratio}, {canv_width}, {canv_height}")

    newsize = compare_ratios(canv_ratio, im_ratio, canv_width, canv_height)

    this_canv.delete(1)

    params = {'im_resize_new': im.resize((newsize['w'], newsize['h'])),
              'wid_int': int(canv_width),
              'ht_int': int(canv_height)}
    
    return params
