from math import radians, cos, sin
from ..export_params import ExportParams
from .base_entity import BaseEntity

class FlatBaseEntity(BaseEntity):

    def __init__(self, obj):
        super().__init__(obj)

    def get_dimentsions(self):
        d = self.obj.dimensions
        dimensions = {
            "x": d[0] * ExportParams.world_scale,
            "y": d[1] * ExportParams.world_scale,
            "z": 0.01
        }
        return dimensions

    def get_rotation(self):
        r = self.obj.rotation_euler
        cr = cos((r[0] - radians(90)) * 0.5)
        sr = sin((r[0] - radians(90)) * 0.5)
        cp = cos(r[2] * 0.5)
        sp = sin(r[2] * 0.5)
        cy = cos(-r[1] * 0.5)
        sy = sin(-r[1] * 0.5)

        rotation = {
            "x": sr * cp * cy - cr * sp * sy,
            "y": cr * sp * cy + sr * cp * sy,
            "z": cr * cp * sy - sr * sp * cy,
            "w": cr * cp * cy + sr * sp * sy
        }
        return rotation
