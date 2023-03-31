import bpy

from .entities import MaterialEntity, ZoneEntity
from .entity_factory import EntityFactory

class OverteObjectPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Overte Object"
    bl_idname = "OBJECT_PT_overte_object"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return EntityFactory.createEntity(obj)

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        entity = EntityFactory.createEntity(obj)
        if entity:
            entity.draw_panel(layout)


class OverteCollectionPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Overte Zone"
    bl_idname = "OBJECT_PT_overte_collection"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    @classmethod
    def poll(cls, context):
        col = context.collection
        return EntityFactory.matchName(col, "Zone")

    def draw(self, context):
        layout = self.layout
        col = context.collection

        if EntityFactory.matchName(col, "Zone"):
            entity = ZoneEntity(col)
            entity.draw_panel(layout)
        else:
            row = layout.row()
            row.label(text="Collection name is not a \"Zone\"")


class OverteMaterialPanel(bpy.types.Panel):
    """Creates a Panel in the Material properties window"""
    bl_label = "Overte Material"
    bl_idname = "OBJECT_PT_overte_material"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.active_material

    def draw(self, context):
        layout = self.layout
        
        obj = context.active_object
        if context.active_object and context.active_object.active_material:
            mat = context.active_object.active_material
            entity = MaterialEntity(mat)
            entity.draw_panel(layout)
        else:
            row = layout.row()
            row.label(text="No material")


class OverteWorldPanel(bpy.types.Panel):
    """Creates a Panel in the World properties window"""
    bl_label = "Overte Settings"
    bl_idname = "OBJECT_PT_overte_world"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"

    def draw(self, context):
        obj = context.scene.world

        layout = self.layout
        row = layout.row()
        row.prop(obj.overte, "domain_url")
        row = layout.row()
        row.prop(obj.overte, "models_path")
        row = layout.row()
        row.prop(obj.overte, "world_scale")
        row = layout.row()
        row.operator("world.overte_refresh_library")
