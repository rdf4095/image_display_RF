"""
module: canvas_ui.py

purpose: types and functions for canvas to contain images.

author: Russell Folks

history:
-------
03-04-2024  creation
03-14-2024  Add a section for utility functions
"""
from PIL import ImageTk
import tkinter as tk

# -------------
# utility
# -------------
def compare_ratios(vp, im, w, h):
    if vp > im:
        ht_new = h
        wid_new = int(ht_new * im)
    else:
        wid_new = w
        ht_new = int(wid_new / im)

    return {"h":ht_new, "w": wid_new}


# -------------
# static canvas: images are fixed size
# -------------
def Posn_init(self, x: int, y: int):
    self.x = x
    self.y = y

Posn = type('Posn', (), {"__init__": Posn_init})

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

    match hjust:
        case 'left':
            imp1.x, imp3.x = 0, 0
            imp2.x, imp4.x = vp['w'] + vp['gutter'], vp['w'] + vp['gutter']
        case 'center':
            imp1.x = vp['w'] - (widths[0])
            imp3.x = vp['w'] - (widths[2])
            imp2.x, imp4.x = vp['w'] + vp['gutter'], vp['w'] + vp['gutter']

    match vjust:
        case 'top':
            imp1.y, imp2.y = 0, 0
            imp3.y, imp4.y = vp['h'] + vp['gutter'], vp['h'] + vp['gutter']
        case 'bottom':
            imp1.y = vp['h'] - heights[0]
            imp2.y = vp['h'] - heights[1]
            imp3.y, imp4.y = vp['h'] + vp['gutter'], vp['h'] + vp['gutter']

    return [imp1, imp2, imp3, imp4]


def init_image_size(im: object,
                    vp: dict) -> dict:
    
    vp_ratio = vp['w'] / vp['h']
    im_ratio = im.width / im.height

    newsize = compare_ratios(vp_ratio, im_ratio, vp['w'], vp['h'])

    # return {"h":ht_new, "w": wid_new}
    return newsize


# --------------
# dynamic canvas: canvas and contained images can be resized.
# --------------
def resize_images(ev: tk.Event,
                  im: object,
                  vp: dict,
                  canv: object) -> None:
    """Display image in a resizable canvas."""

    global im_tk_new1 
    params1 = calc_resize(ev, im)

    # print(f'in resize_images, w,h: {canv.winfo_width()}, {canv.winfo_height()}')

    im_tk_new1 = ImageTk.PhotoImage(params1['im_resize_new'])
    canv.create_image(0, 0,
                      anchor=tk.NW,
                      image=im_tk_new1)


def calc_resize(ev: tk.Event,
                imobj: object) -> object:
    """Calculate new size for image in a resizable canvas."""

    this_canv = ev.widget
    canv_width = ev.width
    canv_height = ev.height

    canv_ratio = canv_width / canv_height
    im_ratio = imobj.width / imobj.height
    # print(f"ratios: canv, im, cw, ch: {canv_ratio}, {im_ratio}, {canv_width}, {canv_height}")

    newsize = compare_ratios(canv_ratio, im_ratio, canv_width, canv_height)

    this_canv.delete(1)
    # print(f"dyn canv resized im w,h: {newsize['w']}, {newsize['h']}")

    params = {'im_resize_new': imobj.resize((newsize['w'], newsize['h'])),
              'wid_int': int(canv_width),
              'ht_int': int(canv_height)}
    
    return params
