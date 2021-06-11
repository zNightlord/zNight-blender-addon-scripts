import bpy
from bpy.types import Operator


class EMPTY_OT(Operator):
    bl_idname = "favpie.empty"
    bl_label = "Empty"

    def execute(self, context):
        self.report({'INFO'}, "Empty pie menu.")
        return {'FINISHED'}


