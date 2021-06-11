import bpy
from bpy.props import CollectionProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences, PropertyGroup


class FavorpieProperty(PropertyGroup):
        pieName: StringProperty(
        )
        pieIndex: IntProperty(
        )


class FAVORPIE_PREF(AddonPreferences):
        bl_idname = __package__

        pieOne: StringProperty(
                name="Pie Four",
        )
        pieTwo: StringProperty(
                name="Pie Six",
        )
        pieThree: StringProperty(
                name="Pie Two",
        )
        pieFour: StringProperty(
                name="Pie Eight",
        )
        pieFive: StringProperty(
                name="Pie Seven",
        )
        pieSix: StringProperty(
                name="Pie Nine",
        )
        pieSeven: StringProperty(
                name="Pie One"
        )
        pieEight: StringProperty(
                name="Pie Three"
        )
        def draw(self, context):
                layout = self.layout
                layout.label(text="Editors")



