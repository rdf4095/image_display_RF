# image_display_RF

This application demonstrates display of images in a python Canvas.

There are three variant modules that can be run independently with the
supplied image examples. Setup and window controls are similar for all, but
the Canvas is handled differently. Canvas interaction functionality is 
mostly contained in the canvas_ui.py module.

display rationale
-----------------
image shapes are: portrait | or landscape --
viewport display order:
vp_0  vp_1
vp_2  vp_3

images can be positioned according to this logic:
landscape first:     OR      portrait first:
-- |                         |  --
|  --                        -- |

modules
-------
image_canvas_static.py
Displays up to four of the available images, scaled to viewports within
the canvas. Viewports are conceptual divisions of the Canvas area, and are
set to be width 400 pixels, height 300 pixels. Images can be any shape, so
width or height may be less than the viewport width or height. Alignment
of images can be adjusted using two Comboboxes. The two controls are:

    Vertical - justifies images to the top, middle or bottom of the viewport.
    Horizontal - justifies images to the left, center or right of the viewport.

image_canvas_dyn.py
Displays a single image. Alignment controls are absent, but the Canvas and
the contained image will change in size as the window is interactively
dragged to a different size. The "reset image size" button does just that.

image_canvas_both.py
Displays two Canvas objects, to demonstrate static and dynamic functionality
in one window.