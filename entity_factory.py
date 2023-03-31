import bpy

from .entities import LightEntity, BoxEntity, QuadEntity, SphereEntity, CylinderEntity, ConeEntity, ImageEntity, WebEntity, ModelEntity, TextEntity, CustomModelEntity
from .asset_loader import AssetLoader

class EntityFactory(object):

    @staticmethod
    def matchName(obj, name):
        return obj.name == name or obj.name.startswith(name + ".")

    @staticmethod
    def createEntity(obj):
        entity = None

        if obj.type == 'LIGHT':
            light = bpy.data.lights[obj.name]
            if light.type == 'POINT' or light.type == 'SPOT':
                entity = LightEntity(obj, light)

        if obj.type == 'MESH':
            if (EntityFactory.matchName(obj, "Cube") or EntityFactory.matchName(obj, "Box")):
                entity = BoxEntity(obj)
            elif (EntityFactory.matchName(obj, "Plane") or EntityFactory.matchName(obj, "Quad")):
                entity = QuadEntity(obj)
            elif (EntityFactory.matchName(obj, "Icosphere") or EntityFactory.matchName(obj, "Sphere")):
                entity = SphereEntity(obj)
            elif (EntityFactory.matchName(obj, "Cylinder")):
                entity = CylinderEntity(obj)
            elif (EntityFactory.matchName(obj, "Cone")):
                entity = ConeEntity(obj)
            elif EntityFactory.matchName(obj, "Image"):
                entity = ImageEntity(obj)
            elif EntityFactory.matchName(obj, "Web"):
                entity = WebEntity(obj)
            elif EntityFactory.matchName(obj, "Text"):
                entity = TextEntity(obj)
            elif EntityFactory.matchName(obj, "Model"):
                entity = CustomModelEntity(obj)
            elif AssetLoader.getOverteModelUrl(obj):
                entity = ModelEntity(obj)

        return entity

