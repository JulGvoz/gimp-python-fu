#!/usr/bin/env python

from gimpfu import *


def botc_tokenfy(image, drawable, color, original, file):
    true_size = 385.0
    pdb.gimp_image_undo_group_start(image)
    pdb.gimp_message_set_handler(ERROR_CONSOLE)
    # resize the image so it is easier to deal with
    pdb.plug_in_autocrop(image, drawable)
    pdb.gimp_image_resize(image, image.width + 6, image.height + 6, 3, 3)
    if image.height < image.width:
        pdb.gimp_image_scale(image, true_size, true_size * image.height / image.width)
    else:
        pdb.gimp_image_scale(image, true_size * image.width / image.height, true_size)
    original_width = image.width
    original_height = image.height
    pdb.gimp_image_resize(
        image,
        true_size,
        true_size,
        (true_size - original_width) / 2,
        (true_size - original_height) / 2,
    )
    pdb.gimp_layer_resize_to_image_size(drawable)

    # get color of top left corner, which we expect to be just pure transparent
    bg_color = pdb.gimp_image_pick_color(image, drawable, 5, 5, FALSE, FALSE, 0)
    bg_color = (0, 0, 0, 0)

    # set context parameters (for select color)
    pdb.gimp_context_set_feather(FALSE)
    pdb.gimp_context_set_sample_merged(FALSE)
    pdb.gimp_context_set_sample_transparent(TRUE)
    pdb.gimp_context_set_sample_threshold(0.5)
    pdb.gimp_context_set_sample_criterion(0)

    # select the background of the image
    pdb.gimp_image_select_color(image, 2, drawable, bg_color)

    # invert  to select the foreground
    pdb.gimp_selection_invert(image)

    # save as the only path
    pdb.plug_in_sel2path(image, drawable)

    # we want the path to be proper, therefore we select all
    pdb.gimp_selection_all(image)

    # set context for stroke
    pdb.gimp_context_set_opacity(100)
    pdb.gimp_context_set_paint_mode(LAYER_MODE_NORMAL)
    pdb.gimp_context_set_stroke_method(STROKE_LINE)
    pdb.gimp_context_set_line_width(2.5)

    # pdb.gimp_message("Debug image: ")
    # pdb.gimp_message(image)

    # pdb.gimp_message("Creating new layer")
    border_layer = pdb.gimp_layer_new(
        image, true_size, true_size, 0, "White Border", 100, 28
    )
    border_layer.add_alpha()
    pdb.gimp_drawable_fill(border_layer, FILL_TRANSPARENT)
    # pdb.gimp_message(FILL_TRANSPARENT)
    # pdb.gimp_message(border_layer)

    # pdb.gimp_image_insert_layer(image, border_layer, 0, -1)

    fill_layer = pdb.gimp_layer_new(
        image, true_size, true_size, 0, "Pure color", 100, 28
    )
    fill_layer.add_alpha()

    image.insert_layer(fill_layer)

    token_layer = pdb.gimp_file_load_layer(image, file)
    image.insert_layer(token_layer)
    pdb.gimp_layer_scale(token_layer, 695, 695, FALSE)
    pdb.gimp_layer_set_offsets(
        token_layer, (true_size - 695) / 2, (true_size - 695) / 2
    )
    pdb.gimp_layer_set_mode(token_layer, LAYER_MODE_GRAIN_EXTRACT)
    """
    pdb.gimp_layer_resize(
        token_layer,
        695,
        695,
        0,
        0,
    )
    """

    image.insert_layer(border_layer)

    pdb.gimp_drawable_fill(fill_layer, FILL_TRANSPARENT)

    pdb.gimp_context_set_foreground(color)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, image.active_vectors)
    pdb.gimp_drawable_edit_fill(fill_layer, FILL_FOREGROUND)

    pdb.gimp_selection_all(image)

    # stroke around the path
    # pdb.gimp_message("Drawing a border")
    pdb.gimp_context_set_foreground((255, 255, 255))
    pdb.gimp_drawable_edit_stroke_item(border_layer, image.active_vectors)

    # cleanup
    pdb.gimp_image_remove_vectors(image, image.active_vectors)
    pdb.gimp_image_remove_layer(image, drawable)
    pdb.gimp_image_undo_group_end(image)
    if original:
        # pdb.gimp_image_resize(image, 539, 539, (539 - true_size) / 2, 60)
        pdb.python_fu_fix_size(image, image.active_drawable)


register(
    "python-fu-botc-tokenfy",
    "Tokenfy",
    "Converts icon to a token",
    "Zobody",
    "JulGvoz",
    "2021",
    "Tokenfy...",
    "RGBA",  # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_COLOR, "color", "Colour", (0, 96, 255)),
        (PF_BOOL, "original", "Adjust for bra1n tool", FALSE),
        (
            PF_STRING,
            "file",
            "Token file location",
            "C:/Users/Namai/Desktop/gimp/plugins/token.png",
        ),
    ],
    [],
    botc_tokenfy,
    menu="<Image>/Filters/Map",
)

main()