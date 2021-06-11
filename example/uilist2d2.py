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

bl_info = {
    "name": "object-uilist-dev",
    "description": "",
    "author": "p2or",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Text Editor",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
from bpy.props import (BoolProperty, CollectionProperty, IntProperty,
                       StringProperty)
from bpy.types import Operator, Panel, PropertyGroup, UIList

# -------------------------------------------------------------------
#   Keyword Operators
# -------------------------------------------------------------------

class SCREENWRITER_OT_keyword_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "keyword.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.keyword_index
        #items = scn.text_marker_list

        try:
            item = scn.keyword[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.keyword) - 1:
                item_next = scn.keyword[idx+1].name
                scn.keyword.move(idx, idx+1)
                scn.keyword_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.keyword_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.keyword[idx-1].name
                scn.keyword.move(idx, idx-1)
                scn.keyword_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.keyword_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.keyword[idx].name)
                scn.keyword_index -= 1
                scn.keyword.remove(idx)
                if bool(context.scene.object):
                    context.scene.object.clear()
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            txt = bpy.context.space_data.text
            text = bpy.data.texts
            term = txt.keyword_searchterm
            if term != '' and len(text) > 0:
                pass
#            if context.object:
#                selection_names = [obj.name for obj in bpy.context.selected_objects]
#                selection_names = []
#                for obj in bpy.context.selected_objects:
                    #selection_names.append(obj.name)
                    
                item = scn.keyword.add()
                item.name = term
                item.key_type = "USER" #TEXT #URLobj.type
                item.key_id = len(scn.keyword)
                scn.keyword_index = len(scn.keyword)-1
#                info = '"%s" added to list' % (item.name)
#                self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}


class SCREENWRITER_OT_keyword_printItems(Operator):
    """Print all items and their properties to the console"""
    bl_idname = "keyword.print_items"
    bl_label = "Print Items to Console"
    bl_description = "Print all items and their properties to the console"
    bl_options = {'REGISTER', 'UNDO'}

    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")

    @classmethod
    def poll(cls, context):
        return bool(context.scene.keyword)

    def execute(self, context):
        scn = context.scene
        if self.reverse_order:
            for i in range(scn.keyword_index, -1, -1):        
                item = scn.keyword[i]
                print ("Name:", item.name,"-",item.key_type,item.key_id)
        else:
            for item in scn.keyword:
                print ("Name:", item.name,"-",item.key_type,item.key_id)
        return{'FINISHED'}


class SCREENWRITER_OT_keyword_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "keyword.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.keyword)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.keyword):
            context.scene.keyword.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}


class SCREENWRITER_OT_keyword_removeDuplicates(Operator):
    """Remove all duplicates"""
    bl_idname = "keyword.remove_duplicates"
    bl_label = "Remove Duplicates"
    bl_description = "Remove all duplicates"
    bl_options = {'INTERNAL'}

    def find_duplicates(self, context):
        """find all duplicates by name"""
        name_lookup = {}
        for c, i in enumerate(context.scene.keyword):
            name_lookup.setdefault(i.name, []).append(c)
        duplicates = set()
        for name, indices in name_lookup.items():
            for i in indices[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))

    @classmethod
    def poll(cls, context):
        return bool(context.scene.keyword)

    def execute(self, context):
        scn = context.scene
        removed_items = []
        # Reverse the list before removing the items
        for i in self.find_duplicates(context)[::-1]:
            scn.keyword.remove(i)
            removed_items.append(i)
        if removed_items:
            scn.keyword_index = len(scn.keyword)-1
            info = ', '.join(map(str, removed_items))
            self.report({'INFO'}, "Removed indices: %s" % (info))
        else:
            self.report({'INFO'}, "No duplicates")
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SCREENWRITER_OT_keyword_selectItems(Operator):
    """Select Items in the Viewport"""
    bl_idname = "keyword.select_items"
    bl_label = "Select Item(s) in Viewport"
    bl_description = "Select Items in the Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    select_all: BoolProperty(
        default=False,
        name="Select all Items of List",
        options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return bool(context.scene.keyword)

    def execute(self, context):
        scn = context.scene
        idx = scn.keyword_index

        try:
            item = scn.keyword[idx]
        except IndexError:
            self.report({'INFO'}, "Nothing selected in the list")
            return{'CANCELLED'}

        obj_error = False
        bpy.ops.object.select_all(action='DESELECT')
        if not self.select_all:
            obj = scn.objects.get(scn.keyword[idx].name, None)
            if not obj: 
                obj_error = True
            else:
                obj.select_set(True)
                info = '"%s" selected in Viewport' % (obj.name)
        else:
            selected_items = []
            unique_objs = set([i.name for i in scn.keyword])
            for i in unique_objs:
                obj = scn.objects.get(i, None)
                if obj:
                    obj.select_set(True)
                    selected_items.append(obj.name)

            if not selected_items: 
                obj_error = True
            else:
                missing_items = unique_objs.difference(selected_items)
                if not missing_items:
                    info = '"%s" selected in Viewport' \
                        % (', '.join(map(str, selected_items)))
                else:
                    info = 'Missing items: "%s"' \
                        % (', '.join(map(str, missing_items)))
        if obj_error: 
            info = "Nothing to select, object removed from scene"
        self.report({'INFO'}, info)    
        return{'FINISHED'}


