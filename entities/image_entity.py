from ..export_params import ExportParams
from .flat_base_entity import FlatBaseEntity

class ImageEntity(FlatBaseEntity):

    def __init__(self, obj):
        super().__init__(obj)

    def export(self):
        entity = super().export("Image")

        color = { }
        if (sum(self.obj.overte.color) != 3):
            color = self.get_color(self.obj.overte.color)

        subimage = { }
        if sum(self.obj.overte.image_subimage) != 0:
            subimage = {
                "subImage": {
                    "x": self.obj.overte.image_subimage[0],
                    "y": self.obj.overte.image_subimage[1],
                    "width": self.obj.overte.image_subimage[2],
                    "height": self.obj.overte.image_subimage[3]
                }
            }

        imageEntity = {
            "position": self.get_position(),
            "dimensions": self.get_dimensions(),
            "rotation": self.get_rotation(),
            "queryAACube": self.get_query_aa_cube(),
            "imageURL": ExportParams.get_url(self.obj.overte.image_url),
        }

        if self.obj.overte.alpha != 1.0:
            imageEntity["alpha"] = self.obj.overte.alpha

        if self.obj.overte.emissive == True:
            imageEntity["emissive"] = True

        if self.obj.overte.image_keep_aspect == False:
            imageEntity["keepAspectRatio"] = False

        return {**entity, **imageEntity, **color, **subimage}

    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "image_url")
        row = box.row()
        row.prop(self.obj.overte, "color")
        row = box.row()
        row.prop(self.obj.overte, "alpha")
        row = box.row()
        row.prop(self.obj.overte, "emissive")
        row = box.row()
        row.prop(self.obj.overte, "image_subimage")
        row = box.row()
        row.prop(self.obj.overte, "image_keep_aspect")

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)
