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
    "name": "Hotkey: 'V'",
    "description": "Sculpt Brush Menu",
    "author": "pitiwazou, meta-androcto",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "W key",
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


# Pie Sculp Pie Menus - W
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
        # Moved to Draw group
        # pie.operator("sculpt.sculptraw",
        #             text="    Draw", icon_value=brush_icons["draw"])
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
        pie.menu(PIE_MT_SculptMask.bl_idname,
                text="    Mask", icon_value=brush_icons["mask"])

        ## Moved to Draw group
        # pie.operator("paint.brush_select",
        #             text="    Inflate/Deflate", icon_value=brush_icons["inflate"]).sculpt_tool = 'INFLATE'
        ## 3 - BOTTOM - RIGHT
        pie.menu(PIE_MT_SculptExtras.bl_idname,
                text="    More",icon_value=brush_icons["cloth"])

# Pie Sculpt Draw - Draw tool brushes
class PIE_MT_SculptDraw(Menu):
    bl_idname = "PIE_MT_sculptDraw"
    bl_label = "Pie Sculpt Draw"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5
        layout.operator("paint.brush_select",
                    text="    Clay", icon_value=brush_icons["clay"]).sculpt_tool = 'CLAY'
        layout.operator("paint.brush_select",
                        text="    Inflate/Deflate", icon_value=brush_icons["inflate"]).sculpt_tool = 'INFLATE'
        layout.operator("paint.brush_select",
                    text="    Blob", icon_value=brush_icons["blob"]).sculpt_tool = 'BLOB'
        layout.operator("paint.brush_select",
                    text="    Layer", icon_value=brush_icons["layer"]).sculpt_tool = 'LAYER'
        layout.operator("paint.brush_select",
                    text="    Clay Thumb", icon_value=brush_icons["clay"]).sculpt_tool = 'CLAY_THUMB'

# Pie Sculpt Mask - Mask tool Brushes
class PIE_MT_SculptMask(Menu):
    bl_idname = "PIE_MT_sculptMask"
    bl_label = "Pie Sculpt Mask"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5
        
        layout.operator("paint.brush_select", text='    Mask',
                        icon_value=brush_icons["mask"]).sculpt_tool = 'MASK'
        layout.operator("paint.brush_select", text='    Face sets',
                        icon_value=brush_icons["draw_face_sets"]).sculpt_tool = 'DRAW_FACE_SETS'
        layout.operator("view3d.select_box", text='    Box Mask')
        layout.operator("paint.mask_lasso_gesture", text='  Lasso Mask')

# Pie Sculpt Extras - More Tool Brushes
class PIE_MT_SculptExtras(Menu):
    bl_idname = "PIE_MT_sculptExtras"
    bl_label = "Pie Sculpt Extras"

    def draw(self, context):
        global brush_icons  
        layout = self.layout
        layout.scale_y = 1.5

        layout.operator("paint.brush_select", text='    Cloth',
                        icon_value=brush_icons["cloth"]).sculpt_tool = 'CLOTH'
        layout.operator("paint.brush_select", text='    Simplify',
                        icon_value=brush_icons["simplify"]).sculpt_tool = 'SIMPLIFY'
        layout.operator("paint.brush_select", text='    Slide Relax',
                        icon_value=brush_icons["topology"]).sculpt_tool = 'TOPOLOGY'
    
# Pie Sculpt Grab - Grab Tool Brushes
class PIE_MT_SculptGrab(Menu):
    bl_idname = "PIE_MT_sculptGrab"
    bl_label = "Pie Sculpt Grab"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5

        layout.operator("paint.brush_select",
                        text='    Grab', icon_value=brush_icons["grab"]).sculpt_tool = 'GRAB'
        layout.operator("paint.brush_select",
                        text='    Snakehook', icon_value=brush_icons["snake_hook"]).sculpt_tool = 'SNAKE_HOOK'
        layout.operator("paint.brush_select",
                        text='    Pose', icon_value=brush_icons["pose"]).sculpt_tool = 'POSE'
        layout.operator("paint.brush_select",
                        text='    Nudge', icon_value=brush_icons["nudge"]).sculpt_tool = 'NUDGE'
        layout.operator("paint.brush_select", text='    Multi-plane Scrape',
                        icon_value=brush_icons["multiplane_scrape"]).sculpt_tool = 'MULTIPLANE_SCRAPE'
        layout.operator("paint.brush_select",
                        text='    Thumb', icon_value=brush_icons["thumb"]).sculpt_tool = 'THUMB'
        layout.operator("paint.brush_select",
                        text='    Rotate', icon_value=brush_icons["rotate"]).sculpt_tool = 'ROTATE'
        layout.operator("paint.brush_select", text='    Pinch/Magnify',
                        icon_value=brush_icons["pinch"]).sculpt_tool = 'PINCH'
        
# Pie Sculpt Smooth (Red) - Red tool Brushes
class PIE_MT_SculptSmooth(Menu):
    bl_idname = "PIE_MT_sculptSmooth"
    bl_label = "Pie Sculpt Smooth"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5

        layout.operator("paint.brush_select", text='    Smooth',
                        icon_value=brush_icons["smooth"]).sculpt_tool = 'SMOOTH'
        layout.operator("paint.brush_select", text='    Flatten',
                        icon_value=brush_icons["flatten"]).sculpt_tool = 'FLATTEN'
        layout.operator("paint.brush_select", text='    Scrape/Peaks',
                        icon_value=brush_icons["scrape"]).sculpt_tool = 'SCRAPE'
        layout.operator("paint.brush_select", text='    Fill/Deepen',
                        icon_value=brush_icons["fill"]).sculpt_tool = 'FILL'
            
brush_icons = {}

def create_icons():
    global brush_icons
    icons_directory = bpy.utils.system_resource('DATAFILES', "icons")
    brushes = ["crease", "blob", "smooth", "draw", "clay", "clay_strips","clay_thumb", "inflate", "grab",
        "nudge", "thumb", "snake_hook", "rotate", "pose", "flatten", "scrape", "fill", "pinch",
        "layer", "simplify", "topology", "multiplane_scrape", "cloth", "mask","draw_face_sets"]
    for brush in brushes:
        filename = os.path.join(icons_directory, f"brush.sculpt.{brush}.dat")
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        brush_icons[brush] = icon_value


def release_icons():
    global brush_icons
    for value in brush_icons.values():
        bpy.app.icons.release(value)

classes = (
    PIE_MT_SculptPie,
    PIE_MT_SculptExtras,
    PIE_MT_SculptGrab,
    PIE_MT_SculptDraw,
    PIE_MT_SculptMask,
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
        kmi = km.keymap_items.new('wm.call_menu_pie', 'V', 'PRESS')
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