# -------------------------------------------------------------------
#   Keyword Drawing
# -------------------------------------------------------------------

class SCREENWRITER_UL_keyword_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #split = layout.split(factor=0.3)
        #split.label(text="Index: %d" % (index))
        keyword_icon = "%s" % item.key_type
        #split.prop(item, "name", text="", emboss=False, translate=False, icon=keyword_icon)
        layout.label(text=item.name, icon=keyword_icon) # avoids renaming the item by accident

    def invoke(self, context, event):
        pass  

# -------------------------------------------------------------------
#   Object Operators
# -------------------------------------------------------------------

class SCREENWRITER_OT_objects_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "object.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.object_index

        try:
            item = scn.object[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.object) - 1:
                item_next = scn.object[idx+1].name
                scn.object.move(idx, idx+1)
                scn.object_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.object_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.object[idx-1].name
                scn.object.move(idx, idx-1)
                scn.object_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.object_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.object[idx].name)
                scn.object_index -= 1
                scn.object.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            if context.object:
                selection_names = [obj.name for obj in bpy.context.selected_objects]
                selection_names = []
                for obj in bpy.context.selected_objects:
                    #selection_names.append(obj.name)
                    
                    item = scn.object.add()
                    item.name = obj.name
                    item.obj_type = obj.type
                    item.obj_id = len(scn.object)
                    scn.object_index = len(scn.object)-1
#                info = '"%s" added to list' % (item.name)
#                self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}


class SCREENWRITER_OT_objects_printItems(Operator):
    """Print all items and their properties to the console"""
    bl_idname = "object.print_items"
    bl_label = "Print Items to Console"
    bl_description = "Print all items and their properties to the console"
    bl_options = {'REGISTER', 'UNDO'}

    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")

    @classmethod
    def poll(cls, context):
        return bool(context.scene.object)

    def execute(self, context):
        scn = context.scene
        if self.reverse_order:
            for i in range(scn.object_index, -1, -1):        
                item = scn.object[i]
                print ("Name:", item.name,"-",item.obj_type,item.obj_id)
        else:
            for item in scn.object:
                print ("Name:", item.name,"-",item.obj_type,item.obj_id)
        return{'FINISHED'}


class SCREENWRITER_OT_objects_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "object.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.object)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.object):
            context.scene.object.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}


class SCREENWRITER_OT_objects_removeDuplicates(Operator):
    """Remove all duplicates"""
    bl_idname = "object.remove_duplicates"
    bl_label = "Remove Duplicates"
    bl_description = "Remove all duplicates"
    bl_options = {'INTERNAL'}

    def find_duplicates(self, context):
        """find all duplicates by name"""
        name_lookup = {}
        for c, i in enumerate(context.scene.object):
            name_lookup.setdefault(i.name, []).append(c)
        duplicates = set()
        for name, indices in name_lookup.items():
            for i in indices[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))

    @classmethod
    def poll(cls, context):
        return bool(context.scene.object)

    def execute(self, context):
        scn = context.scene
        removed_items = []
        # Reverse the list before removing the items
        for i in self.find_duplicates(context)[::-1]:
            scn.object.remove(i)
            removed_items.append(i)
        if removed_items:
            scn.object_index = len(scn.object)-1
            info = ', '.join(map(str, removed_items))
            self.report({'INFO'}, "Removed indices: %s" % (info))
        else:
            self.report({'INFO'}, "No duplicates")
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SCREENWRITER_OT_objects_selectItems(Operator):
    """Select Items in the Viewport"""
    bl_idname = "object.select_items"
    bl_label = "Select Item(s) in Viewport"
    bl_description = "Select Items in the Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    select_all: BoolProperty(
        default=False,
        name="Select all Items of List",
        options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return bool(context.scene.object)

    def execute(self, context):
        scn = context.scene
        idx = scn.object_index

        try:
            item = scn.object[idx]
        except IndexError:
            self.report({'INFO'}, "Nothing selected in the list")
            return{'CANCELLED'}

        obj_error = False
        bpy.ops.object.select_all(action='DESELECT')
        if not self.select_all:
            obj = scn.objects.get(scn.object[idx].name, None)
            if not obj: 
                obj_error = True
            else:
                obj.select_set(True)
                info = '"%s" selected in Viewport' % (obj.name)
        else:
            selected_items = []
            unique_objs = set([i.name for i in scn.object])
            for i in unique_objs:
                obj = scn.objects.get(i, None)
                if obj:
                    obj.select_set(True)
                    selected_items.append(obj.name)

            if not selected_items: 
                obj_error = True
            else:
                missing_items = unique_objs.difference(selected_items)
                if not missing_items:
                    info = '"%s" selected in Viewport' \
                        % (', '.join(map(str, selected_items)))
                else:
                    info = 'Missing items: "%s"' \
                        % (', '.join(map(str, missing_items)))
        if obj_error: 
            info = "Nothing to select, object removed from scene"
        self.report({'INFO'}, info)    
        return{'FINISHED'}


