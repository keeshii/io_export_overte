from ..asset_loader import AssetLoader
from ..export_params import ExportParams
from .base_entity import BaseEntity

class ModelEntity(BaseEntity):

    modelUrl = ''

    def __init__(self, obj):
        super().__init__(obj)
        self.modelUrl = AssetLoader.getOverteModelUrl(self.obj)

    def get_model(self):
        model = {}
        if self.obj.overte.shape_type != 'none':
            model["shapeType"] = self.obj.overte.shape_type

        if self.obj.overte.compound_shape_url != '':
            model["compoundShapeURL"] = self.obj.overte.compound_shape_url

        if self.obj.overte.use_original_pivot != False:
            model["useOriginalPivot"] = self.obj.overte.use_original_pivot

        if self.obj.overte.animation_url != '':
            animation = {}
            animation["url"] = self.obj.overte.animation_url
            if self.obj.overte.animation_running != False:
                animation["running"] = self.obj.overte.animation_running
    
            if self.obj.overte.animation_loop != True:
                animation["loop"] = self.obj.overte.animation_loop
    
            if self.obj.overte.animation_allow_translation != True:
                animation["allowTranslation"] = self.obj.overte.animation_allow_translation
    
            if self.obj.overte.animation_hold != False:
                animation["hold"] = self.obj.overte.animation_hold
    
            if self.obj.overte.animation_current_frame != 0:
                animation["currentFrame"] = self.obj.overte.animation_current_frame

            if self.obj.overte.animation_first_frame != 0:
                animation["firstFrame"] = self.obj.overte.animation_first_frame

            if self.obj.overte.animation_last_frame != 100000:
                animation["lastFrame"] = self.obj.overte.animation_last_frame

            if self.obj.overte.animation_fps != 30:
                animation["fps"] = self.obj.overte.animation_fps
            model["animation"] = animation

        if self.obj.overte.textures != '':
            model["textures"] = self.obj.overte.textures

        if self.obj.overte.group_culled != False:
            model["groupCulled"] = self.obj.overte.group_culled

        return model

    def export(self):
        entity = super().export("Model")
        model = self.get_model()

        modelEntity = {
            "position": self.get_position(),
            "dimensions": self.get_dimensions(),
            "rotation": self.get_rotation(),
            "queryAACube": self.get_query_aa_cube(),
            "modelURL": ExportParams.get_url(self.modelUrl)
        }
        return {**entity, **modelEntity, **model}

    def draw_model_panel(self, box):
        row = box.row()
        row.prop(self.obj.overte, "shape_type")
        row = box.row()
        row.prop(self.obj.overte, "compound_shape_url")
        row = box.row()
        row.prop(self.obj.overte, "use_original_pivot")

        box2 = box.box()
        row = box2.row()
        row.prop(self.obj.overte, "animation_url")
        row = box2.row()
        row.prop(self.obj.overte, "animation_running")
        row = box2.row()
        row.prop(self.obj.overte, "animation_loop")
        row = box2.row()
        row.prop(self.obj.overte, "animation_allow_translation")
        row = box2.row()
        row.prop(self.obj.overte, "animation_hold")
        row = box2.row()
        row.prop(self.obj.overte, "animation_current_frame")
        row = box2.row()
        row.prop(self.obj.overte, "animation_first_frame")
        row = box2.row()
        row.prop(self.obj.overte, "animation_last_frame")
        row = box2.row()
        row.prop(self.obj.overte, "animation_fps")

        row = box.row()
        row.prop(self.obj.overte, "textures")
        row = box.row()
        row.prop(self.obj.overte, "group_culled")


    def draw_panel(self, layout):
        box = layout.box()
        row = box.row()
        row.label(text="modelUrl: " + AssetLoader.getOverteModelUrl(self.obj))
        self.draw_model_panel(box)

        self.draw_entity_panel(layout)
        self.draw_behavior_panel(layout)
        self.draw_script_panel(layout)
        self.draw_collision_panel(layout)
        self.draw_physics_panel(layout)
