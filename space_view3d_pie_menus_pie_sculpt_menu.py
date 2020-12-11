# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Hotkey: 'V' > Sculpt Pie",
    "description": "Sculpt Brush Menu",
    "author": "pitiwazou, meta-androcto, zNight(modified)",
    "version": (0, 1, 0),
    "blender": (2, 91, 0),
    "location": "V key",
    "warning": "",
    "doc_url": "",
    "category": "Sculpt Pie"
    }   

import os

import bpy
from bpy.types import Menu, Operator


# Sculpt Draw
class PIE_OT_SculptSculptDraw(Operator):
    bl_idname = "sculpt.sculptraw"
    bl_label = "Sculpt SculptDraw"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.tool_settings.sculpt.brush = bpy.data.brushes['SculptDraw']
        return {'FINISHED'}


# Pie Sculp Pie Menus - V
class PIE_MT_SculptPie(Menu):
    bl_idname = "PIE_MT_sculpt"
    bl_label = "Pie Sculpt"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        pie = layout.menu_pie()
        pie.scale_y = 1.2
        # 4 - LEFT
        pie.menu(PIE_MT_SculptDraw.bl_idname,
                    text="    Draw Brushes", icon_value=brush_icons["clay"])
        # Moved to TOP - 7
        # pie.operator("paint.brush_select",
        #             text="    Crease", icon_value=brush_icons["crease"]).sculpt_tool = 'CREASE'
        ## 6 - RIGHT
        pie.menu(PIE_MT_SculptSmooth.bl_idname,
                    text="    Smooth Brushes", icon_value=brush_icons["smooth"])

        # Moved to Draw group
        # pie.operator("paint.brush_select",
        #             text="    Blob", icon_value=brush_icons["blob"]).sculpt_tool = 'BLOB'
        # 2 - BOTTOM
        pie.menu(PIE_MT_SculptGrab.bl_idname,
                    text="    Grab Brushes", icon_value=brush_icons["grab"])
        ## 8 - TOP
        pie.operator("sculpt.sculptraw",
                    text="    Draw", icon_value=brush_icons["draw"])
        ## 7 - TOP - LEFT
        pie.operator("paint.brush_select",
                    text="    Crease", icon_value=brush_icons["crease"]).sculpt_tool = 'CREASE'
        # Moved to Draw group
        # pie.operator("paint.brush_select",
        #             text="    Clay", icon_value=brush_icons["clay"]).sculpt_tool = 'CLAY'
        ## 9 - TOP - RIGHT
        pie.operator("paint.brush_select",
                    text="    Clay Strips", icon_value=brush_icons["clay_strips"]).sculpt_tool = 'CLAY_STRIPS'
        ## 1 - BOTTOM - LEFT
        pie.menu(PIE_MT_SculptMaskTrim.bl_idname,
                text="    Mask & Trim", icon_value=brush_icons["mask"])
        ## Moved to Draw group
        # pie.operator("paint.brush_select",
        #             text="    Inflate/Deflate", icon_value=brush_icons["inflate"]).sculpt_tool = 'INFLATE'
        ## 3 - BOTTOM - RIGHT
        pie.menu(PIE_MT_SculptExtras.bl_idname,
                text="    More Tools", icon_value=brush_icons["cloth"])

        pie.separator()
        pie.separator()
        other = pie.column()
        gap = other.column()
        gap.separator()
        gap.scale_y = 4
        transformation_menu_A = other.box().row()
        transformation_menu_A.scale_y= 1.3
        transformation_menu_A.scale_x= 1.2
        transformation_menu_A.operator("wm.tool_set_by_id",text='Move', icon_value=brush_icons["transform.translate"]).name = "builtin.move"
        transformation_menu_A.operator("wm.tool_set_by_id",text='Rotate', icon_value=brush_icons["transform.rotate"]).name = "builtin.rotate"
        transformation_menu_A.operator("wm.tool_set_by_id",text='Scale', icon_value=brush_icons["transform.resize"]).name = "builtin.scale"
        transformation_menu_A.operator("wm.tool_set_by_id",text='Transform', icon_value=brush_icons["transform.transform"]).name = "builtin.transform"

        pie.separator()
        pie.separator()
        other_B = pie.row()
        other_B.label(text='                        ')
        gap_B = other_B.column()
        gap_B.separator()
        gap_B.scale_y = 3
        transformation_menu_B = other_B.box().column()
        transformation_menu_B.label(text="Mirror", icon='MOD_MIRROR')
        transformation_menu_B.scale_x= 1.2
        transformation_menu_B.operator("wm.context_toggle", text="X ").data_path = "object.data.use_mirror_x"
        transformation_menu_B.operator("wm.context_toggle", text="Y ").data_path = "object.data.use_mirror_y"
        transformation_menu_B.operator("wm.context_toggle", text="Z ").data_path = "object.data.use_mirror_z"
        gap_B.label()
        gap_B.label()
