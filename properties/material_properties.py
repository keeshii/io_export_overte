import bpy

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntVectorProperty, IntProperty

from .common_properites import OverteCommonProperties

class OverteMaterialProperties(OverteCommonProperties):
    material_url: StringProperty(
        name="Material URL",
        description="The URL to an external JSON file or \"materialData\". Append \"?<material name>\" to select a single material if multiple are defined",
        default="",
    )

    material_data: StringProperty(
        name="Material Data JSON",
        description="Can be used instead of a JSON file when material set to materialData",
        default="",
    )

    material_priority: IntProperty(
        name="Priority",
        description="The priority of the material, where a larger number means higher priority. Original materials = 0",
        min=0, max=65535,
        default=1
    )

    material_mapping_mode: EnumProperty(
        name="Material Mapping Mode",
        description="How the material is mapped to the entity. If set to \"UV space\", then the material will be applied with the target entity's UV coordinates. If set to \"3D Projected\", then the 3D transform of the material entity will be used",
        items=(
            ('default', "UV space", "UV space"),
            ('projected', "3D projected", "3D projected"),
        ),
        default='default',
    )

    material_position: FloatVectorProperty(
        name="Material Position",
        description="The offset position of the bottom left of the material within the parent's UV space",
        default=(0.0, 0.0),
        size=2,
        min=0, max=1
    )

    material_scale: FloatVectorProperty(
        name="Material Scale",
        description="How many times the material will repeat in each direction within the parent's UV space",
        default=(1.0, 1.0),
        size=2,
        min=0, max=100000
    )

    material_rotation: FloatProperty(
        name="Material Rotation",
        description="How much to rotate the material within the parent's UV-space, in degrees",
        default=0.0,
        min=-100000, max=100000
    )

    material_repeat: BoolProperty(
        name="Material Repeat",
        description="If enabled, the material will repeat, otherwise it will clamp",
        default=True
    )
