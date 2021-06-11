import bpy
from bpy.props import (BoolProperty, CollectionProperty, IntProperty,
                       PointerProperty, StringProperty)
from bpy.types import Operator, Panel, PropertyGroup, UIList

# -------------------------------------------------------------------
#   Properties
# -------------------------------------------------------------------

class CUSTOM_ObjectProps(PropertyGroup):
    #obj_idx: IntProperty()
    obj_ref: PointerProperty(
        name="Object",
        type=bpy.types.Object
        )

class CUSTOM_NameProps(PropertyGroup):
    active_obj_index: IntProperty()
    object_collection: CollectionProperty(
        name = "Object Collection",
        type = CUSTOM_ObjectProps
        )

class CUSTOM_SceneProps(PropertyGroup):
    active_user_index: IntProperty()
    user_collection: CollectionProperty(
        name = "Name Collection",
        type = CUSTOM_NameProps)
                
# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class CUSTOM_OT_AddOperator(Operator):
    """Tooltip"""
    bl_idname = "scene.ctm_add_operator"
    bl_label = "Simple Add Operator"

    def execute(self, context):
        scn = context.scene
        custom = scn.ctm
        
        # Clear name collection
        #custom.user_collection.clear()
        
        """ Add user item """
        my_user = custom.user_collection.add()
        
        from random import choice
        my_user.name = choice(("Bob", "Lucy", "John", "Anne", "Sophie"))
                
        """ Add all objects in the scene """
        # Clear object collection
        #my_user.object_collection.clear()
        
        for obj in scn.objects:
            my_obj = my_user.object_collection.add()
            my_obj.name = "{}_{}".format(my_user.name, obj.name)
            my_obj.obj_ref = obj
        
        """ Set active index of both lists to the last item """
        custom.active_user_index = len(custom.user_collection)-1
        my_user.active_obj_index = len(my_user.object_collection)-1
        
        return {'FINISHED'}


class CUSTOM_OT_PrintOperator(Operator):
    """Tooltip"""
    bl_idname = "scene.ctm_print_operator"
    bl_label = "Simple Print Operator"
    
    def execute(self, context):
        scn = context.scene
        custom = scn.ctm
        lookup_dict = {}
        
        """ Print user and attribs """
        for uc, user in enumerate(custom.user_collection):
            print ("User: {}, Name: {}, Ref: {}".format(uc, user.name, user))
            
            """ Print objects and attribs """
            for oc, obj in enumerate(user.object_collection):
                print ("-> Object {}, Ref {}".format(oc, obj))
                lookup_dict.setdefault(user, []).append(obj.obj_ref)
        
        """ In case, dicts are nice """
        print ("\nLookup:", lookup_dict)
        return {'FINISHED'}


class CUSTOM_OT_ClearOperator(Operator):
    """Tooltip"""
    bl_idname = "scene.ctm_clear_operator"
    bl_label = "Simple Clear Operator"
    
    remove_all: BoolProperty(options={'SKIP_SAVE'})
    
    def execute(self, context):
        custom = context.scene.ctm
        
        for uc in custom.user_collection:
            uc.object_collection.clear()
            uc.active_obj_index = -1
        
        if self.remove_all: 
            custom.user_collection.clear()
            custom.active_user_index = -1
            
        return {'FINISHED'}


# -------------------------------------------------------------------
#   Draw
# -------------------------------------------------------------------

class CUSTOM_UL_Main(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.row().prop(item, "name", text="{}".format(index), emboss=False, translate=False, icon="USER")
            
    def invoke(self, context, event):
        pass   

class CUSTOM_UL_Sub(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.6)
        custom_icon = "OUTLINER_OB_{}".format(item.obj_ref.type)
        split.prop(item.obj_ref, "name", text="{}".format(index), emboss=False, translate=False, icon=custom_icon)
        split.label(text="User: {}".format(data.name))
            
    def invoke(self, context, event):
        pass
    

class FAVORPIE_PT_panel(Panel):
    bl_label = "Pie Menu"
    bl_idname = "FAVORPIE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ""
    bl_category = "FavorPie"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        custom = scn.ctm
        
        min_rows = 10
        draw_fac = 0
        user = None
        
        row = layout.row()
        split = layout.split(factor=draw_fac)
        
        split.template_list(
            listtype_name = "CUSTOM_UL_Main", 
            list_id  = "", 
            dataptr = custom, 
            propname = "user_collection", 
            active_dataptr = custom, 
            active_propname = "active_user_index",
            rows = min_rows
            )
        
        if len(custom.user_collection) > 0 and \
            custom.active_user_index != -1:
            
            draw_fac = 0.5
            user = custom.user_collection[custom.active_user_index]
                
            split.template_list(
                listtype_name = "CUSTOM_UL_Sub",
                list_id = "", 
                dataptr = user,
                propname = "object_collection",
                active_dataptr = user,
                active_propname = "active_obj_index",
                rows = min_rows
                )

        layout.row().operator(CUSTOM_OT_PrintOperator.bl_idname, text="Print to Console", icon="CONSOLE")
        
        row = layout.row()
        row.operator(CUSTOM_OT_ClearOperator.bl_idname, text="Remove Users", icon="REMOVE").remove_all = True
        row.operator(CUSTOM_OT_ClearOperator.bl_idname, text="Remove Objects", icon="REMOVE")
        
        layout.row().operator(CUSTOM_OT_AddOperator.bl_idname, text="Add User Entry", icon="USER")
        if user and user.active_obj_index >= 0:
            obj = user.object_collection[user.active_obj_index]    
            layout.label(text="Selection: {} | {}".format(user.name, obj.obj_ref.name))
            

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    CUSTOM_ObjectProps,
    CUSTOM_NameProps,
    CUSTOM_SceneProps,
    CUSTOM_OT_AddOperator,
    CUSTOM_OT_PrintOperator,
    CUSTOM_OT_ClearOperator,
    CUSTOM_UL_Main,
    CUSTOM_UL_Sub,
    FAVORPIE_PT_panel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)  

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    


if __name__ == "__main__":
    register()
