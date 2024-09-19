bl_info = {
    "name": "Godot Workflow",
    "blender": (4, 2, 0),
    "category": "Object",
    "version": (0, 1),
    "author": "Kotobukid",
    "description": "Support workflow for Godot Engine",
}

import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty


class ExportCustomPattern(bpy.types.Operator):
    """Export as GLTF format"""
    bl_idname = "export.custom_pattern"
    bl_label = "Export GLTF"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filepath = bpy.data.scenes["Scene"]["export_file_path"]

        revert_to_select = []
        revert_to_deselect = []

        if filepath:
            for obj in bpy.data.objects:
                if obj['export target']:
                    if not obj.select_get():
                        revert_to_deselect.append(obj.name)

                    obj.select_set(True)

                else:
                    if obj.select_get():
                        revert_to_select.append(obj.name)

                    obj.select_set(False)
            export_pattern1(filepath)

            for name in revert_to_deselect:
                bpy.data.objects[name].select_set(False)
            for name in revert_to_select:
                bpy.data.objects[name].select_set(True)
        else:
            pass
        return {'FINISHED'}


class SimpleFileBrowserOperator(Operator):
    """Set filename to export on clicking 'Export GLTF' button"""
    bl_idname = "wm.file_selector"
    bl_label = "Select File"

    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        print("Selected file:", self.filepath)
        bpy.data.scenes["Scene"]["export_file_path"] = self.filepath

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OBJECT_OT_set_export_target(bpy.types.Operator):
    """Set 'export target' custom property to every object"""
    bl_idname = "object.set_export_target"
    bl_label = "Initialize for Godot ready"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 関数の内容はここに記述する

        objects = bpy.data.objects

        for o in objects:
            if 'export target' in o:
                pass
            else:
                o['export target'] = False

        self.report({'INFO'}, "Initialize completed.")

        bpy.context.area.tag_redraw()

        return {'FINISHED'}


class OBJECT_OT_make_colonly(bpy.types.Operator):
    """Mark current object as CollisionShape on imported by Godot"""
    bl_idname = "object.make_colonly"
    bl_label = "Toggle '-colonly'"
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

        layout.operator("wm.file_selector", text="Set filename to export")
        layout.operator("export.custom_pattern")


# アドオンの登録
def register():
    bpy.utils.register_class(ExportCustomPattern)
    bpy.utils.register_class(SimpleFileBrowserOperator)
    bpy.utils.register_class(OBJECT_OT_set_export_target)
    bpy.utils.register_class(OBJECT_OT_make_colonly)
    bpy.utils.register_class(OBJECT_PT_godot_workflow_panel)


# アドオンの登録解除
def unregister():
    bpy.utils.unregister_class(ExportCustomPattern)
    bpy.utils.unregister_class(SimpleFileBrowserOperator)
    bpy.utils.unregister_class(OBJECT_OT_set_export_target)
    bpy.utils.unregister_class(OBJECT_OT_make_colonly)
    bpy.utils.unregister_class(OBJECT_PT_godot_workflow_panel)


# file_type = "GLB" # "GLB"
file_type = "GLTF_SEPARATE"  # "GLB"


def export_pattern1(filename):
    bpy.ops.export_scene.gltf(
        # filepath=r"C:\sample_export\aaa",
        filepath=filename,
        check_existing=True,
        export_import_convert_lighting_mode='SPEC',
        gltf_export_id="",
        export_use_gltfpack=False,
        export_gltfpack_tc=True,
        export_gltfpack_tq=8,
        export_gltfpack_si=1,
        export_gltfpack_sa=False,
        export_gltfpack_slb=False,
        export_gltfpack_vp=14,
        export_gltfpack_vt=12,
        export_gltfpack_vn=8,
        export_gltfpack_vc=8,
        export_gltfpack_vpi='Integer',
        export_gltfpack_noq=True,
        export_format=file_type,
        ui_tab='GENERAL',
        export_copyright="",
        export_image_format='AUTO',
        export_image_add_webp=False,
        export_image_webp_fallback=False,
        export_texture_dir="",
        export_jpeg_quality=75,
        export_image_quality=75,
        export_keep_originals=False,
        export_texcoords=True,
        export_normals=True,
        export_gn_mesh=False,
        export_draco_mesh_compression_enable=False,
        export_draco_mesh_compression_level=6,
        export_draco_position_quantization=14,
        export_draco_normal_quantization=10,
        export_draco_texcoord_quantization=12,
        export_draco_color_quantization=10,
        export_draco_generic_quantization=12,
        export_tangents=False,
        export_materials='EXPORT',
        export_unused_images=False,
        export_unused_textures=False,
        export_vertex_color='MATERIAL',
        export_all_vertex_colors=True,
        export_active_vertex_color_when_no_material=True,
        export_attributes=False,
        use_mesh_edges=False,
        use_mesh_vertices=False,
        export_cameras=False,
        use_selection=True,
        use_visible=False,
        use_renderable=False,
        use_active_collection_with_nested=True,
        use_active_collection=False,
        use_active_scene=False,
        collection="",
        at_collection_center=False,
        export_extras=False,
        export_yup=True,
        export_apply=False,
        export_shared_accessors=False,
        export_animations=True,
        export_frame_range=False,
        export_frame_step=1,
        export_force_sampling=True,
        export_pointer_animation=False,
        export_animation_mode='ACTIONS',
        export_nla_strips_merged_animation_name="Animation",
        export_def_bones=False,
        export_hierarchy_flatten_bones=False,
        export_hierarchy_flatten_objs=False,
        export_armature_object_remove=False,
        export_leaf_bone=False,
        export_optimize_animation_size=True,
        export_optimize_animation_keep_anim_armature=True,
        export_optimize_animation_keep_anim_object=False,
        export_optimize_disable_viewport=False,
        export_negative_frame='SLIDE',
        export_anim_slide_to_zero=False,
        export_bake_animation=False,
        export_anim_single_armature=True,
        export_reset_pose_bones=True,
        export_current_frame=False,
        export_rest_position_armature=True,
        export_anim_scene_split_object=True,
        export_skins=True,
        export_influence_nb=4,
        export_all_influences=False,
        export_morph=True,
        export_morph_normal=True,
        export_morph_tangent=False,
        export_morph_animation=True,
        export_morph_reset_sk_data=True,
        export_lights=False,
        export_try_sparse_sk=True,
        export_try_omit_sparse_sk=False,
        export_gpu_instances=False,
        export_action_filter=False,
        export_convert_animation_pointer=False,
        export_nla_strips=True,
        export_original_specular=False,
        will_save_settings=False,
        export_hierarchy_full_collections=False,
        export_extra_animations=False,
        filter_glob="*.glb"
    )


if __name__ == "__main__":
    register()
