import bpy
from bpy.types import Menu

from .favpie_icons import brush_icons, brushes, tools
from .favpie_ops import *
from .favpie_pref import *

toolPrefix = ["builtin_brush","builtin"]
operators = ["wm","sculpt"]

def nameBrush(name):
    if 'Slide Relax' in name:
        name = name.replace('Slide Relax','Topology')
    else:
        pass
    return name

def namePrefix(name): #remove prefix. builtin_brush.Draw => Draw
    if toolPrefix[0] in name:
        name = name.replace(toolPrefix[0]+".","").title()
    elif toolPrefix[1] in name:
        name = name.replace(toolPrefix[1]+".","").title()
    else:
        pass
    return name

def nameIcon(name):
    name = nameBrush(name)
    icon = namePrefix(name).lower()
    icon = icon.replace(" ","_")
    return icon

class FAVORPIE_MT_Sculpt(Menu):
    bl_idname = "FAVORPIE_MT_Sculpt"
    bl_label = "Favorite Pie"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        pie = layout.menu_pie()
        pie.scale_y = 1.2

        pref = context.preferences.addons[__package__].preferences
        pieOne = pref['pieOne']
        pieTwo = pref['pieTwo']
        pieThree = pref['pieThree']
        pieFour = pref['pieFour']
        pieFive = pref['pieFive']
        pieSix = pref['pieSix']
        pieSeven = pref['pieSeven']
        pieEight = pref['pieEight']

        def pieOperator(ops):
            name = str(ops)
            pie.operator("wm.tool_set_by_id",text=namePrefix(name),icon_value=brush_icons[nameIcon(name)]).name = name
            #pie.operator("favpie.empty",text="Empty")
                    

        pieOperator(pieOne) 
        pieOperator(pieTwo) 
        pieOperator(pieThree)
        pieOperator(pieFour)
        pieOperator(pieFive)
        pieOperator(pieSix)
        pieOperator(pieSeven)
        pieOperator(pieEight)

        # pie.operator(tool,text=namePrefix(pieTwo)).name = pieTwo
        # pie.operator(tool,text=namePrefix(pieThree)).name = pieThree
        # pie.operator(tool,text=namePrefix(pieFour)).name = pieFour
        # pie.operator(tool,text=namePrefix(pieFive)).name = pieFive
        # pie.operator(tool,text=namePrefix(pieSix)).name = pieSix
        # pie.operator(tool,text=namePrefix(pieSeven)).name = pieSeven
        # pie.operator(tool,text=namePrefix(pieEight)).name = pieEight
        
        

