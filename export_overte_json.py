import bpy
import os
import json
import time

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator

from .asset_loader import AssetLoader
from .entities import BaseEntity, ZoneEntity
from .entity_factory import EntityFactory
from .export_params import ExportParams

class ExportOverteJson(Operator, ExportHelper):
    """Exports scene to Overte json world file"""
    bl_idname = "export_scene.overte"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export"

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    def append_path_from_object(self, obj, paths):
        path_name = obj.name[5:] if len(obj.name) > 4 else obj.name[4:]

        if path_name == 'default':
            path_name = ''

        entity = BaseEntity(obj)
        p = entity.get_position()
        r = entity.get_rotation()

        position = str(p["x"]) + ',' + str(p["y"]) + ',' + str(p["z"])
        rotation = str(r["x"]) + ',' + str(r["y"]) + ',' + str(r["z"]) + ',' + str(r["w"])

        paths["/" + path_name] = "/" + position + "/" + rotation

    def process_object(self, obj, entities, parent):
        for child in obj.children:
            if child.type != 'MESH' and child.type != 'LIGHT':
                continue

            entity = EntityFactory.createEntity(child)
            if entity:
                entity.generate(os.path.dirname(self.filepath))
                material = entity.get_material_entity()
                position = entity.get_relative_postion(obj)
                entity = { **entity.export(), **{ "position": position } }
                entity["parentID"] = parent["id"]
                entities.append(entity)
                if material:
                    material = material.export(entity)
                    entities.append(material)

                self.process_object(child, entities, entity)

    def process_collection(self, col, entities, zone):
        if EntityFactory.matchName(col, "Zone"):
            zone = ZoneEntity(col).export()
            entities.append(zone)

        for obj in col.objects:
            if obj.parent or (obj.type != 'MESH' and obj.type != 'LIGHT'):
                continue

            entity = EntityFactory.createEntity(obj)
            if entity:
                entity.generate(os.path.dirname(self.filepath))
                material = entity.get_material_entity()
                entity = entity.export()
                if zone:
                    entity["position"]["x"] -= zone["position"]["x"]
                    entity["position"]["y"] -= zone["position"]["y"]
                    entity["position"]["z"] -= zone["position"]["z"]
                    entity["parentID"] = zone["id"]
                entities.append(entity)
                if material:
                    material = material.export(entity)
                    entities.append(material)

                self.process_object(obj, entities, entity)

        for child in col.children:
            self.process_collection(child, entities, zone)

    def process_paths(self, col, paths):
        for obj in col.objects:
            if obj.type == 'MESH' and EntityFactory.matchName(obj, "Path"):
                self.append_path_from_object(obj, paths)

        for child in col.children:
            self.process_paths(child, paths)

    def write_overte_json(self, context, filepath):
        print("running write_overte_json...")
        AssetLoader.find_all_models()
        ExportParams.current_time = int(time.time() * 1000000)
        
        world = bpy.context.scene.world
        ExportParams.domain_url = world.overte.domain_url
        ExportParams.world_scale = world.overte.world_scale
        ExportParams.models_path = world.overte.models_path

        entities = []
        self.process_collection(bpy.context.scene.collection, entities, None)

        paths = { }
        self.process_paths(bpy.context.scene.collection, paths)

        data = {
            "DataVersion": 0,
            "Entities": entities,
            "Id": BaseEntity(None).get_uuid(),
            "Version": 133
        }

        if len(paths) > 0:
            data["Paths"] = paths

        f = open(filepath, 'w', encoding='utf-8')
        f.write(json.dumps(data, indent=4))
        f.close()

        return {'FINISHED'}

    def execute(self, context):
        return self.write_overte_json(context, self.filepath)
