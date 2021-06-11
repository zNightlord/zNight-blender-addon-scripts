# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Favorite Pie",
    "author" : "zNight (Trung Phạm)",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Interface"
}
import bpy

from .favpie_icons import create_icons, release_icons
from .favpie_menu import *
from .favpie_pref import FAVORPIE_PREF
from .favpie_ui_panel import *

classes = (
    FAVORPIE_PT_panel,
    FAVORPIE_PREF,
    FAVORPIE_MT_Sculpt,
    EMPTY_OT,
    FAVORPIE_UL_Editor,
    FAVORPIE_UL_Pie,
)
addon_keymaps = []
def defaultPie(name,func):
    for prefix in favpie_menu.toolPrefix:
            if prefix == "builtin_brush":
                func = prefix+"."+func
            else:
                pass
    bpy.context.preferences.addons[__package__].preferences[name] = func

def register():
    create_icons()

    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Sculpt Pie Menu
        km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'V', 'PRESS') #Replace 'V' with interfere 'W' Faceset shortcut
        kmi.properties.name = "FAVORPIE_MT_Sculpt"
        addon_keymaps.append((km, kmi))

    # Default
    defaultPie('pieOne',"Scrape")
    defaultPie('pieTwo',"Fill")
    defaultPie('pieThree',"Clay Strips")
    defaultPie('pieFour',"Inflate")
    defaultPie('pieFive',"Snake Hook")
    defaultPie('pieSix',"Pose")
    defaultPie('pieSeven',"Mask")
    defaultPie('pieEight',"Draw Face Sets")

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
