from ..export_params import ExportParams
from .base_entity import BaseEntity

class LightEntity(BaseEntity):

    def __init__(self, obj, light):
        super().__init__(obj)
        self.light = light

    def get_dimentsions(self):
        scale = self.obj.scale
        # Lights have a fixed dimensions of 4x4x4
        dimensions = {
            "x": 4.0 * scale[0] * ExportParams.world_scale,
            "y": 4.0 * scale[2] * ExportParams.world_scale,
            "z": 4.0 * scale[1] * ExportParams.world_scale
        }
        return dimensions

    def export(self):
        entity = super().export("Light")

        color = { }
        if sum(self.light.color) != 3:
            color = self.get_color(self.light.color)

        lightEntity = {
            "position": self.get_position(),
            "dimensions": self.get_dimentsions(),
            "rotation": self.get_rotation(),
            "queryAACube": self.get_query_aa_cube(),
            "intensity": self.obj.overte.light_intensity,
            "exponent": self.obj.overte.light_exponent,
            "cutoff": self.obj.overte.light_cut_off,
            "falloffRadius": self.obj.overte.light_fall_off_radius
        }

        if self.light.type == 'SPOT':
            lightEntity["isSpotlight"] = True

        return {**entity, **lightEntity, **color}

    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "light_intensity")
        row = box.row()
        row.prop(self.obj.overte, "light_fall_off_radius")
        row = box.row()
        row.prop(self.obj.overte, "light_exponent")
        row = box.row()
        row.prop(self.obj.overte, "light_cut_off")

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)
