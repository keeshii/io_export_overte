import bpy

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntVectorProperty, IntProperty

from ..export_params import ExportParams
from .common_properites import OverteCommonProperties

class OverteObjectProperties(OverteCommonProperties):

    model_file: StringProperty(
        name="File Name",
        description="File name for the model. If empty the object name will be used",
        default='',
    )

    shape_type: EnumProperty(
        name="Collision Shape",
        description="The shape of the collision hull used if collisions are enabled. This affects how an entity collides",
        items=(
            ('none', "No Collision", "No Collision"),
            ('box', "Box", "Box"),
            ('sphere', "Sphere", "Sphere"),
            ('compound', "Compound", "Compound"),
            ('simple-hull', "Basic", "Whole model"),
            ('simple-compound', "Good", "Sub-meshes"),
            ('static-mesh', "Exact", "All polygons"),
        ),
        default='none',
    )

    compound_shape_url: StringProperty(
        name="Compound Shape URL",
        description="The model file to use for the compound shape if Collision Shape is \"Compound\"",
        default='',
    )

    use_original_pivot: BoolProperty(
        name="Use Original Pivot",
        description="If false, the model will be centered based on its content, ignoring any offset in the model itself. If true, the model will respect its original offset",
        default=False,
    )

    animation_url: StringProperty(
        name="Animation URL",
        description="An animation to play on the model",
        default='',
    )

    animation_running: BoolProperty(
        name="Play Automatically",
        description="If enabled, the animation on the model will play automatically",
        default=False,
    )

    animation_loop: BoolProperty(
        name="Loop",
        description="If enabled, then the animation will continuously repeat",
        default=True,
    )

    animation_hold: BoolProperty(
        name="Hold",
        description="If enabled, then rotations and translations of the last frame played are maintained when the animation stops",
        default=False,
    )

    animation_current_frame: IntProperty(
        name="Animation Frame",
        description="The current frame being played in the animation",
        min=0, max=100000,
        default=0
    )

    animation_first_frame: IntProperty(
        name="First Frame",
        description="The first frame to play in the animation",
        min=0, max=100000,
        default=0
    )
    
    animation_last_frame: IntProperty(
        name="Last Frame",
        description="The last frame to play in the animation",
        min=0, max=100000,
        default=100000
    )

    animation_fps: IntProperty(
        name="Animation FPS",
        description="The speed of the animation",
        min=0, max=120,
        default=30
    )
    
    animation_allow_translation: BoolProperty(
        name="Allow Transition",
        description="If enabled, this allows an entity to move in space during an animation",
        default=False,
    )

    textures: StringProperty(
        name="Texture",
        description="A JSON string containing a texture. Use a name from the Original Texture property to override it",
        default='',
    )

    original_texture: StringProperty(
        name="Original Texture",
        description="A JSON string containing the original texture used on the model",
        default='{}',
    )

    group_culled: BoolProperty(
        name="Group Culled",
        description="If false, individual pieces of the entity may be culled by the render engine. If true, either the entire entity will be culled, or it won't at all",
        default=False,
    )


    image_url: StringProperty(
        name="ImageUrl",
        description="The URL for the image source",
        default="",
    )

    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1, 1, 1),
        size=3,
        min=0, max=1,
        description="The color of this entity",
    )

    alpha: FloatProperty(
        name="Alpha",
        description="The opacity of the entity between 0.0 fully transparent and 1.0 completely opaque",
        default=1.0,
        min=0.0,
        max=1.0
    )

    emissive: BoolProperty(
        name="Emissive",
        description="If enabled, the image will display at full brightness",
        default=False,
    )

    image_subimage: IntVectorProperty(
        name="Subimage (x,y,w,h)",
        description="The area of the image that is displayed",
        default=(0, 0, 0, 0),
        size=4,
        min=0, max=100000,
    )

    image_keep_aspect: BoolProperty(
        name="Keep Aspect Ratio",
        description="If enabled, the image will maintain its original aspect ratio",
        default=True,
    )


    web_source_url: StringProperty(
        name="SourceUrl",
        description="The URL for the web page source",
        default="http://localhost/",
    )

    web_source_resolution: IntProperty(
        name="Resolution DPI",
        description="The resolution to display the page at, in pixels per inch. Use this to resize your web source in the frame",
        min=0, max=65535,
        default=30
    )

    web_max_fps: IntProperty(
        name="Max FPS",
        description="The FPS at which to render the web entity. Higher values will have a performance impact",
        min=0, max=255,
        default=15
    )

    web_use_background: BoolProperty(
        name="Use Background",
        description="If disabled, this web entity will support a transparent background for the webpage and its elements if the CSS property of 'background-color' on the 'body' is set with transparency",
        default=True,
    )

    web_input_mode: EnumProperty(
        name="Input Mode",
        description="The user input mode to use",
        items=(
            ('touch', "Touch events", "Touch events"),
            ('mouse', "Mouse events", "Mouse events")
        ),
        default='touch',
    )

    web_focus_highlight: BoolProperty(
        name="Focus Highlight",
        description="If enabled, highlights when it has keyboard focus",
        default=True,
    )

    web_script_url: StringProperty(
        name="Script URL",
        description="The URL of a script to inject into the web page",
        default="",
    )

    web_user_agent: StringProperty(
        name="User Agent",
        description="The user agent that the web entity will use when visiting web pages",
        default=ExportParams.default_user_agent,
    )

    text_value: StringProperty(
        name="Text",
        description="The text to display on the entity",
        default="Text",
    )

    text_color: FloatVectorProperty(
        name="Text Color",
        subtype='COLOR',
        default=(1, 1, 1),
        size=3,
        min=0, max=1,
        description="The color of the text",
    )

    text_alpha: FloatProperty(
        name="Text Alpha",
        description="The opacity of the text between 0.0 fully transparent and 1.0 completely opaque",
        default=1.0,
        min=0.0,
        max=1.0
    )

    text_background_alpha: FloatProperty(
        name="Background Alpha",
        description="The opacity of the background between 0.0 fully transparent and 1.0 completely opaque",
        default=1.0,
        min=0.0,
        max=1.0
    )

    text_line_height: FloatProperty(
        name="Font Size",
        description="The height of each line of text. This determines the size of the text",
        default=0.06,
        min=0.0,
        max=10000.0
    )

    text_font: StringProperty(
        name="Font",
        description="The font to render the text. Supported values: \"Courier\", \"Inconsolata\", \"Roboto\", \"Timeless\", or a URL to a .sdff file",
        default="Roboto",
    )

    text_effect: EnumProperty(
        name="Effect",
        description="The effect that is applied to the text",
        items=(
            ('none', "None", "None"),
            ('outline', "Outline", "Outline"),
            ('outline fill', "Outline with fill", "Outline with fill"),
            ('shadow', "Shadow", "Shadow")
        ),
        default='none',
    )

    text_effect_color: FloatVectorProperty(
        name="Effect Color",
        subtype='COLOR',
        default=(1, 1, 1),
        size=3,
        min=0, max=1,
        description="The color of the text effect",
    )

    text_effect_thickness: FloatProperty(
        name="Effect Thickness",
        description="The magnitude of the text effect",
        default=0.2,
        min=0.0,
        max=0.5
    )

    text_alignment: EnumProperty(
        name="Alignment",
        description="How the text is aligned within its left and right bounds",
        items=(
            ('left', "Left", "Left"),
            ('center', "Center", "Center"),
            ('right', "Right", "Right")
        ),
        default='left',
    )

    text_margin: FloatVectorProperty(
        name="Margin",
        description="The top margin, in meters (top,right,bottom,left)",
        default=(0, 0, 0, 0),
        size=4,
        min=-1000, max=1000,
    )

    text_unlit: BoolProperty(
        name="Unlit",
        description="If enabled, the entity will not be lit by the keylight or local lights",
        default=False,
    )

    light_intensity: FloatProperty(
        name="Intensity",
        description="The brightness of the light",
        default=5.0,
        min=-1000.0,
        max=10000.0
    )
    
    light_fall_off_radius: FloatProperty(
        name="Fall-Off Radius",
        description="The distance from the light's center where the intensity is reduced",
        default=1.0,
        min=-0.0,
        max=10000.0
    )

    light_exponent: FloatProperty(
        name="Spotlight Exponent",
        description="Affects the softness of the spotlight beam; the higher the value, the softer the beam",
        default=1.0,
        min=-0.0,
        max=10000.0
    )
    
    light_cut_off: FloatProperty(
        name="Spotlight Cut-Off",
        description="Affects the size of the spotlight beam; the higher the value, the larger the beam",
        default=75.0,
        min=-0.0,
        max=90.0
    )
