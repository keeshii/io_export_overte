from ..export_params import ExportParams
from .flat_base_entity import FlatBaseEntity

class WebEntity(FlatBaseEntity):

    def __init__(self, obj):
        super().__init__(obj)

    def export(self):
        entity = super().export("Web")

        color = { }
        if (sum(self.obj.overte.color) != 3):
            color = self.get_color(self.obj.overte.color)

        webEntity = {
            "position": self.get_position(),
            "dimensions": self.get_dimentsions(),
            "rotation": self.get_rotation(),
            "queryAACube": self.get_query_aa_cube(),
            "sourceUrl": ExportParams.get_url(self.obj.overte.web_source_url),
        }

        if self.obj.overte.alpha != 1.0:
            webEntity["alpha"] = self.obj.overte.alpha

        if self.obj.overte.web_source_resolution != 30:
            webEntity["dpi"] = self.obj.overte.web_source_resolution

        if self.obj.overte.web_max_fps != 15:
            webEntity["maxFPS"] = self.obj.overte.web_max_fps

        if self.obj.overte.web_input_mode != "touch":
            webEntity["inputMode"] = self.obj.overte.web_input_mode

        if self.obj.overte.web_use_background == False:
            webEntity["useBackground"] = False

        if self.obj.overte.web_focus_highlight == False:
            webEntity["useBackground"] = False

        if self.obj.overte.web_script_url != "":
            webEntity["scriptURL"] = self.obj.overte.web_script_url

        if self.obj.overte.web_user_agent != ExportParams.default_user_agent:
            webEntity["userAgent"] = self.obj.overte.web_user_agent

        return {**entity, **webEntity, **color}

    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "web_source_url")
        row = box.row()
        row.prop(self.obj.overte, "web_source_resolution")
        row = box.row()
        row.prop(self.obj.overte, "color")
        row = box.row()
        row.prop(self.obj.overte, "alpha")
        row = box.row()
        row.prop(self.obj.overte, "web_use_background")
        row = box.row()
        row.prop(self.obj.overte, "web_max_fps")
        row = box.row()
        row.prop(self.obj.overte, "web_input_mode")
        row = box.row()
        row.prop(self.obj.overte, "web_focus_highlight")
        row = box.row()
        row.prop(self.obj.overte, "web_script_url")
        row = box.row()
        row.prop(self.obj.overte, "web_user_agent")

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)
