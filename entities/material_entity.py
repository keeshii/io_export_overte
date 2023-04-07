from ..export_params import ExportParams
from .base_entity import BaseEntity

class MaterialEntity(BaseEntity):

    def __init__(self, obj):
        super().__init__(obj)

    def get_material(self):
        material = {}
        if self.obj.overte.material_url != '':
            materialData = ExportParams.get_url(self.obj.overte.material_url)
            if self.obj.overte.material_url == 'materialData':
                materialData = self.obj.overte.material_url
            material["materialURL"] = materialData

        if self.obj.overte.material_data != '':
            material["materialData"] = self.obj.overte.material_data

        if self.obj.overte.material_priority != 0:
            material["priority"] = self.obj.overte.material_priority

        if self.obj.overte.material_mapping_mode != 'default':
            material["materialMappingMode"] = self.obj.overte.material_mapping_mode

        if sum(self.obj.overte.material_position) > 0.0:
            material["materialMappingPos"] = {
                "x": self.obj.overte.material_position[0],
                "y": self.obj.overte.material_position[1],
            }

        scale = self.obj.overte.material_scale
        if scale[0] != 1.0 or scale[1] != 1.0:
            material["materialMappingScale"] = {
                "x": scale[0],
                "y": scale[1],
            }

        if self.obj.overte.material_rotation != 0.0:
            material["materialMappingRot"] = self.obj.overte.material_rotation

        if self.obj.overte.material_repeat != True:
            material["materialRepeat"] = self.obj.overte.material_repeat

        return material

    def export(self, parentEntity):
        entity = super().export("Material")
        material = self.get_material()

        materialEntity = {
            "name": parentEntity["name"] + '.' + entity["name"],
            "position": { "x": 0, "y": 0, "z": 0 },
            "rotation": { "x": 0, "y": 0, "z": 0, "w": 1 },
            "queryAACube": parentEntity["queryAACube"],
            "parentID": parentEntity["id"]
        }
        return {**entity, **materialEntity, **material}

    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "material_url")
        row = box.row()
        row.prop(self.obj.overte, "material_data")
        row = box.row()
        row.prop(self.obj.overte, "material_priority")
        row = box.row()
        row.prop(self.obj.overte, "material_mapping_mode")
        row = box.row()
        row.prop(self.obj.overte, "material_position")
        row = box.row()
        row.prop(self.obj.overte, "material_scale")
        row = box.row()
        row.prop(self.obj.overte, "material_rotation")
        row = box.row()
        row.prop(self.obj.overte, "material_repeat")

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_physics_panel(layout)
