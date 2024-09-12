"""
module: canvas_ui.py

purpose: Types and functions for a canvas intended to contain images.

comments: To display images at their native size(s) when img dimensions
          are smaller than both the viewport height and width, EITHER: a new 
          routine should be written, to replace compare_ratios, OR:
          init_image_size wouldn't be needed in the calling
          module, and native sizes would be used directly. That approach is not
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
09-07-2024  Add get_1_posn(), to determine a single image position.
09-12-2024  Add get_positions() to determine up to four image positions.
            Remove handle_extra().
"""
"""
TODO: - Should get_posn() be modified to prevent images from overflowing 
        the viewport? This should probably be done by the caller.
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


def get_positions(vp, wd, ht, arrange):
    pos_list = []

    posn1 = get_1_posn(vp, wd[0], ht[0], arrange[0], arrange[1])
    pos_list.append(posn1)

    if len(wd) >= 2:
        posn2 = get_1_posn(vp, wd[1], ht[1], arrange[0], arrange[1], True)
        pos_list.append(posn2)

    if len(wd) >= 3:
        posn3 = get_1_posn(vp, wd[2], ht[2], arrange[0], arrange[1], False, True)
        pos_list.append(posn3)

    if len(wd) == 4:
        posn4 = get_1_posn(vp, wd[3], ht[3], arrange[0], arrange[1], True, True)
        pos_list.append(posn4)

    return pos_list


def get_1_posn(vp, wd, ht, hjust, vjust, shiftR=False, shiftD=False):
    """Assign location for one image in a Canvas."""
    imp = Posn(0, 0)

    match vjust:
        case 'top':
            imp.y = 0
        case 'center':
            imp.y = (vp['h'] - ht) / 2
        case 'bottom':
            imp.y = vp['h'] - ht

    match hjust:
        case 'left':
            imp.x = 0
        case 'center':
            imp.x = (vp['w'] - wd) / 2
        case 'right':
            imp.x = vp['w'] - wd

    if shiftR is True:
        imp.x += (vp['w'] + vp['gutter'])
    if shiftD is True:
        imp.y += (vp['h'] + vp['gutter'])

    return imp


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
    print(f'params1: {params1}')
    print(f"params1.im_resize_new w,h: {params1['im_resize_new'].width}, {params1['im_resize_new'].height}")
    print(f"params1.im_resize_new size: {params1['im_resize_new'].size}")

    im_tk_new1 = ImageTk.PhotoImage(params1['im_resize_new'])
    canv.create_image(0, 0,
                      anchor=tk.NW,
                      image=im_tk_new1)

def calc_resize_to_vp(vp, im):
    canv_width = vp['w']
    canv_height = vp['h']

    canv_ratio = canv_width / canv_height
    im_ratio = im.width / im.height
    # print(f"ratios: canv, im, cw, ch: {canv_ratio}, {im_ratio}, {canv_width}, {canv_height}")

    newsize = compare_ratios(canv_ratio, im_ratio, canv_width, canv_height)

    params = {'im_resize_new': im.resize((newsize['w'], newsize['h'])),
              'wid_int': int(canv_width),
              'ht_int': int(canv_height)}
    
    return params



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
