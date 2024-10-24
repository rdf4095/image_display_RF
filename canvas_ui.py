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
09-13-2024  Add type hinting to get_1_posn and get_positions.
10-23-2024  Add function set_canv_centered, to move all images toward the
            center of the canvas, allowing for the viewport gutter.
"""
"""
TODO: - Should get_posn() be modified to prevent images from overflowing 
        the viewport? This should probably be done by the caller.
      - refactor set_canv_centered.
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


def get_positions(vp: dict,
                  wd: list,
                  ht: list,
                  arrange: tuple) -> list:
    """Assign locations for all images in a Canvas."""
    pos_list = []

    


    if arrange == ('cc', 'cc'):
        pos_list = set_canv_centered(vp, wd, ht)
        print()
        print(f'    pos_list: {pos_list[0].x}, {pos_list[0].y}')
        return pos_list

    posn1 = get_1_posn(vp, wd[0], ht[0], arrange)
    pos_list.append(posn1)

    if len(wd) >= 2:
        posn2 = get_1_posn(vp, wd[1], ht[1], arrange, True)
        pos_list.append(posn2)

    if len(wd) >= 3:
        posn3 = get_1_posn(vp, wd[2], ht[2], arrange, False, True)
        pos_list.append(posn3)

    if len(wd) == 4:
        posn4 = get_1_posn(vp, wd[3], ht[3], arrange, True, True)
        pos_list.append(posn4)

    return pos_list


def get_1_posn(vp: dict,
               wd: list,
               ht: list,
               arrange: tuple,
               shiftR: bool = False,
               shiftD: bool = False) -> Posn:
    """Assign location for one image in a Canvas."""
    imp = Posn(0, 0)

    match arrange[1]:
        case 'top':
            imp.y = 0
        case 'center':
            imp.y = (vp['h'] - ht) / 2
        case 'bottom':
            imp.y = vp['h'] - ht

    match arrange[0]:
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


def set_canv_centered(vp, wd, ht):
    positions = []
    imp1 = Posn(0, 0)
    imp2 = Posn(0, 0)
    imp3 = Posn(0, 0)
    imp4 = Posn(0, 0)

    imp1.x = vp['w'] - wd[0]
    imp1.y = vp['h'] - ht[0]
    positions.append(imp1)

    imp2.x = vp['w'] + vp['gutter']
    imp2.y = vp['h'] - ht[1]
    positions.append(imp2)

    imp3.x = vp['w'] - wd[2]
    imp3.y = vp['h'] + vp['gutter']
    positions.append(imp3)

    imp4.x = vp['w'] + vp['gutter']
    imp4.y = vp['h'] + vp['gutter']
    positions.append(imp4)

    # for n, p in enumerate(positions):
    #     print(f'    imp: {positions[n].x}, {positions[n].y}')

    return positions


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

def calc_resize_to_vp(vp: dict, im: object) -> dict:
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



def calc_resize(ev: tk.Event, im: object) -> dict:
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
              'im_wd_new': newsize['w'],
              'im_ht_new': newsize['h'],
              'canv_wd': int(canv_width),
              'canv_ht': int(canv_height)}
    
    return params