# -------------------------------------------------------------------
#   Object Drawing
# -------------------------------------------------------------------

class SCREENWRITER_UL_objects_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scn = context.scene
        idx = scn.keyword_index
#        print(idx)
#        if int(idx) > 0:
        if scn.keyword[idx].name is not None:
            #split = layout.split(factor=0.3)
            #split.label(text="Index: %d" % (index))
            object_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=object_icon)
            layout.label(text=item.name, icon=object_icon) # avoids renaming the item by accident

    def invoke(self, context, event):
        pass   


class SCREENWRITER_PT_objectList(Panel):
    """Assign Objects to Screenplay Keywords"""
    bl_idname = 'TEXT_PT_my_panel'
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_label = "Assign Objects to Screenplay Keywords"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        txt = bpy.context.space_data.text
                
        col = layout.column(align=True)   
        row = col.row(align=True)
        row.label(text="Keyword")
        row.label(text="Object")        

        row = col.row(align=True)

        row.prop(txt, 'keyword_searchterm', text='')

        row.separator()
        ob = []
        row = row.row()
        #row = row.box()
        if len(context.selected_objects):
            for obj in bpy.context.selected_objects:
                ob.append(obj.name+" ")                 
            ob = ''.join(ob)
                
            row.label( text=ob)
              
        tworow = col.row(align=True)
        rows = 10
        row = tworow.row()

        col = row.column(align=True)
        col.operator("keyword.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("keyword.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("keyword.list_action", icon='URL', text="").action = 'UP'
        col.operator("keyword.list_action", icon='COMMUNITY', text="").action = 'DOWN'
        col.separator()
        col.operator("keyword.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("keyword.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
        col.separator()
        col.operator("keyword.remove_duplicates", icon="GHOST_ENABLED", text="")
        col.operator("keyword.clear_list", icon="X", text="")

        row.template_list("SCREENWRITER_UL_keyword_items", "", scn, "keyword", scn, "keyword_index", rows=rows)

        rows = 10
        row = tworow.row()
        row.template_list("SCREENWRITER_UL_objects_items", "", scn, "object", scn, "object_index", rows=rows)

        col = row.column(align=True)
        col.operator("object.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("object.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("object.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("object.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
        col.separator()
        col.operator("object.remove_duplicates", icon="GHOST_ENABLED", text="")
        col.operator("object.clear_list", icon="X", text="")

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("object.print_items", icon="LINENUMBERS_ON") #LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("object.select_items", icon="VIEW3D", text="Select Item")
        row.operator("object.select_items", icon="GROUP", text="Select all Items").select_all = True
        row = col.row(align=True)


# -------------------------------------------------------------------
#   Keyword Collection
# -------------------------------------------------------------------

class SCREENWRITER_keywordCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    key_type: StringProperty()
    key_id: IntProperty()
    

# -------------------------------------------------------------------
#   Object Collection
# -------------------------------------------------------------------

class SCREENWRITER_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    obj_type: StringProperty()
    obj_id: IntProperty()


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    SCREENWRITER_OT_objects_actions,
    SCREENWRITER_OT_objects_printItems,
    SCREENWRITER_OT_objects_clearList,
    SCREENWRITER_OT_objects_removeDuplicates,
    SCREENWRITER_OT_objects_selectItems,
    SCREENWRITER_UL_objects_items,
    SCREENWRITER_objectCollection,
    
    SCREENWRITER_OT_keyword_actions,
    SCREENWRITER_OT_keyword_printItems,
    SCREENWRITER_OT_keyword_clearList,
    SCREENWRITER_OT_keyword_removeDuplicates,
    SCREENWRITER_OT_keyword_selectItems,
    SCREENWRITER_UL_keyword_items,
    SCREENWRITER_keywordCollection,
    
    SCREENWRITER_PT_objectList,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Custom scene properties
    bpy.types.Scene.object = CollectionProperty(type=SCREENWRITER_objectCollection)
    bpy.types.Scene.object_index = IntProperty()
    bpy.types.Scene.keyword = CollectionProperty(type=SCREENWRITER_keywordCollection)
    bpy.types.Scene.keyword_index = IntProperty()
    bpy.types.Scene.wordlink = CollectionProperty(type=SCREENWRITER_keywordCollection)
    bpy.types.Scene.wordlink_index = IntProperty()
    
    bpy.types.Text.keyword_searchterm = StringProperty(
        description="Search Terms for adding Assets")
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.keyword
    del bpy.types.Scene.keyword_index
    del bpy.types.Scene.object
    del bpy.types.Scene.object_index
    
    del bpy.types.Text.text_marker_searchterm


if __name__ == "__main__":
    register()