# Pie Sculpt Draw - Draw tool brushes
class PIE_MT_SculptDraw(Menu):
    bl_idname = "PIE_MT_sculptDraw"
    bl_label = "Pie Sculpt Draw"

    def draw(self, context):
        global brush_icons
        layout = self.layout    
        layout.scale_y = 1.5    
        layout.operator("wm.tool_set_by_id",text='Clay', icon_value=brush_icons["clay"]).name = "builtin_brush.Clay"
        layout.operator("wm.tool_set_by_id",text='Draw Sharp', icon_value=brush_icons["draw_sharp"]).name = "builtin_brush.Draw Sharp"
        layout.operator("wm.tool_set_by_id",text='Inflate', icon_value=brush_icons["inflate"]).name = "builtin_brush.Inflate"
        layout.operator("wm.tool_set_by_id",text='Blob', icon_value=brush_icons["blob"]).name = "builtin_brush.Blob"
        layout.operator("wm.tool_set_by_id",text='Layer', icon_value=brush_icons["layer"]).name = "builtin_brush.Layer"
        layout.operator("wm.tool_set_by_id",text='Clay Thumb', icon_value=brush_icons["clay_thumb"]).name = "builtin_brush.Clay Thumb"

# Pie Sculpt Grab - Grab Tool Brushes
class PIE_MT_SculptGrab(Menu):
    bl_idname = "PIE_MT_sculptGrab"
    bl_label = "Pie Sculpt Grab"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5

        layout.operator("wm.tool_set_by_id",text='Grab', icon_value=brush_icons["grab"]).name = "builtin_brush.Grab"
        layout.operator("wm.tool_set_by_id",text='Snake Hook', icon_value=brush_icons["snake_hook"]).name = "builtin_brush.Snake Hook"
        layout.operator("wm.tool_set_by_id",text='Pose', icon_value=brush_icons["pose"]).name = "builtin_brush.Pose"
        layout.operator("wm.tool_set_by_id",text='Nudge', icon_value=brush_icons["nudge"]).name = "builtin_brush.Nudge"
        layout.operator("wm.tool_set_by_id",text='Boundary', icon_value=brush_icons["boundary"]).name = "builtin_brush.Boundary"
        layout.operator("wm.tool_set_by_id",text='Multi-plane Scrape', icon_value=brush_icons["multiplane_scrape"]).name = "builtin_brush.Multi-plane Scrape"
        layout.operator("wm.tool_set_by_id",text='Thumb', icon_value=brush_icons["thumb"]).name = "builtin_brush.Thumb"
        layout.operator("wm.tool_set_by_id",text='Rotate', icon_value=brush_icons["rotate"]).name = "builtin_brush.Rotate"
        layout.operator("wm.tool_set_by_id",text='Thumb', icon_value=brush_icons["thumb"]).name = "builtin_brush.Thumb"
        layout.operator("wm.tool_set_by_id",text='Pinch', icon_value=brush_icons["pinch"]).name = "builtin_brush.Pinch"
        
# Pie Sculpt Smooth (Red) - Smooth tool Brushes
class PIE_MT_SculptSmooth(Menu):
    bl_idname = "PIE_MT_sculptSmooth"
    bl_label = "Pie Sculpt Smooth"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5
        layout.operator("wm.tool_set_by_id",text='Smooth',icon_value=brush_icons["smooth"]).name = "builtin_brush.Smooth"
        layout.operator("wm.tool_set_by_id",text='Scrape', icon_value=brush_icons["scrape"]).name = "builtin_brush.Scrape"
        layout.operator("wm.tool_set_by_id",text='Fill', icon_value=brush_icons["fill"]).name = "builtin_brush.Fill"
        layout.operator("wm.tool_set_by_id",text='Flatten', icon_value=brush_icons["flatten"]).name = "builtin_brush.Flatten"

# Pie Sculpt Mask - Mask & Trim tool Brushes
class PIE_MT_SculptMaskTrim(Menu):
    bl_idname = "PIE_MT_sculptMaskTrim"
    bl_label = "Pie Sculpt Mask"

    def draw(self, context):    
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5
        # Mask Draw tool
        layout.operator("wm.tool_set_by_id",text='Mask', icon_value=brush_icons["mask"]).name = "builtin_brush.Mask"
        layout.operator("wm.tool_set_by_id",text='Draw Face sets', icon_value=brush_icons["draw_face_sets"]).name = "builtin_brush.Draw Face Sets"
        # # Mask Tools
        pie = layout.menu_pie()
        col = pie.column()
        col.menu(PIE_MT_SculptMask.bl_idname,
                text="    Mask", icon_value=brush_icons["border_mask"])
        # # Trim Tools
        col.menu(PIE_MT_SculptTrim.bl_idname,
                text="    Trim", icon_value=brush_icons["box_trim"])
