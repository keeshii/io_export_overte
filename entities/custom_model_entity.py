import os
import bpy

from ..export_params import ExportParams
from .model_entity import ModelEntity

class CustomModelEntity(ModelEntity):

    def __init__(self, obj):
        super().__init__(obj)
        file_name = self.obj.name if self.obj.overte.model_file == "" else self.obj.overte.model_file
        self.modelUrl = ExportParams.models_path + file_name + '.glb'

    def generate(self, output_dir):
        # make sure the output directory exists
        os.makedirs(output_dir + '/' + ExportParams.models_path, exist_ok=True)
        filepath = output_dir + '/' + self.modelUrl

        bpy.ops.object.select_all(action='DESELECT')
        self.obj.select_set(True)
        bpy.ops.object.duplicate()
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()

        bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format='GLB',
            use_selection=True,
            export_apply=True
        )
        bpy.ops.object.delete()

    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.label(text="modelUrl: " + self.modelUrl)
        row = box.row()
        row.prop(self.obj.overte, "model_file")
        self.draw_model_panel(box)

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)
