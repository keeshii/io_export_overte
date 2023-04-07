from math import radians
from mathutils import Matrix
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

    def get_absolute_rotation(self):
        rot = self.obj.matrix_world.to_euler('XYZ')
        r = rot.to_matrix().to_4x4() @ Matrix.Rotation(radians(-90), 4, 'X').to_4x4()
        return r.to_euler('XYZ')
