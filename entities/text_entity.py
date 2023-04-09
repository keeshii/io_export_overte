from ..export_params import ExportParams
from .flat_base_entity import FlatBaseEntity

class TextEntity(FlatBaseEntity):

    def __init__(self, obj):
        super().__init__(obj)

    def export(self):
        entity = super().export("Text")

        text_color = { }
        if sum(self.obj.overte.text_color) != 3:
            text_color = {
                "textColor": self.get_color(self.obj.overte.text_color)["color"]
            }

        background_color = self.get_material_color()
        if background_color is None:
            background_color = { }
        else:
            background_color = {
                "backgroundColor": background_color["color"]
            }

        textEntity = {
            "position": self.get_position(),
            "dimensions": self.get_dimensions(),
            "rotation": self.get_rotation(),
            "queryAACube": self.get_query_aa_cube(),
            "text": self.obj.overte.text_value,
        }

        if self.obj.overte.text_alpha != 1.0:
            textEntity["textAlpha"] = self.obj.overte.text_alpha

        if self.obj.overte.text_background_alpha != 1.0:
            textEntity["backgroundAlpha"] = self.obj.overte.text_background_alpha

        if self.obj.overte.text_line_height != 0.06:
            textEntity["lineHeight"] = self.obj.overte.text_line_height

        if self.obj.overte.text_font != "Roboto":
            textEntity["inputMode"] = self.obj.overte.text_font

        if self.obj.overte.text_effect != "none":
            textEntity["textEffect"] = self.obj.overte.text_effect
            textEntity["textEffectColor"] = self.get_color(self.obj.overte.text_effect_color)["color"]
            textEntity["textEffectThickness"] = self.obj.overte.text_effect_thickness

        if self.obj.overte.text_alignment != "left":
            textEntity["alignment"] = self.obj.overte.text_alignment

        if self.obj.overte.text_margin[0] > 0:
            textEntity["topMargin"] = self.obj.overte.text_margin[0]

        if self.obj.overte.text_margin[1] > 0:
            textEntity["rightMargin"] = self.obj.overte.text_margin[1]

        if self.obj.overte.text_margin[2] > 0:
            textEntity["bottomMargin"] = self.obj.overte.text_margin[2]

        if self.obj.overte.text_margin[3] > 0:
            textEntity["leftMargin"] = self.obj.overte.text_margin[3]

        if self.obj.overte.text_unlit == True:
            textEntity["unlit"] = True

        return {**entity, **textEntity, **text_color, **background_color}

    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "text_value")
        row = box.row()
        row.prop(self.obj.overte, "text_color")
        row = box.row()
        row.prop(self.obj.overte, "text_alpha")
        row = box.row()
        row.prop(self.obj.overte, "text_background_alpha")
        row = box.row()
        row.prop(self.obj.overte, "text_line_height")
        row = box.row()
        row.prop(self.obj.overte, "text_font")
        row = box.row()
        row.prop(self.obj.overte, "text_effect")
        row = box.row()
        row.prop(self.obj.overte, "text_effect_color")
        row = box.row()
        row.prop(self.obj.overte, "text_effect_thickness")
        row = box.row()
        row.prop(self.obj.overte, "text_alignment")
        row = box.row()
        row.prop(self.obj.overte, "text_margin")
        row = box.row()
        row.prop(self.obj.overte, "text_unlit")

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)
