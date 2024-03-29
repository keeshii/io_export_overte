import os
import bpy
import json

from ..export_params import ExportParams
from .model_entity import ModelEntity

class CustomModelEntity(ModelEntity):

    def __init__(self, obj):
        super().__init__(obj)
        self.file_name = self.obj.name if self.obj.overte.model_file == "" else self.obj.overte.model_file
        self.modelUrl = ExportParams.models_path + self.file_name + '.glb'

    def get_material_entities(self):
        if ExportParams.use_fst:
            return []
        return super().get_material_entities()

    def generateFstFile(self, output_dir):
        materials = super().get_material_entities()
        if len(materials) == 0:
            return False

        # make sure the output directory exists
        modelsPath = output_dir + '/' + ExportParams.models_path
        os.makedirs(modelsPath, exist_ok=True)
        filepath = modelsPath + self.file_name + '.fst'

        lines = []
        lines.append('filename = ' + self.file_name + '.glb')

        materialMap = {}
        for material in materials:
            material.generate(output_dir, modelsPath)
            matdata = material.generated_data
            materialMap['[mat::' + material.obj.name + ']'] = matdata

        lines.append("materialMap = " + json.dumps(materialMap))
        content = "\n".join(lines) + "\n"

        f = open(filepath, 'w', encoding='utf-8')
        f.write(content)
        f.close()
        return True

    def generate(self, output_dir):
        # Already generated by an another entity, skip
        if self.file_name in ExportParams.models_dict:
            self.modelUrl = ExportParams.models_dict[self.file_name]
            return

        if ExportParams.use_fst and self.generateFstFile(output_dir):
            self.modelUrl = ExportParams.models_path + self.file_name + '.fst'

        # Mark as generated
        ExportParams.models_dict[self.file_name] = self.modelUrl

        # make sure the output directory exists
        os.makedirs(output_dir + '/' + ExportParams.models_path, exist_ok=True)
        filepath = output_dir + '/' + ExportParams.models_path + self.file_name + '.glb'

        if not bpy.context.object is None and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode = 'OBJECT')

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
        row.label(text="modelUrl: " + self.file_name + '.glb')
        row = box.row()
        row.prop(self.obj.overte, "model_file")
        self.draw_model_panel(box)

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)
