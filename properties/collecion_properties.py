import bpy

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntVectorProperty, IntProperty

from .common_properites import OverteCommonProperties

class OverteCollectionProperties(OverteCommonProperties):
    zone_shape_type: EnumProperty(
        name="Shape Type",
        description="The shape of the volume in which the zone's lighting effects and avatar permissions have effect",
        items=(
            ('box', "Box", "Box"),
            ('sphere', "Sphere", "Sphere"),
            ('cylinder-y', "Cylinder", "Cylinder"),
            ('compound', "Compound", "Use Compound Shape URL"),
        ),
        default='box',
    )

    zone_compound_url: StringProperty(
        name="Compound Shape URL",
        description="The model file to use for the compound shape if Shape Type is \"Use Compound Shape URL\"",
        default="",
    )

    flying_allowed: BoolProperty(
        name="Flying Allowed",
        description="If enabled, users can fly in the zone",
        default=True
    )

    ghosting_allowed: BoolProperty(
        name="Ghosting Allowed",
        description="If enabled, users with avatar collisions turned off will not collide with content in the zone",
        default=True
    )

    filter_url: StringProperty(
        name="Filter URL",
        description="The URL of a JS file that checks for changes to entity properties within the zone. Runs periodically",
        default="",
    )

    skybox_mode: EnumProperty(
        name="Skybox Mode",
        description="Configures the skybox in the zone. The skybox is a cube map image",
        items=(
            ('enabled', "On", "Enabled"),
            ('disabled', "Off", "Disabled"),
            ('inherit', "Inherit", "Inherit"),
        ),
        default='inherit',
    )

    skybox_color: FloatVectorProperty(
        name="Skybox Color",
        subtype='COLOR',
        default=(1, 1, 1),
        size=3,
        min=0, max=1,
        description="If the URL is blank, this changes the color of the sky, otherwise it modifies the color of the skybox",
    )

    skybox_url: StringProperty(
        name="SkyboxUrl",
        description="A cube map image that is used to render the sky",
        default="",
    )

    zone_margin: FloatProperty(
        name="Zone Margin",
        description="Additional space around the zone entity",
        default=0.0,
        min=0.0,
        max=100.0
    )

    ambient_mode: EnumProperty(
        name="Ambient Mode",
        description="Configures the ambient light in the zone. Use this if you want your skybox to reflect light on the content",
        items=(
            ('enabled', "On", "Enabled"),
            ('disabled', "Off", "Disabled"),
            ('inherit', "Inherit", "Inherit"),
        ),
        default='inherit',
    )

    ambient_intensity: FloatProperty(
        name="Ambient Intensity",
        description="The intensity of the ambient light",
        default=0.5,
        min=-200.0,
        max=200.0
    )

    ambient_url: StringProperty(
        name="Ambient Url",
        description="A cube map image that defines the color of the light coming from each direction",
        default="",
    )

    keylight_mode: EnumProperty(
        name="Keylight Mode",
        description="Configures the key light in the zone. This light is directional",
        items=(
            ('enabled', "On", "Enabled"),
            ('disabled', "Off", "Disabled"),
            ('inherit', "Inherit", "Inherit"),
        ),
        default='inherit',
    )

    keylight_color: FloatVectorProperty(
        name="Keylight Color",
        subtype='COLOR',
        default=(1, 1, 1),
        size=3,
        min=0, max=1,
        description="The color of the key light",
    )

    keylight_intensity: FloatProperty(
        name="Keylight Intensity",
        description="The intensity of the key light",
        default=1.0,
        min=-40,
        max=40
    )

    keylight_vertical: FloatProperty(
        name="Vertical Angle",
        description="The angle in deg at which light emits. Starts in the entity's -z direction, and rotates around its y axis",
        default=45.0,
        min=-180.0,
        max=180.0
    )

    keylight_horizontal: FloatProperty(
        name="Horizontal Angle",
        description="The angle in deg at which light emits. Starts in the entity's -z direction, and rotates around its x axis",
        default=0.0,
        min=-180.0,
        max=180.0
    )

    keylight_cast_shadows: BoolProperty(
        name="Cast Shadows",
        description="If enabled, shadows are cast. The entity or avatar casting the shadow must also have Cast Shadows enabled. Note: Shadows are rendered only on high-profiled computers. This setting will have no effect on computers profiled to medium or low graphics",
        default=False
    )

    keylight_shadow_bias: FloatProperty(
        name="Shadow Bias",
        description="The bias of the shadows cast by the light.  Use this to fine-tune your shadows to your scene to prevent shadow acne and peter panning",
        default=0.5,
        min=-0.0,
        max=1.0
    )

    keylight_shadow_distance: FloatProperty(
        name="Max Shadow Distance",
        description="The max distance from your view at which shadows will be computed",
        default=40.0,
        min=-0.0,
        max=250.0
    )

    haze_mode: EnumProperty(
        name="Haze Mode",
        description="Configures the haze in the scene",
        items=(
            ('enabled', "On", "Enabled"),
            ('disabled', "Off", "Disabled"),
            ('inherit', "Inherit", "Inherit"),
        ),
        default='inherit',
    )

    haze_range: IntProperty(
        name="Range",
        description="How far the haze extends out. This is measured in meters",
        min=1, max=100000,
        default=1000
    )

    haze_use_altitude: BoolProperty(
        name="Use Altitude",
        description="If enabled, this adjusts the haze intensity as it gets higher",
        default=False
    )

    haze_base: IntProperty(
        name="Base",
        description="The base of the altitude range. Measured in entity space",
        min=-16000, max=16000,
        default=0
    )

    haze_ceiling: IntProperty(
        name="Ceiling",
        description="The ceiling of the altitude range. Measured in entity space",
        min=-16000, max=16000,
        default=200
    )

    haze_color: FloatVectorProperty(
        name="Haze Color",
        subtype='COLOR',
        default=(0.5, 0.604, 0.702),
        size=3,
        min=0, max=1,
        description="The color of the haze",
    )

    haze_background_blend: FloatProperty(
        name="Background Blend",
        description="How much the skybox shows through the haze. The higher the value, the more it shows through",
        default=0.0,
        min=0.0,
        max=1.0
    )

    haze_enable_glare: BoolProperty(
        name="Enable Glare",
        description="If enabled, a glare is enabled on the skybox, based on the key light",
        default=False
    )
    
    haze_glare_color: FloatVectorProperty(
        name="Glare Color",
        subtype='COLOR',
        default=(1.0, 0.899, 0.702),
        size=3,
        min=0, max=1,
        description="The color of the glare based on the key light",
    )

    haze_glare_angle: IntProperty(
        name="Glare Angle",
        description="The angular size of the glare and how much it encompasses the skybox, based on the key light",
        min=0, max=180,
        default=20
    )

    bloom_mode: EnumProperty(
        name="Bloom Mode",
        description="Configures how much bright areas of the scene glow",
        items=(
            ('enabled', "On", "Enabled"),
            ('disabled', "Off", "Disabled"),
            ('inherit', "Inherit", "Inherit"),
        ),
        default='inherit',
    )

    bloom_intensity: FloatProperty(
        name="Bloom Intensity",
        description="The intensity, or brightness, of the bloom effect",
        default=0.25,
        min=0.0,
        max=1.0
    )

    bloom_threshold: FloatProperty(
        name="Bloom Threshold",
        description="The cutoff of the bloom. The higher the value, the more only bright areas of the scene will glow",
        default=0.7,
        min=0.0,
        max=1.0
    )

    avatar_priority: EnumProperty(
        name="Avatar Priority",
        description="Alter Avatars' update priorities",
        items=(
            ('crowd', "Crowd", "Crowd"),
            ('hero', "Hero", "Hero"),
            ('inherit', "Inherit", "Inherit"),
        ),
        default='inherit',
    )

    screen_share: EnumProperty(
        name="Screen-share",
        description="Enable screen-sharing within this zone",
        items=(
            ('enabled', "On", "Enabled"),
            ('disabled', "Off", "Disabled"),
            ('inherit', "Inherit", "Inherit"),
        ),
        default='inherit',
    )
