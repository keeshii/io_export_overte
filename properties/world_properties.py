import bpy

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntVectorProperty, IntProperty

from .common_properites import OverteCommonProperties

class OverteWorldProperties(bpy.types.PropertyGroup):
    domain_url: StringProperty(
        name="Domain URL",
        description="Adress added to all local assets",
        default="http://localhost/",
    )

    models_path: StringProperty(
        name="Models Path",
        description="Place where models will be generated",
        default="generated/",
    )

    textures_path: StringProperty(
        name="Textures Path",
        description="Place where material images will be stored",
        default="textures/",
    )

    world_scale: FloatProperty(
        name="World scale",
        description="Changes the size of the world during the export process",
        min=0.0, max=1000.0,
        soft_min=0.0, soft_max=1000.0,
        default=1,
    )
