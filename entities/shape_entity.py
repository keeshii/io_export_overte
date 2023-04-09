from ..export_params import ExportParams
from .base_entity import BaseEntity
from .material_entity import MaterialEntity

class ShapeBaseEntity(BaseEntity):

    def __init__(self, obj, entityType, shapeType):
        super().__init__(obj)
        self.entityType = entityType
        self.shapeType = shapeType

    def get_material_entity(self):
        try:
            obj = self.obj
            material = obj.material_slots[0].material
            if material.overte.material_url != '':
                return MaterialEntity(material)
        except:
            return None

    def export(self):
        entity = super().export(self.entityType)
        color = self.get_material_color()
        if color is None:
            color = self.get_color([186, 199, 204])

        shapeEntity = {
            "position": self.get_position(),
            "dimensions": self.get_dimensions(),
            "rotation": self.get_rotation(),
            "queryAACube": self.get_query_aa_cube()
        }

        if self.shapeType != None:
            shapeEntity["shape"] = self.shapeType

        if self.obj.overte.alpha != 1.0:
            shapeEntity["alpha"] = self.obj.overte.alpha

        return {**entity, **shapeEntity, **color}

    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "alpha")

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)


# ------------ SHAPE_ENTITIES --------------------

class BoxEntity(ShapeBaseEntity):
    def __init__(self, obj):
        super().__init__(obj, "Box", "Cube")

class QuadEntity(ShapeBaseEntity):
    def __init__(self, obj):
        super().__init__(obj, "Box", "Cube")

class SphereEntity(ShapeBaseEntity):
    def __init__(self, obj):
        super().__init__(obj, "Sphere", None)

class CylinderEntity(ShapeBaseEntity):
    def __init__(self, obj):
        super().__init__(obj, "Shape", "Cylinder")

class ConeEntity(ShapeBaseEntity):
    def __init__(self, obj):
        super().__init__(obj, "Shape", "Cone")
