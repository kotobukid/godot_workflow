import bpy
import os
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Custom Armature Adder",
    "author": "kotobukid",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Custom Armature",
    "description": "Adds a custom armature with front display and stick visualization",
    "category": "Add Mesh",
}

# SVGアイコンのコードをヒアドキュメントとして定義
icon_svg = '''
<svg viewBox="0 0 20 20 " xmlns="http://www.w3.org/2000/svg" xmlns:bx="https://boxy-svg.com">
    <line style="fill: none; stroke-width: 3px; stroke: rgb(255, 255, 255);" x1="10" y1="14.863" x2="10" y2="5.137"></line>
    <circle style="fill: none; stroke-width: 3px; stroke: rgb(255, 255, 255);" cx="10" cy="16.65" r="1.787"></circle>
    <circle style="fill: none; stroke-width: 3px; stroke: rgb(255, 255, 255);" cx="10" cy="3.35" r="1.787"></circle>
</svg>
'''

# アイコンを保存するディクショナリ
custom_icons = None


def setup_new_armature(object):
    if object.type == 'ARMATURE':
        object.show_in_front = True
        # アーマチュアデータに直接アクセス
        armature_data = object.data
        armature_data.display_type = 'STICK'
        # print(f"新しいArmatureが設定されました: {object.name}")


class ADD_OT_CustomArmature(Operator):
    bl_idname = "object.add_custom_armature"
    bl_label = "Add Custom Armature"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        loc = bpy.context.scene.cursor.location
        bpy.ops.object.armature_add(enter_editmode=False, location=loc)
        armature = context.active_object
        setup_new_armature(armature)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        ADD_OT_CustomArmature.bl_idname,
        text="Custom Armature (Front + Stick)",
        icon_value=custom_icons["custom_icon_add_custom_armature"].icon_id,
    )


def register():
    global custom_icons
    custom_icons = bpy.utils.previews.new()

    # SVGコードから一時ファイルを作成
    icon_path = os.path.join(bpy.app.tempdir, "custom_icon_add_custom_armature.svg")
    with open(icon_path, "w") as f:
        f.write(icon_svg)

    # アイコンを登録
    custom_icons.load("custom_icon_add_custom_armature", icon_path, 'IMAGE')

    register_class(ADD_OT_CustomArmature)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)

    unregister_class(ADD_OT_CustomArmature)
    bpy.types.VIEW3D_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
