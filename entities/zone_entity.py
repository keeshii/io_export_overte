from mathutils import Matrix, Vector
from math import radians
from ..export_params import ExportParams
from .base_entity import BaseEntity

class ZoneEntity(BaseEntity):

    def __init__(self, obj):
        super().__init__(obj)

    def get_all_zone_objects(self, col, objs):
        objs = objs + list(col.objects)
        for child in col.children:
            objs = self.get_all_zone_objects(child, objs)
        return objs

    def get_zone_position_dimension(self, col):
        objs = self.get_all_zone_objects(col, [])
        zone_margin = col.overte.zone_margin
        if len(objs) == 0:
            return {
                "position": { "x": 0, "y": 0, "z": 0 },
                "dimensions": { "x": 0, "y": 0, "z": 0 },
                "queryAACube": { "x": 0, "y": 0, "z": 0, "scale": 1 }
            }
        minx = maxx = miny = maxy = minz = maxz = None
        for obj in objs:
            bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
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
        return {
            "position": {
                "x": (minx + (maxx - minx) / 2) * ExportParams.world_scale,
                "y": (minz + (maxz - minz) / 2) * ExportParams.world_scale,
                "z": -(miny + (maxy - miny) / 2) * ExportParams.world_scale
            },
            "dimensions": {
                "x": (maxx - minx + zone_margin * 2) * ExportParams.world_scale,
                "y": (maxz - minz + zone_margin * 2) * ExportParams.world_scale,
                "z": (maxy - miny + zone_margin * 2) * ExportParams.world_scale
            },
            "queryAACube": {
                "x": (minx + (maxx - minx) / 2) * ExportParams.world_scale - (scale / 2),
                "y": (minz + (maxz - minz) / 2) * ExportParams.world_scale - (scale / 2),
                "z": -(miny + (maxy - miny) / 2) * ExportParams.world_scale - (scale / 2),
                "scale": scale
            }
        }

    def get_skybox_option(self):
        skybox_option = { }
        if self.obj.overte.skybox_mode == 'enabled':
            skybox_color = { }
            if sum(self.obj.overte.skybox_color) != 0 and sum(self.obj.overte.skybox_color) != 3:
                skybox_color = self.get_color(self.obj.overte.skybox_color)
            skybox_option = {
                "skybox": {
                    "url": ExportParams.get_url(self.obj.overte.skybox_url),
                    **skybox_color
                },
                "skyboxMode": "enabled"
            }
        elif self.obj.overte.skybox_mode == 'disabled':
            skybox_option = {
                "skyboxMode": 'disabled',
            }
        return skybox_option

    def get_ambient_option(self):
        ambient_option = { }
        if self.obj.overte.ambient_mode == 'enabled':
            ambient_option = {
                "ambientLightMode": 'enabled',
                "ambientLight": {
                    "ambientIntensity": self.obj.overte.ambient_intensity,
                    "ambientURL": ExportParams.get_url(self.obj.overte.ambient_url)
                }
            }
        elif self.obj.overte.ambient_mode == 'disabled':
            ambient_option = {
                "ambientLightMode": 'disabled',
            }
        return ambient_option

    def get_keylight_option(self):
        keylight_option = { }
        if self.obj.overte.keylight_mode == 'enabled':
            point = Vector((0, 0, -1))
            v = self.obj.overte.keylight_vertical
            h = self.obj.overte.keylight_horizontal
            mat_rot_v = Matrix.Rotation(radians(90.0 - v), 4, 'X')
            mat_rot_h = Matrix.Rotation(radians(-h), 4, 'Z')
            direction = point @ mat_rot_v @ mat_rot_h

            keylight_color = { }
            if sum(self.obj.overte.keylight_color) != 3:
                keylight_color = self.get_color(self.obj.overte.keylight_color)

            keylight_option = {
                "keyLightMode": 'enabled',
                "keyLight": {
                    "direction": {
                        "x": direction[0],
                        "y": direction[2],
                        "z": -direction[1]
                    }
                },
                "intensity": self.obj.overte.keylight_intensity,
                "castShadows": self.obj.overte.keylight_cast_shadows,
                "shadowBias": self.obj.overte.keylight_shadow_bias,
                "shadowMaxDistance": self.obj.overte.keylight_shadow_distance,
                **keylight_color
            }
        elif self.obj.overte.keylight_mode == 'disabled':
            keylight_option = {
                "keyLightMode": 'disabled',
            }
        return keylight_option

    def get_zone_option(self):
        zone_option = {}
        zone_option["shapeType"] = self.obj.overte.zone_shape_type

        if self.obj.overte.zone_shape_type == 'compound':
            zone_option["compoundShapeURL"] = ExportParams.get_url(self.obj.overte.zone_compound_url)

        if self.obj.overte.flying_allowed != True:
            zone_option["flyingAllowed"] = self.obj.overte.flying_allowed

        if self.obj.overte.ghosting_allowed != True:
            zone_option["ghostingAllowed"] = self.obj.overte.ghosting_allowed

        if self.obj.overte.filter_url != '':
            zone_option["filterURL"] = self.obj.overte.filter_url
        return zone_option

    def get_haze_option(self):
        haze_option = {}

        if self.obj.overte.haze_mode == 'enabled':
            haze_option["hazeMode"] = "enabled"
            haze = {}
            custom_haze = False

            if self.obj.overte.haze_range != 1000:
                haze["hazeRange"] = self.obj.overte.haze_range
                custom_haze = True

            if self.obj.overte.haze_use_altitude != False:
                haze["hazeAltitudeEffect"] = self.obj.overte.haze_use_altitude
                custom_haze = True

            if self.obj.overte.haze_base != 0:
                haze["hazeBaseRef"] = self.obj.overte.haze_base
                custom_haze = True

            if self.obj.overte.haze_ceiling != 200:
                haze["hazeCeiling"] = self.obj.overte.haze_ceiling
                custom_haze = True

            c = self.get_color(self.obj.overte.haze_color)["color"]
            if c["red"] != 127 or c["green"] != 154 or c["blue"] != 179:
                haze["hazeColor"] = c
                custom_haze = True

            if self.obj.overte.haze_background_blend != 0.0:
                haze["hazeBackgroundBlend"] = self.obj.overte.haze_background_blend
                custom_haze = True

            if self.obj.overte.haze_enable_glare != False:
                haze["hazeEnableGlare"] = self.obj.overte.haze_enable_glare
                custom_haze = True

                c = self.get_color(self.obj.overte.haze_glare_color)["color"]
                if c["red"] != 255 or c["green"] != 229 or c["blue"] != 179:
                    haze["hazeGlareColor"] = c

                if self.obj.overte.haze_glare_angle != 20:
                    haze["hazeGlareAngle"] = self.obj.overte.haze_glare_angle

            if custom_haze:
                haze_option["haze"] = haze

        elif self.obj.overte.haze_mode == 'disabled':
            haze_option["hazeMode"] = "disabled"

        return haze_option

    def get_bloom_option(self):
        bloom_option = {}

        if self.obj.overte.bloom_mode == 'enabled':
            bloom_option["bloomMode"] = "enabled"
            bloom = {}
            custom_bloom = False

            if self.obj.overte.bloom_intensity != 0.25:
                bloom["bloomIntensity"] = self.obj.overte.bloom_intensity
                custom_haze = True

            if self.obj.overte.bloom_threshold != 0.7:
                bloom["bloomThreshold"] = self.obj.overte.bloom_threshold
                custom_haze = True

            if self.obj.overte.bloom_size != 0.9:
                bloom["bloomSize"] = self.obj.overte.bloom_size
                custom_haze = True

            if custom_haze:
                bloom_option["bloom"] = bloom

        elif self.obj.overte.bloom_mode == 'disabled':
            bloom_option["bloomMode"] = "disabled"

        return bloom_option

    def get_avatar_option(self):
        avatar_option = {}
        if self.obj.overte.avatar_priority != 'inherit':
            avatar_option["avatarPriority"] = self.obj.overte.avatar_priority
        if self.obj.overte.screen_share != 'inherit':
            avatar_option["screenshare"] = self.obj.overte.screen_share
        return avatar_option

    def export(self):
        entity = super().export("Zone")
        zone_data = self.get_zone_position_dimension(self.obj)

        zone_option = self.get_zone_option()
        skybox_option = self.get_skybox_option()
        ambient_option = self.get_ambient_option()
        keylight_option = self.get_keylight_option()
        haze_option = self.get_haze_option()
        bloom_option = self.get_bloom_option()
        avatar_option = self.get_avatar_option()

        zoneEntity = {
            "position": zone_data["position"],
            "dimensions": zone_data["dimensions"],
            "rotation": { "x": 0.0, "y": 0.00, "z": 0.00, "w": 1 },
            "queryAACube": zone_data["queryAACube"]
        }
        return {
            **entity, **zoneEntity, **zone_option, **skybox_option,
            **ambient_option, **keylight_option, **haze_option,
            **bloom_option, **avatar_option
        }

    def draw_panel(self, layout):
        row = layout.row()
        row.prop(self.obj.overte, "zone_margin")

        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "zone_shape_type")
        enabled = self.obj.overte.zone_shape_type == 'compound'
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "zone_compound_url")
        row = box.row()
        row.prop(self.obj.overte, "flying_allowed")
        row = box.row()
        row.prop(self.obj.overte, "ghosting_allowed")
        row = box.row()
        row.prop(self.obj.overte, "filter_url")

        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "skybox_mode")
        enabled = self.obj.overte.skybox_mode == 'enabled'
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "skybox_color")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "skybox_url")

        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "ambient_mode")
        enabled = self.obj.overte.ambient_mode == 'enabled'
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "ambient_intensity")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "ambient_url")

        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "keylight_mode")
        enabled = self.obj.overte.keylight_mode == 'enabled'
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "keylight_color")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "keylight_intensity")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "keylight_vertical")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "keylight_horizontal")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "keylight_cast_shadows")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "keylight_shadow_bias")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "keylight_shadow_distance")

        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "haze_mode")
        enabled = self.obj.overte.haze_mode == 'enabled'
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_range")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_use_altitude")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_base")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_ceiling")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_color")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_background_blend")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_enable_glare")
        enabled = self.obj.overte.haze_mode == 'enabled' and self.obj.overte.haze_enable_glare
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_glare_color")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "haze_glare_angle")

        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "bloom_mode")
        enabled = self.obj.overte.bloom_mode == 'enabled'
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "bloom_intensity")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "bloom_threshold")
        row = box.row()
        row.enabled = enabled
        row.prop(self.obj.overte, "bloom_size")

        box = layout.box()
        row = box.row()
        row.prop(self.obj.overte, "avatar_priority")
        row = box.row()
        row.prop(self.obj.overte, "screen_share")
        
        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_physics_panel(layout)
