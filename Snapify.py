bl_info = {
    "name": "Snapify",
    "author": "Herwork",
    "version": (1, 0),
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




def main(context, targ, mode):        
    if mode == 0: 
        for i in bpy.context.object.pose.bones:
            try:
                bpy.data.objects[targ].pose.bones[i.name]
            except:
                continue
            i.constraints.new('COPY_LOCATION')
            i.constraints.new('COPY_ROTATION')
            i.constraints['Copy Location'].target = bpy.data.objects[targ]
            i.constraints['Copy Location'].subtarget = i.name
            i.constraints['Copy Rotation'].target = bpy.data.objects[targ]
            i.constraints['Copy Rotation'].subtarget = i.name

    if mode == 1:
        for i in bpy.context.object.pose.bones:
            try:
                i.constraints.remove(i.constraints["Copy Location"])
                i.constraints.remove(i.constraints["Copy Rotation"])
            except:
                continue



class addArm(bpy.types.Operator):
    """A button that does stuff.."""
    bl_idname = "rig.snap"
    bl_label = "Snap!"
    
    def execute(self, context):
        scene = context.scene
        targ = scene.mychosenObject
        print(targ)
        if targ == None:
            self.report({"ERROR"}, "No player rig found")
        
        try:
            main(context, targ.name, 0)
            return {'FINISHED'}
        except:
            self.report({"ERROR"}, "Object or Armature found")


class removeArm(bpy.types.Operator):
    """A button that does stuff.."""
    bl_idname = "rig.remove"
    bl_label = "Unsnap"
    
    def execute(self, context):
        scene = context.scene
        targ = scene.mychosenObject
        print(targ)
        if targ == None:
            self.report({"ERROR"}, "No player rig found")
        
        try:
            main(context, targ.name, 1)
            return {'FINISHED'}
        except:
            self.report({"ERROR"}, "Object or Armature found")


class TestPanel(bpy.types.Panel):
    bl_label = "Snapify"
    bl_idname = "PT_SnapPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Snapify"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        mytool = scene.my_tool
        
        col = layout.column()
        col.label(text= "Select the player rig", icon= "RESTRICT_SELECT_OFF")
        col.prop(scene, "mychosenObject", text="", expand=True)
        
        row = layout.row()
        row.label(text= "Snap cosmetic to a rig", icon= "COMMUNITY")
        row = layout.row(align=True)
        row.operator("rig.snap", icon="SHADERFX")
        row.operator("rig.remove", icon="LOOP_BACK")


        


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