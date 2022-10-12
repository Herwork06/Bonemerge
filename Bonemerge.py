bl_info = {
    "name": "Bonemerge",
    "author": "Herwork, hisanimations",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Rigging",
    "description": "Snaps any cosmetics to a player rig",
    "warning": "",
    "doc_url": "",
    "category": "Rigging",
}


import bpy
from bpy.types import Operator, Object, Armature
from bpy.props import FloatVectorProperty, EnumProperty, StringProperty, FloatProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


loc = "BONEMERGE-ATTACH-LOC"
rot = "BONEMERGE-ATTACH-ROT"

def main(context, mode, targ = None):
    #targ = targ.name
    if mode == 0:
        for i in bpy.context.selected_objects:
            if i.name == targ:
                continue
            if i.type == 'MESH':
                if not i.parent:
                    continue
                else:
                    i = i.parent
            
            #i.location = bpy.data.objects[targ].location # for organization
            
            for ii in i.pose.bones:
                try:
                    bpy.data.objects[targ].pose.bones[ii.name]
                except:
                    continue
                    
                try:
                    ii.constraints[loc]
                    pass
                except:
                    ii.constraints.new('COPY_LOCATION').name = loc
                    ii.constraints.new('COPY_ROTATION').name = rot
                
                ii.constraints[loc].target = bpy.data.objects[targ]
                ii.constraints[loc].subtarget = ii.name
                ii.constraints[rot].target = bpy.data.objects[targ]
                ii.constraints[rot].subtarget = ii.name

    if mode == 1:
        for i in bpy.context.selected_objects:
            if i.type == 'MESH':
                if not i.parent:
                    continue
                else:
                    i = i.parent
            for ii in i.pose.bones:
                try:
                    ii.constraints.remove(ii.constraints[loc])
                    ii.constraints.remove(ii.constraints[rot])
                except:
                    continue



class addArm(bpy.types.Operator):
    """Attach cosmetics"""
    bl_idname = "rig.snap"
    bl_label = "Attach"
    bl_options = {'UNDO'} # make undoable
    
    def execute(self, context):
        scene = context.scene
        targ = scene.mychosenObject
        if targ == None:
            self.report({"ERROR"}, "No player rig found")
        
        try:
            main(context, 0, targ.name)
            return {'FINISHED'}
        except:
            self.report({"ERROR"}, "Object or Armature found")


class removeArm(bpy.types.Operator):
    """Detach cosmetics"""
    bl_idname = "rig.remove"
    bl_label = "Detach"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        targ = "justcause"
        
        try:
            main(context, 1) #a target is not needed
            return {'FINISHED'}
        except:
            raise TypeError("you have somehow made an error!")


class TestPanel(bpy.types.Panel):
    bl_label = "Bonemerge"
    bl_idname = "PT_MergePanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Bonemerge"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        #mytool = scene.my_tool - this crashes the addon
        
        col = layout.column()
        col.label(text= "Select the player rig", icon= "RESTRICT_SELECT_OFF")
        col.prop(scene, "mychosenObject", text="", expand=True)
        
        row = layout.row()
        row.label(text= "Snap cosmetic to a rig", icon= "COMMUNITY")
        row = layout.row(align=True)
        row.operator("rig.snap", icon="LINKED")
        row.operator("rig.remove", icon="UNLINKED")


        


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping

classes = [TestPanel, addArm,removeArm]        
        
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.mychosenObject = bpy.props.PointerProperty(
        type=Armature
    )
    
def unregister():
    for cls in classes:
        bpy.utils.register_class(cls)

    del bpy.types.Scene.mychosenObject
    
if __name__ == "__main__":
    register()
