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
"""
from PIL import ImageTk
import tkinter as tk

# -------
# utility
# -------
def compare_ratios(vp, im, w, h):
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

    num_items = len(heights)

    # print('vertical:')
    match vjust:
        case 'top':
            # print('    top')
            imp1.y, imp2.y = 0, 0
            imp3.y, imp4.y = vp['h'] + vp['gutter'], vp['h'] + vp['gutter']
        case 'center':
            # print('    v center')
            # (vp ht - im ht) / 2
            pass
        case 'bottom':
            # print('    bottom')
            imp1.y = vp['h'] - heights[0]
            imp2.y = vp['h'] - heights[1]
            if num_items > 2:
                imp3.y = vp['h'] + vp['gutter'] + (vp['h'] - heights[2])
                if num_items > 3:
                    imp4.y = vp['h'] + vp['gutter'] + (vp['h'] - heights[3])

    # print('horizontal:')
    match hjust:
        case 'left':
            # print('left')
            imp1.x, imp3.x = 0, 0
            imp2.x, imp4.x = vp['w'] + vp['gutter'], vp['w'] + vp['gutter']
        case 'center':
            # print('    h center')
            imp1.x = vp['w'] - (widths[0])
            imp2.x = vp['w'] + vp['gutter']
            if num_items > 2:
                imp3.x = vp['w'] - (widths[2])
                if num_items > 3:
                    imp4.x = vp['w'] + vp['gutter']
        case 'right':
            # print('    right')
            # vp wd - im wd
            pass

    return [imp1, imp2, imp3, imp4]


def init_image_size(im: object,
                    vp: dict) -> dict:
    """Set image display size and shape, based on the defined viewport size."""
    vp_ratio = vp['w'] / vp['h']
    im_ratio = im.width / im.height

    newsize = compare_ratios(vp_ratio, im_ratio, vp['w'], vp['h'])

    # return {"h":ht_new, "w": wid_new}
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
                imobj: object) -> object:
    """Calculate new size for a dynamically resizable canvas."""
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
