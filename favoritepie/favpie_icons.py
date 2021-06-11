import os

import bpy

brush_icons = {}
brushes = ["crease", "blob", "draw", "draw_sharp", "clay", "clay_strips","clay_thumb", "inflate","layer",
        "grab", "nudge", "thumb", "snake_hook", "rotate", "pose", "multiplane_scrape", "boundary", "topology", "pinch",
        "flatten", "scrape", "fill", "smooth",
        "simplify", "cloth", "displacement_eraser", "mask", "draw_face_sets",
        ]
tools = ["transform.translate","transform.rotate","transform.resize","transform.transform",
        "mesh_filter","cloth_filter",
        "border_mask","lasso_mask","line_mask","box_trim","lasso_trim","line_project",
        "box_face_set","lasso_face_set","face_set_edit"]


def create_icons():
    global brush_icons
    icons_directory = bpy.utils.system_resource('DATAFILES', "icons")

    for brush in brushes:
            filename = os.path.join(icons_directory, f"brush.sculpt.{brush}.dat")
            icon_value = bpy.app.icons.new_triangles_from_file(filename)
            brush_icons[brush] = icon_value
        

    # for transform_ops in transform:
    #     filename = os.path.join(icons_directory, f"ops.{transform_ops}.dat")
    #     icon_value = bpy.app.icons.new_triangles_from_file(filename)
    #     brush_icons[transform_ops] = icon_value

def release_icons():
    global brush_icons
    for value in brush_icons.values():
        bpy.app.icons.release(value)
