from mathutils import Vector
from math import radians
from ..export_params import ExportParams
import uuid

class BaseEntity(object):

    def __init__(self, obj):
        self.obj = obj
        self.uuid = None

    def get_uuid(self):
        if (self.uuid is None):
            self.uuid = "{" + str(uuid.uuid4()) + "}"
        return self.uuid

    def get_absolute_position(self):
        # find center of the object by calculating an avarage of its bounding-box
        if self.obj.type == 'MESH':
            bbox_center = 0.125 * sum((Vector(b) for b in self.obj.bound_box), Vector())
            return self.obj.matrix_world @ bbox_center

        return self.obj.matrix_world.decompose()[0]

    def get_position(self):
        absolute_position = self.get_absolute_position()
        position = {
            "x": absolute_position[0] * ExportParams.world_scale,
            "y": absolute_position[2] * ExportParams.world_scale,
            "z": -absolute_position[1] * ExportParams.world_scale
        }
        return position

    def get_relative_postion(self, parent):
        parent_location = parent.get_absolute_position()
        child_location = self.get_absolute_position()
        parent_rot = parent.get_absolute_rotation()
        location = parent_rot.to_matrix().inverted().to_4x4() @ (child_location - parent_location)

        position = {
            "x": location[0] * ExportParams.world_scale,
            "y": location[2] * ExportParams.world_scale,
            "z": -location[1] * ExportParams.world_scale
        }
        return position

    def get_dimensions(self):
        d = self.obj.dimensions
        dimensions = {
            "x": d[0] * ExportParams.world_scale,
            "y": d[2] * ExportParams.world_scale,
            "z": d[1] * ExportParams.world_scale
        }
        return dimensions

    def get_rotation_quat(self, r):
        q = r.to_quaternion()
        rotation = { "x": q[1], "y": q[3], "z": -q[2], "w": q[0] }
        return rotation

    def get_absolute_rotation(self):
        return self.obj.matrix_world.to_euler('XYZ')

    def get_relative_rotation(self, parent):
        parent_r = parent.get_absolute_rotation()
        child_r = self.get_absolute_rotation()
        r = (parent_r.to_matrix().inverted().to_4x4() @ child_r.to_matrix().to_4x4()).to_euler('XYZ')
        return self.get_rotation_quat(r)

    def get_rotation(self):
        r = self.get_absolute_rotation()
        return self.get_rotation_quat(r)

    def get_query_aa_cube(self):
        if self.obj.type == 'MESH':
            minx = maxx = miny = maxy = minz = maxz = None
            bbox_corners = [self.obj.matrix_world @ Vector(corner) for corner in self.obj.bound_box]
            for corner in bbox_corners:
                x = corner[0]
                y = corner[1]
                z = corner[2]
                if (minx is None or minx > x):
                    minx = x
                if (maxx is None or maxx < x):
                    maxx = x
                if (miny is None or miny > y):
                    miny = y
                if (maxy is None or maxy < y):
                    maxy = y
                if (minz is None or minz > z):
                    minz = z
                if (maxz is None or maxz < z):
                    maxz = z

            scale = max(maxx - minx, maxy - miny, maxz - minz) * ExportParams.world_scale
            query_aa_cube = {
                "x": (minx + (maxx - minx) / 2) * ExportParams.world_scale - (scale / 2),
                "y": (minz + (maxz - minz) / 2) * ExportParams.world_scale - (scale / 2),
                "z": -(miny + (maxy - miny) / 2) * ExportParams.world_scale - (scale / 2),
                "scale": scale
            }
        else:
            position = self.get_absolute_position()
            scale = max(self.obj.scale) * ExportParams.world_scale * 1.5
            query_aa_cube = {
                "x": position[0] * ExportParams.world_scale - (scale / 2),
                "y": position[2] * ExportParams.world_scale - (scale / 2),
                "z": -position[1] * ExportParams.world_scale + (scale / 2),
                "scale": scale
            }
        return query_aa_cube

    def get_scripts(self):
        scripts = { }
        if self.obj.overte.script_url:
            scripts["script"] = ExportParams.get_url(self.obj.overte.script_url)
        if self.obj.overte.server_script_url:
            scripts["serverScripts"] = ExportParams.get_url(self.obj.overte.server_script_url)
        if self.obj.overte.user_data:
            scripts["userData"] = self.obj.overte.user_data
        return scripts

    def get_collisions(self):
        collisions = { }
        if self.obj.overte.collides_enabled == False:
            collisions["collisionless"] = True
            collisions["ignoreForCollisions"] = True
        else:
            collision_mask = 0
            collides_with = ""

            if self.obj.overte.collides_static:
                collision_mask = collision_mask + 1
                collides_with = collides_with + "static,"
            if self.obj.overte.collides_kinematic:
                collision_mask = collision_mask + 4
                collides_with = collides_with + "kinematic,"
            if self.obj.overte.collides_dynamic:
                collision_mask = collision_mask + 2
                collides_with = collides_with + "dynamic,"
            if self.obj.overte.collides_my_avatar:
                collision_mask = collision_mask + 8
                collides_with = collides_with + "myAvatar,"
            if self.obj.overte.collides_other_avatars:
                collision_mask = collision_mask + 16
                collides_with = collides_with + "otherAvatar,"

            if collision_mask < 31:
                collisions["collisionMask"] = collision_mask
                collisions["collidesWith"] = collides_with

            if self.obj.overte.collides_sound:
                collisions["collisionSoundURL"] = ExportParams.get_url(self.obj.overte.collides_sound)

        if self.obj.overte.server_script_url:
            collisions["serverScripts"] = ExportParams.get_url(self.obj.overte.server_script_url)

        if self.obj.overte.is_dynamic == True:
            collisions["dynamic"] = True
            collisions["collisionsWillMove"] = True
        return collisions

    def get_entity_values(self):
        entity = { }
        if self.obj.overte.description:
            entity["description"] = self.obj.overte.description

        if self.obj.overte.parent_joint_index != 65535:
            entity["parentJointIndex"] = self.obj.overte.parent_joint_index

        if self.obj.overte.render_layer != 'world':
            entity["renderLayer"] = self.obj.overte.render_layer

        if self.obj.overte.primitive_mode != 'solid':
            entity["primitiveMode"] = self.obj.overte.primitive_mode

        if self.obj.overte.bilboard_mode != 'none':
            entity["billboardMode"] = self.obj.overte.bilboard_mode

        entity["isFacingAvatar"] = self.obj.overte.bilboard_mode == 'full'
        entity["faceCamera"] = self.obj.overte.bilboard_mode == 'yaw'

        if self.obj.overte.visible == False:
            entity["visible"] = False
        if self.obj.overte.locked == True:
            entity["locked"] = True
        return entity

    def get_behavior(self):
        behavior = { }
        if self.obj.overte.cloneable == True:
            behavior["cloneable"] = True
            behavior["cloneLifetime"] = self.obj.overte.clone_lifetime
            if self.obj.overte.clone_limit != 0:
                behavior["cloneLimit"] = self.obj.overte.cloneLimit
            if self.obj.overte.clone_dynamic == True:
                behavior["cloneDynamic"] = True
            if self.obj.overte.clone_avatar_entity == True:
                behavior["cloneAvatarEntity"] = True

        grab = { }
        if self.obj.overte.grabbable == True:
            if self.obj.overte.grabbable_follow_controllers == False:
                grab["grabFollowsController"] = False
            if self.obj.overte.triggerable == True:
                grab["triggerable"] = True
            if self.obj.overte.grabbable_follow_controllers == False or self.obj.overte.triggerable == True:
                behavior["grab"] = grab
        else:
            behavior["grab"] = {
                "grabbable": False,
                "equippableLeftRotation": { "x": 0, "y": 0, "z": 0, "w": 1 },
                "equippableRightRotation": { "x": 0, "y": 0, "z": 0, "w": 1 }
            }

        if self.obj.overte.cast_shadows == False:
            behavior["canCastShadow"] = False

        if self.obj.overte.href != '':
            behavior["href"] = ExportParams.get_url(self.obj.overte.href)

        if self.obj.overte.ignore_pick_intersection == True:
            behavior["ignorePickIntersection"] = True

        if self.obj.overte.lifetime != -1:
            behavior["lifetime"] = self.obj.overte.lifetime

        return behavior

    def get_physics(self):
        physics = { }
        v = self.obj.overte.linear_velocity
        if v[0] != 0.0 or v[1] != 0.0 or v[2] != 0.0:
            physics["velocity"] = {
                "x": v[0],
                "y": v[2],
                "z": -v[1]
            }

        v = self.obj.overte.angular_velocity
        if v[0] != 0.0 or v[1] != 0.0 or v[2] != 0.0:
            physics["angularVelocity"] = {
                "x": radians(v[0]),
                "y": radians(v[2]),
                "z": -radians(v[1])
            }

        physics["damping"] = self.obj.overte.linear_damping
        physics["angularDamping"] = self.obj.overte.angular_damping

        if self.obj.overte.restitution != 0.5:
            physics["restitution"] = self.obj.overte.restitution

        if self.obj.overte.friction != 0.5:
            physics["friction"] = self.obj.overte.friction

        if self.obj.overte.density != 1000:
            physics["density"] = self.obj.overte.density

        v = self.obj.overte.gravity
        if v[0] != 0.0 or v[1] != 0.0 or v[2] != 0.0:
            physics["gravity"] = {
                "x": v[0],
                "y": v[1],
                "z": v[2]
            }

        return physics

    def get_color(self, value):
        color = {
            "color": {
                "red": int(value[0] * 255),
                "green": int(value[1] * 255),
                "blue": int(value[2] * 255)
            }
        }
        return color

    def get_material_entities(self):
        return []

    def get_material_color(self):
        try:
            obj = self.obj
            material = obj.material_slots[0].material
            nodes = material.node_tree.nodes
            principled = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
            base_color = principled.inputs['Base Color'] #Or principled.inputs[0]
            value = base_color.default_value

            # Translate as color
            color = self.get_color(value)
            # Get the link
            # link = base_color.links[0]
            # link_node = link.from_node
            # print( link_node.image.name )
            return color
        except:
            return None

    def export(self, entityType):
        entity_values = self.get_entity_values()
        scripts = self.get_scripts()
        collisions = self.get_collisions()
        behavior = self.get_behavior()
        physics = self.get_physics()

        entity = {
            "id": self.get_uuid(),
            "type": entityType,
            "name": self.obj.name,
            "lastEdited": ExportParams.current_time,
            "created": ExportParams.current_time,
            "clientOnly": False,
            "avatarEntity": False,
            "localEntity": False,
        }
        return { **entity, **scripts, **entity_values, **collisions, **behavior, **physics }

    def draw_physics_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "linear_velocity")
        row = box.row()
        row.prop(self.obj.overte, "linear_damping")
        row = box.row()
        row.prop(self.obj.overte, "angular_velocity")
        row = box.row()
        row.prop(self.obj.overte, "angular_damping")
        row = box.row()
        row.prop(self.obj.overte, "restitution")
        row = box.row()
        row.prop(self.obj.overte, "friction")
        row = box.row()
        row.prop(self.obj.overte, "density")
        row = box.row()
        row.prop(self.obj.overte, "gravity")

    def draw_behavior_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "grabbable")
        box2 = box.box()
        row = box2.row()
        row.prop(self.obj.overte, "cloneable")
        if self.obj.overte.cloneable == True:
            row = box2.row()
            row.prop(self.obj.overte, "clone_lifetime")
            row = box2.row()
            row.prop(self.obj.overte, "clone_limit")
            row = box2.row()
            row.prop(self.obj.overte, "clone_dynamic")
            row = box2.row()
            row.prop(self.obj.overte, "clone_avatar_entity")
        row = box.row()
        row.prop(self.obj.overte, "triggerable")
        row = box.row()
        row.prop(self.obj.overte, "grabbable_follow_controllers")
        row = box.row()
        row.prop(self.obj.overte, "cast_shadows")
        row = box.row()
        row.prop(self.obj.overte, "href")
        row = box.row()
        row.prop(self.obj.overte, "ignore_pick_intersection")
        row = box.row()
        row.prop(self.obj.overte, "lifetime")

    def draw_collision_panel(self, layout):
        box = layout.box()
        box2 = box.box()
        row = box2.row()
        row.prop(self.obj.overte, "collides_enabled")
        enabled = self.obj.overte.collides_enabled == True
        row = box2.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "collides_static")
        row = box2.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "collides_kinematic")
        row = box2.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "collides_dynamic")
        row = box2.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "collides_my_avatar")
        row = box2.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "collides_other_avatars")
        row = box2.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "collides_sound")
        row = box.row()
        row.prop(self.obj.overte, "is_dynamic")

    def draw_entity_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "description")
        row = box.row()
        row.prop(self.obj.overte, "parent_joint_index")
        row = box.row()
        row.prop(self.obj.overte, "render_layer")
        row = box.row()
        row.prop(self.obj.overte, "primitive_mode")
        row = box.row()
        row.prop(self.obj.overte, "bilboard_mode")
        row = box.row()
        row.prop(self.obj.overte, "visible")
        row = box.row()
        row.prop(self.obj.overte, "locked")


    def draw_script_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "script_url")
        row = box.row()
        row.prop(self.obj.overte, "server_script_url")
        row = box.row()
        row.prop(self.obj.overte, "user_data")

    def draw_panel(self, layout):
        return

    def generate(self, output_dir):
        return
