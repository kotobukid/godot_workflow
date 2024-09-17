bl_info = {
    "name": "Godot Workflow",
    "blender": (4, 2, 0),
    "category": "Object",
    "version": (0, 1),
    "author": "Kotobukid",
    "description": "Support workflow for Godot Engine",
}


import bpy


class OBJECT_OT_set_export_target(bpy.types.Operator):
    """Tooltip for the operator"""
    bl_idname = "object.set_export_target"
    bl_label = "Initialize for Godot ready"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 関数の内容はここに記述する

        objects = bpy.data.objects

        for o in objects:
            print(o)
            if 'export target' in o:
                pass
            else:
                o['export target'] = False

        self.report({'INFO'}, "Initialize completed.")

        bpy.context.area.tag_redraw()

        return {'FINISHED'}


class OBJECT_OT_make_colonly(bpy.types.Operator):
    bl_idname = "object.make_colonly"
    bl_label = "Make colonly"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        name = bpy.context.active_object.name
        postfix = '-colonly'

        if name.endswith(postfix):
            bpy.context.active_object.name = name[:-len(postfix)]
        else:
            bpy.context.active_object.name = name + postfix
        self.report({'INFO'}, "Make colonly completed.")

        return {'FINISHED'}


class OBJECT_PT_godot_workflow_panel(bpy.types.Panel):
    """Creates a Panel in the Object mode toolbar"""
    bl_label = "Godot Workflow"
    bl_idname = "OBJECT_PT_godot_workflow_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Godot"
    bl_context = "objectmode"  # オブジェクトモードで表示する設定

    def draw(self, context):
        layout = self.layout
        # ボタンを作成し、押したときにsample_operatorを呼び出す
        layout.operator("object.set_export_target")
        layout.operator("object.make_colonly")


# アドオンの登録
def register():
    bpy.utils.register_class(OBJECT_OT_set_export_target)
    bpy.utils.register_class(OBJECT_OT_make_colonly)
    bpy.utils.register_class(OBJECT_PT_godot_workflow_panel)


# アドオンの登録解除
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_set_export_target)
    bpy.utils.unregister_class(OBJECT_OT_make_colonly)
    bpy.utils.unregister_class(OBJECT_PT_godot_workflow_panel)


if __name__ == "__main__":
    register()
