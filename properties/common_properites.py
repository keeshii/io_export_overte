import bpy

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntVectorProperty, IntProperty

class OverteCommonProperties(bpy.types.PropertyGroup):
    description: StringProperty(
        name="Description",
        description="Use this field to describe the entity",
        default="",
    )

    visible: BoolProperty(
        name="Visible",
        description="If enabled, this entity will be visible",
        default=True
    )

    locked: BoolProperty(
        name="Locked",
        description="If enabled, this entity will be locked",
        default=False
    )

    parent_joint_index: IntProperty(
        name="Parent Joint Index",
        description="If the entity is parented to an avatar, this joint defines where on the avatar the entity is parented",
        min=0, max=65535,
        default=65535
    )

    render_layer: EnumProperty(
        name="Render Layer",
        description="The layer on which this entity is rendered",
        items=(
            ('world', "World", "World"),
            ('front', "Front", "Front"),
            ('hud', "HUD", "HUD"),
        ),
        default='world',
    )

    primitive_mode: EnumProperty(
        name="Primitive Mode",
        description="The mode in which to draw an entity, either \"Solid\" or \"Wireframe\"",
        items=(
            ('solid', "Solid", "Solid"),
            ('lines', "Wireframe", "Wireframe"),
        ),
        default='solid',
    )

    bilboard_mode: EnumProperty(
        name="Bilboard Mode",
        description="Determines if and how the entity will face the camera",
        items=(
            ('none', "None", "None"),
            ('yaw', "Yaw", "Yaw"),
            ('full', "Full", "Full"),
        ),
        default='none',
    )

    script_url: StringProperty(
        name="Script",
        description="The URL to an external JS file to add behaviors to the client",
        default="",
    )

    server_script_url: StringProperty(
        name="Server Script",
        description="The URL to an external JS file to add behaviors to the server",
        default="",
    )

    user_data: StringProperty(
        name="User Data JSON",
        description="Used to store extra data about the entity in JSON format",
        default="",
    )
    
    collides_enabled: BoolProperty(
        name="Collides",
        description="If enabled, this entity will collide with other entities or avatars",
        default=True
    )
    
    collides_static: BoolProperty(
        name="Static Entities",
        description="If enabled, this entity will collide with other non-moving, static entities",
        default=True
    )
    
    collides_kinematic: BoolProperty(
        name="Kinematic Entities",
        description="If enabled, this entity will collide with other kinematic entities (they have velocity but are not dynamic)",
        default=True
    )

    collides_dynamic: BoolProperty(
        name="Dynamic Entities",
        description="If enabled, this entity will collide with other dynamic entities",
        default=True
    )

    collides_my_avatar: BoolProperty(
        name="My Avatar",
        description="If enabled, this entity will collide with your own avatar",
        default=True
    )

    collides_other_avatars: BoolProperty(
        name="Other Avatars",
        description="If enabled, this entity will collide with other user's avatars",
        default=True
    )

    collides_sound: StringProperty(
        name="Collision Sound",
        description="The URL of a sound to play when the entity collides with something else",
        default=''
    )

    is_dynamic: BoolProperty(
        name="Is Dynamic",
        description="If enabled, this entity has collisions associated with it that can affect its movement",
        default=False
    )

    grabbable: BoolProperty(
        name="Grabbable",
        description="If enabled, this entity will allow grabbing input and will be movable",
        default=False
    )

    cloneable: BoolProperty(
        name="Cloneable",
        description="If enabled, this entity can be duplicated",
        default=False
    )


    clone_lifetime: IntProperty(
        name="Clone Lifetime",
        description="The lifetime for clones of this entity",
        min=-1, max=100000,
        default=300
    )
    
    clone_limit: IntProperty(
        name="Clone Limit",
        description="The total number of clones of this entity that can exist in the domain at any given time",
        min=0, max=100000,
        default=0
    )
    
    clone_dynamic: BoolProperty(
        name="Clone Dynamic",
        description="If enabled, then clones created from this entity will be dynamic, allowing the clone to collide",
        default=False
    )
    
    clone_avatar_entity: BoolProperty(
        name="Clone Avatar Entity",
        description="Clone Avatar Entity",
        default=False
    )

    triggerable: BoolProperty(
        name="Triggerable",
        description="If enabled, the collider on this entity is used for triggering events",
        default=False
    )

    grabbable_follow_controllers: BoolProperty(
        name="Follow Controllers",
        description="If enabled, grabbed entities will follow the movements of your hand controller instead of your avatar's hand",
        default=True
    )

    cast_shadows: BoolProperty(
        name="Cast Shadows",
        description="If enabled, the geometry of this entity casts shadows when a shadow-casting light source shines on it. Note: Shadows are rendered only on high-profiled computers. This setting will have no effect on computers profiled to medium or low graphics",
        default=True
    )

    href: StringProperty(
        name="Link",
        description="The URL that will be opened when a user clicks on this entity. Useful for web pages and portals",
        default=''
    )

    ignore_pick_intersection: BoolProperty(
        name="Ignore Pick Intersection",
        description="If enabled, this entity will not be considered for ray picks, and will also not occlude other entities when picking",
        default=False
    )

    lifetime: IntProperty(
        name="Lifetime",
        description="The time this entity will exist in the environment for",
        min=-1, max=100000,
        default=-1
    )

    linear_velocity: FloatVectorProperty(
        name="Linear Velocity",
        description="The linear velocity vector of the entity. The velocity at which this entity moves forward in space",
        default=(0, 0, 0),
        size=3,
        min=-270.0, max=270.0
    )

    linear_damping: FloatProperty(
        name="Linear Damping",
        description="The linear damping to slow down the linear velocity of an entity over time. A higher damping value slows down the entity more quickly. The default value is for an exponential decay timescale of 2.0s, where it takes 2.0s for the movement to slow to 1/e = 0.368 of its initial value",
        default=0,
        min=0.0,
        max=1.0
    )

    angular_velocity: FloatVectorProperty(
        name="Angular Velocity",
        description="The angular velocity of the entity in 'deg/s' with respect to its axes, about its pivot point",
        default=(0, 0, 0),
        size=3,
        min=-3240.0, max=3240.0
    )

    angular_damping: FloatProperty(
        name="Angular Damping",
        description="The angular damping to slow down the angular velocity of an entity over time. A higher damping value slows down the entity more quickly. The default value is for an exponential decay timescale of 2.0s, where it takes 2.0s for the movement to slow to 1/e = 0.368 of its initial value",
        default=0,
        min=0.0,
        max=1.0
    )

    restitution: FloatProperty(
        name="Bounciness",
        description="If enabled, the entity can bounce against other objects that also have Bounciness",
        default=0.5,
        min=0.0,
        max=0.99
    )

    friction: FloatProperty(
        name="Friction",
        description="The friction applied to slow down an entity when it's moving against another entity",
        default=0.5,
        min=0.0,
        max=10.0
    )

    density: FloatProperty(
        name="Density",
        description="The density of the entity. The higher the density, the harder the entity is to move",
        default=1000.0,
        min=100.0,
        max=10000.0
    )

    gravity: FloatVectorProperty(
        name="Gravity",
        description="The acceleration due to gravity that the entity should move with, in world space",
        default=(0, 0, 0),
        size=3,
        min=-98.0, max=98.0
    )

