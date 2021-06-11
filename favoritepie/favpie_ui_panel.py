import bpy
from bpy.types import Panel, UIList

from .favpie_menu import *
from .favpie_ops import *
from .favpie_pref import *


class FAVORPIE_UL_Editor(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        ma = slot.material
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if ma:
                layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
            else:
                layout.label(text="", translate=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

    def invoke(self, context, event):
        pass       

class FAVORPIE_UL_Pie(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item,"name",text="",emboss=False)
    
    def invoke(self, context, event):
        pass   
    
class FAVORPIE_PT_panel(Panel):
    bl_label = "Favorite Pie"
    bl_idname = "FAVORPIE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ""
    bl_category = "FPie"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        obj = context.object
        pref = context.preferences.addons[__package__].preferences
        row = col.row(align=True)
        col = row.column(align=True)


        col.prop(pref, "pieSeven", text="Pie One")
        col.prop(pref, "pieThree", text="Pie Two")
        col.prop(pref, "pieEight", text="Pie Three")
        col.prop(pref, "pieOne", text="Pie Four")
        col.prop(pref, "pieTwo", text="Pie Six")
        col.prop(pref, "pieFive", text="Pie Seven")
        col.prop(pref, "pieFour",text="Pie Eight")
        col.prop(pref, "pieSix", text= "Pie Nine")
        
        

        col.label(text="Template UI for later arrangement")
        col.template_list("FAVORPIE_UL_Editor", "", obj, "material_slots", obj, "active_material_index")
