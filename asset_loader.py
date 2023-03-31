import bpy
import os

class AssetLoader(object):
    overteDomainModels = {}

    @staticmethod
    def find_all_models():
        for library in bpy.context.preferences.filepaths.asset_libraries:
            for root, dir, files in os.walk(library.path):
                basePath = root.replace(library.path, "")
                for fileName in files:
                    if fileName.startswith("Model"):
                        continue

                    if (fileName.endswith(".obj") or fileName.endswith(".fbx") or fileName.endswith(".gltf") or fileName.endswith(".glb")):
                        modelName=os.path.splitext(fileName)[0]
                        AssetLoader.overteDomainModels[modelName] = basePath + "/" + fileName

    @staticmethod
    def getOverteModelUrl(obj):
        entityBaseName = obj.name.partition(".")[0]
        if entityBaseName in AssetLoader.overteDomainModels:
            return AssetLoader.overteDomainModels[entityBaseName]
        return None


class AssetLoaderOperator(bpy.types.Operator):
    """Refreshes the list of available models in the asset path"""
    bl_idname = "world.overte_refresh_library"
    bl_label = "Refresh models library"
    bl_options = {'REGISTER'}

    def execute(self, context):
        AssetLoader.find_all_models()
        return {'FINISHED'}