# Sub Menu Sculpt Mask  
class PIE_MT_SculptMask(Menu):
    bl_idname = "PIE_MT_sculptMask"
    bl_label = "Pie Sculpt Mask"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5
        # Mask Tools
        layout.operator("wm.tool_set_by_id",text='Box mask', icon_value=brush_icons["border_mask"]).name = "builtin.box_mask"
        layout.operator("wm.tool_set_by_id",text='Lasso mask', icon_value=brush_icons["lasso_mask"]).name = "builtin.lasso_mask"
        layout.operator("wm.tool_set_by_id",text='Line mask', icon_value=brush_icons["line_mask"]).name = "builtin.line_mask"

# Sub Menu Sculpt Trim
class PIE_MT_SculptTrim(Menu):
    bl_idname = "PIE_MT_sculptTrim"
    bl_label = "Pie Sculpt Trim"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5
        # Trim Tools
        layout.operator("wm.tool_set_by_id",text='Box Trim', icon_value=brush_icons["box_trim"]).name = "builtin.box_trim"
        layout.operator("wm.tool_set_by_id",text='Lasso Trim', icon_value=brush_icons["lasso_trim"]).name = "builtin.lasso_trim"
        layout.operator("wm.tool_set_by_id",text='Line project', icon_value=brush_icons["line_project"]).name = "builtin.line_project"
# Pie Sculpt Extras - More Tool Brushes
class PIE_MT_SculptExtras(Menu):
    bl_idname = "PIE_MT_sculptExtras"
    bl_label = "Pie Sculpt Extras"

    def draw(self, context):
        global brush_icons  
        layout = self.layout
        layout.scale_y = 1.5

        layout.operator("wm.tool_set_by_id",text='Cloth', icon_value=brush_icons["cloth"]).name = "builtin_brush.Cloth"
        layout.operator("wm.tool_set_by_id",text='Slide Relax', icon_value=brush_icons["topology"]).name = "builtin_brush.Slide Relax"
        layout.operator("wm.tool_set_by_id",text='Simplify' , icon_value=brush_icons["simplify"]).name = "builtin_brush.Simplify"
        layout.operator("wm.tool_set_by_id",text='Multires Displacement Eraser', icon_value=brush_icons["displacement_eraser"]).name = "builtin_brush.Multires Displacement Eraser"
        layout.operator("wm.tool_set_by_id",text='Mesh Filter', icon_value=brush_icons["mesh_filter"]).name = "builtin.mesh_filter"
        layout.operator("wm.tool_set_by_id",text='Cloth Filter', icon_value=brush_icons["cloth_filter"]).name = "builtin.cloth_filter"

brush_icons = {}

def create_icons():
    global brush_icons
    icons_directory = bpy.utils.system_resource('DATAFILES', "icons")
    brushes = ["crease", "blob", "draw", "draw_sharp", "clay", "clay_strips","clay_thumb", "inflate","layer",
        "grab", "nudge", "thumb", "snake_hook", "rotate", "pose", "multiplane_scrape", "boundary", "topology", "pinch",
        "flatten", "scrape", "fill", "smooth",
        "simplify", "cloth", "displacement_eraser", "mask", "draw_face_sets",
        "border_mask","lasso_mask","line_mask","box_trim","lasso_trim","line_project","mesh_filter","cloth_filter"
        ]
    transform = ["transform.translate","transform.rotate","transform.resize","transform.transform"]
    for brush in brushes:
        try:
            filename = os.path.join(icons_directory, f"brush.sculpt.{brush}.dat")
            icon_value = bpy.app.icons.new_triangles_from_file(filename)
            brush_icons[brush] = icon_value
        except ValueError:
            filename = os.path.join(icons_directory, f"ops.sculpt.{brush}.dat")
            icon_value = bpy.app.icons.new_triangles_from_file(filename)
            brush_icons[brush] = icon_value
    for transform_ops in transform:
        filename = os.path.join(icons_directory, f"ops.{transform_ops}.dat")
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        brush_icons[transform_ops] = icon_value

def release_icons():
    global brush_icons
    for value in brush_icons.values():
        bpy.app.icons.release(value)


classes = (
    PIE_MT_SculptPie,
    PIE_MT_SculptExtras,
    PIE_MT_SculptGrab,
    PIE_MT_SculptDraw,
    PIE_MT_SculptTrim,
    PIE_MT_SculptMask,
    PIE_MT_SculptMaskTrim,
    PIE_MT_SculptSmooth,
    PIE_OT_SculptSculptDraw
    )

addon_keymaps = []


def register():
    create_icons()

    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Sculpt Pie Menu
        km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'V', 'PRESS') #Replace 'V' with interfere 'W' Faceset shortcut
        kmi.properties.name = "PIE_MT_sculpt"
        addon_keymaps.append((km, kmi))


def unregister():
    release_icons()

    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
