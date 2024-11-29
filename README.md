# image_display_RF
## PURPOSE
This application demonstrates display of images in a python Canvas. 
There are three variant modules that can be run independently, with the
supplied image examples. Setup and window controls are similar for all, but
the Canvas is handled differently.

## DEPENDENCIES
- **styles_ttk** -- custom ttk widget styles
- **pillow** -- PIL (python image library) needed for ttkthemes
- **ttkthemes** -- better ttk widget theme options
- **tkinter** -- may need to installed, on some linux distributions

## OPERATION
The Canvas is divided into four conceptual regions called viewports, two above
and two below. Viewport shape is 4:3, slightly wider than tall.
Images are scaled to viewport size and placed in viewports sequentially: 
upper left, upper right, lower left and finally lower right.

Up to four images can be displayed. Image shapes can be taller (portrait)
or wider (landscape), and they are assigned to viewports by alternating their
shape, with either landscape first, or portrait first.

## modules
    image_canvas_static.py

Displays up to four of the available images, scaled to viewports within
the Canvas. Viewports are conceptual divisions of the Canvas area, and are
set to be width 400 pixels, height 300 pixels. Images can be any shape, so
width or height may be less than the viewport width or height. Alignment
of images can be adjusted using two Comboboxes. The two controls are:

- Vertical: justifies images to the top, middle or bottom of the viewport.
- Horizontal: justifies images to the left, center or right of the viewport.


    image_canvas_dyn.py

Displays a single image. Alignment controls are absent, but the Canvas and
its contained image will resize as the window is resized. The "reset image size"
button sets the window, Canvas and image to their original size.

    image_canvas_both.py

Displays two Canvas objects, to demonstrate static and dynamic functionality
in one window.

    canvas_ui.py

Functions for Canvas setup and image resizing and positioning.