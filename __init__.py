bl_info = {
    "name": "Export Overte json files",
    "author": "keeshii",
    "version": (0, 0, 1),
    "blender": (3, 2, 0),
    "location": "File > Import-Export",
    "description": "Exports scene to Overte json world file.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

import bpy
from .asset_loader import AssetLoader, AssetLoaderOperator
from .export_overte_json import ExportOverteJson
from .properties import OverteObjectProperties, OverteCollectionProperties, OverteMaterialProperties, OverteWorldProperties
from .overte_panels import OverteObjectPanel, OverteCollectionPanel, OverteMaterialPanel, OverteWorldPanel

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportOverteJson.bl_idname, text="Overte (*.json)")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    AssetLoader.find_all_models()
    bpy.utils.register_class(ExportOverteJson)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.utils.register_class(AssetLoaderOperator)

    bpy.utils.register_class(OverteObjectProperties)
    bpy.utils.register_class(OverteObjectPanel)
    bpy.utils.register_class(OverteCollectionProperties)
    bpy.utils.register_class(OverteCollectionPanel)
    bpy.utils.register_class(OverteMaterialProperties)
    bpy.utils.register_class(OverteMaterialPanel)
    bpy.utils.register_class(OverteWorldProperties)
    bpy.utils.register_class(OverteWorldPanel)

    bpy.types.Object.overte = bpy.props.PointerProperty(type=OverteObjectProperties)
    bpy.types.Collection.overte = bpy.props.PointerProperty(type=OverteCollectionProperties)
    bpy.types.Material.overte = bpy.props.PointerProperty(type=OverteMaterialProperties)
    bpy.types.World.overte = bpy.props.PointerProperty(type=OverteWorldProperties)

def unregister():
    bpy.utils.unregister_class(ExportOverteJson)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(AssetLoaderOperator)

    bpy.utils.unregister_class(OverteObjectProperties)
    bpy.utils.unregister_class(OverteObjectPanel)
    bpy.utils.unregister_class(OverteCollectionProperties)
    bpy.utils.unregister_class(OverteCollectionPanel)
    bpy.utils.unregister_class(OverteMaterialProperties)
    bpy.utils.unregister_class(OverteMaterialPanel)
    bpy.utils.unregister_class(OverteWorldProperties)
    bpy.utils.unregister_class(OverteWorldPanel)

if __name__ == "__main__":
    register()

