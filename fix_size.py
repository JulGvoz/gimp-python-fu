#!/usr/bin/env python

from gimpfu import *


def fix_size(image, drawable):
    pdb.gimp_image_undo_group_start(image)

    drawable = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)

    pdb.plug_in_autocrop(image, drawable)

    scaling_factor = 1
    if image.width > 479:
        scaling_factor = min(scaling_factor, 479.0 / image.width)
    if image.height > 345:
        scaling_factor = min(scaling_factor, 345.0 / image.height)
    pdb.gimp_image_scale(
        image, image.width * scaling_factor, image.height * scaling_factor
    )

    pdb.gimp_image_resize(
        image, 539, 539, (539.0 - image.width) / 2, 50.0 + (345.0 - image.height) / 2
    )
    pdb.gimp_layer_resize_to_image_size(drawable)

    pdb.gimp_image_undo_group_end(image)


register(
    "python-fu-fix-size",
    "Fix Token Size",
    "Fixes token size",
    "Zobody",
    "JulGvoz",
    "2021",
    "Fix Token Size",
    "RGBA",  # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
    ],
    [],
    fix_size,
    menu="<Image>/Image",
)

main()