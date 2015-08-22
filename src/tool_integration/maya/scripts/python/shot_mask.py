###############################################################################
# Name: 
#   shot_mask.py
#
# Description: 
#   Creates a polygon shot mask for a camera
#
# Author: 
#   Chris Zurbrigg (http://zurbrigg.com)
#
# Copyright (C) 2014 Chris Zurbrigg. All rights reserved.
###############################################################################

import math

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

class ShotMask(object):
    
    VERSION = 1.02

    DEFAULT_BORDER_THICKNESS = 0.05
    DEFAULT_LABEL_PADDING = 0.1
    
    DEFAULT_BORDER_COLOR = [0.0, 0.0, 0.0, 0.0]
    DEFAULT_LABEL_COLOR = [1.0, 1.0, 1.0, 0.0]
    
    ROOT_NAME = "czShotMask"
    
    BORDER_GROUP_NAME = "czShotMaskBorderGrp"
    LABEL_GROUP_NAME = "czShotMaskLabelGrp"
    COUNTER_GROUP_NAME = "czShotMaskCounterGrp"
    
    LABEL_TOP_LEFT_GROUP_NAME = "czShotMaskLabelTopLeftGrp"
    LABEL_TOP_CENTER_GROUP_NAME = "czShotMaskLabelTopCenterGrp"
    LABEL_TOP_RIGHT_GROUP_NAME = "czShotMaskLabelTopRightGrp"
    LABEL_BOTTOM_LEFT_GROUP_NAME = "czShotMaskLabelBottomLeftGrp"
    LABEL_BOTTOM_CENTER_GROUP_NAME = "czShotMaskLabelBottomCenterGrp"
    LABEL_BOTTOM_RIGHT_GROUP_NAME = "czShotMaskLabelBottomRightGrp"
    
    TOP_BORDER_GEO_NAME = "czShotMaskTopBorderGeo"
    BOTTOM_BORDER_GEO_NAME = "czShotMaskBottomBorderGeo"
    
    BORDER_SHADER_NAME = "czShotMaskBorderShader"
    BORDER_SHADING_GROUP_NAME = "czShotMaskBorderSG"
    LABEL_SHADER_NAME = "czShotMaskLabelShader"
    LABEL_SHADING_GROUP_NAME = "czShotMaskLabelSG"
    
    COUNTER_SCRIPT_NODE_NAME = "czShotMaskCounterScriptNode"
    
    COUNTER_POSITION_TOP_LEFT = 0
    COUNTER_POSITION_TOP_RIGHT = 1
    COUNTER_POSITION_BOTTOM_LEFT = 2
    COUNTER_POSITION_BOTTOM_RIGHT = 3
    
    OPT_VAR_BORDER_COLOR = "czShotMaskBorderColorOptVar"
    OPT_VAR_LABEL_COLOR = "czShotMaskLabelColorOptVar"
    OPT_VAR_COUNTER_SETTINGS = "czShotMaskCounterSettingsOptVar"
    OPT_VAR_LABEL_TEXT = "czShotMaskLabelTextOptVar"
    OPT_VAR_LABEL_SETTINGS = "czShotMaskLabelSettingsOptVar"
    OPT_VAR_LABEL_FONT = "czShotMaskLabelFontOptVar"
    OPT_VAR_BORDER_VISIBLE = "czShotMaskBorderVisible"
    OPT_VAR_BORDER_SETTINGS = "czShotMaskBorderSettings"
    OPT_VAR_CAMERA_NAME = "czShotMaskCameraName"
    
    DEFAULT_COUNTER_PADDING = 4
    COUNTER_PADDING_MIN = 1
    COUNTER_PADDING_MAX = 6
    
    last_camera = None
    
    def __init__(self):
        pass
        
    def build(self, camera=None):
        self._camera = None
        if camera:
            if camera in ShotMask.cameras():
                self._camera = camera
            else:
                om.MGlobal.displayWarning('Camera "{0}" does not exist. Using current viewport camera.'.format(camera))
            
        if not self._camera:
            self._camera = ShotMask.active_camera()
            
        if not self._camera:
            om.MGlobal.displayError("Viewport not selected. Select viewport (or set the camera name) and rebuild.")
            return

        ShotMask.last_camera = self._camera

        ShotMask.delete()
        
        self.refresh_font_properties()
        self.refresh_shot_mask_properties()
        
        self.create_shaders()
        self.create_groups()
        self.create_borders()
        self.create_labels()
        self.create_counter()
        
        self.constrain_to_camera()
        
        ShotMask.update_settings()
        
        mel.eval(self.script_node_mel_cmd())
        
        cmds.select(clear=True)
        
    def create_shaders(self):
        shader_names = ShotMask.shader_names()
        
        for shader_name in shader_names.keys():
            if not cmds.objExists(shader_name):
                cmds.shadingNode("surfaceShader", asShader=True, name=shader_name)
                
                shading_grp_name = shader_names[shader_name]
                if not cmds.objExists(shading_grp_name):
                    cmds.sets(empty=True,
                              noSurfaceShader=True,
                              renderable=True,
                              name=shading_grp_name)
                
                cmds.connectAttr("{0}.outColor".format(shader_name),
                                 "{0}.surfaceShader".format(shading_grp_name),
                                 force=True)
    
    def assign_shader(self, shading_group_name, selection_list):
        cmds.sets(selection_list,
                  edit=True,
                  forceElement=shading_group_name)
        
    def create_groups(self):
        self._root = cmds.group(empty=True, name=ShotMask.ROOT_NAME)
        
        self._border_grp = cmds.group(empty=True, name=ShotMask.BORDER_GROUP_NAME, parent=self._root)
        self._label_grp = cmds.group(empty=True, name=ShotMask.LABEL_GROUP_NAME, parent=self._root)
        self._counter_grp = cmds.group(empty=True, name=ShotMask.COUNTER_GROUP_NAME, parent=self._root)
        
    def create_borders(self):
        self._top_border = cmds.polyPlane(width=self._width,
                                          height=self._border_height,
                                          subdivisionsX=1,
                                          subdivisionsY=1,
                                          constructionHistory=False,
                                          name=ShotMask.TOP_BORDER_GEO_NAME)[0]
        
        self._override_display_type(self._top_border)

        cmds.rotate(-90, 0, 0, self._top_border, absolute=True)
        cmds.move(0, self._top_border_center_y, -self._border_pos_z, self._top_border, absolute=True)
        
        self._bottom_border = cmds.duplicate(self._top_border, 
                                             name=ShotMask.BOTTOM_BORDER_GEO_NAME)[0]
        cmds.move(0, self._bottom_border_center_y, -self._border_pos_z, self._bottom_border, absolute=True)
        
        half_border_height = self._border_height * 0.5
        cmds.xform(self._top_border, pivots=(0, 0, half_border_height), relative=True)
        cmds.xform(self._bottom_border, pivots=(0, 0, -half_border_height), relative=True)
        cmds.makeIdentity(self._top_border, apply=True, translate=True, rotate=True, scale=True, normal=False)
        cmds.makeIdentity(self._bottom_border, apply=True, translate=True, rotate=True, scale=True, normal=False)
        
        
        cmds.parent(self._top_border, self._bottom_border, self._border_grp)
        
        self.assign_shader(ShotMask.BORDER_SHADING_GROUP_NAME,
                           [self._top_border, self._bottom_border])
        
        
    def create_labels(self):
        label_names = ShotMask.label_names()
        label_text = ShotMask.label_text()

        for i in range(0, len(label_names)):
            text = label_text[i]
            if text:
                label_grp = self.build_label_group(text)
                label_grp = cmds.rename(label_grp, label_names[i])
                cmds.parent(label_grp, self._label_grp)
                
                self.transform_label_group(label_grp, label_names[i])
                self.assign_shader(ShotMask.LABEL_SHADING_GROUP_NAME, label_grp)
            
    
    def build_label_group(self, label_text):
        label_curves_grp = cmds.textCurves(constructionHistory=0, text=label_text, font=ShotMask.label_font())
        character_grps = cmds.listRelatives(label_curves_grp[0], children=True)
        
        surface_nodes = []
        for grp in character_grps:
            srf = cmds.planarSrf(grp, 
                                 tolerance=0.01,
                                 constructionHistory=False,
                                 object=True, 
                                 polygon=True)
            surface_nodes.append(srf[0])
        
        cmds.delete(label_curves_grp)
        
        for node in surface_nodes:
            self._override_display_type(node)
            
        return cmds.group(surface_nodes)
        

    def transform_label_group(self, label_grp, label_name):
        
        bb = cmds.exactWorldBoundingBox(label_grp)
        pivots = [0, self._font_min_y, 0]

        if label_name in [ShotMask.LABEL_TOP_LEFT_GROUP_NAME, ShotMask.LABEL_BOTTOM_LEFT_GROUP_NAME]:
            pivots[0] = bb[0]
        elif label_name in [ShotMask.LABEL_TOP_CENTER_GROUP_NAME, ShotMask.LABEL_BOTTOM_CENTER_GROUP_NAME]:
            pivots[0] = (bb[3] - bb[0]) * 0.5
        elif label_name in [ShotMask.LABEL_TOP_RIGHT_GROUP_NAME, ShotMask.LABEL_BOTTOM_RIGHT_GROUP_NAME]:
            pivots[0] = bb[3]
        
        cmds.xform(label_grp, pivots=pivots)
        offset = cmds.xform(label_grp, q=True, pivots=True, worldSpace=True)
        
        position = [0, 0, -self._label_pos_z]
        if label_name == ShotMask.LABEL_TOP_LEFT_GROUP_NAME:
            position[0] = -offset[0] - self._label_plane_width * 0.5 + self._label_offset
            position[1] = -offset[1] + self._label_plane_height * 0.5 - self._label_plane_border_height
        elif label_name == ShotMask.LABEL_TOP_CENTER_GROUP_NAME:
            position[0] = -offset[0]
            position[1] = -offset[1] + self._label_plane_height * 0.5 - self._label_plane_border_height
        elif label_name == ShotMask.LABEL_TOP_RIGHT_GROUP_NAME:
            position[0] = -offset[0] + self._label_plane_width * 0.5 - self._label_offset
            position[1] = -offset[1] + self._label_plane_height * 0.5 - self._label_plane_border_height
            
        elif label_name == ShotMask.LABEL_BOTTOM_LEFT_GROUP_NAME:
            position[0] = -offset[0] - self._label_plane_width * 0.5 + self._label_offset
            position[1] = -offset[1] - self._label_plane_height * 0.5
        elif label_name == ShotMask.LABEL_BOTTOM_CENTER_GROUP_NAME:
            position[0] = -offset[0]
            position[1] = -offset[1] - self._label_plane_height * 0.5
        elif label_name == ShotMask.LABEL_BOTTOM_RIGHT_GROUP_NAME:
            position[0] = -offset[0] + self._label_plane_width * 0.5 - self._label_offset
            position[1] = -offset[1] - self._label_plane_height * 0.5
        
        position[1] += self._label_offset
        cmds.move(position[0], position[1], position[2], label_grp, absolute=True)
        
        cmds.scale(self._label_scale, self._label_scale, self._label_scale, label_grp)
        
        cmds.makeIdentity(label_grp, apply=True, translate=True, rotate=True, scale=True, normal=False)
    
    def create_counter(self):
        script_node = cmds.scriptNode(scriptType=7,
                                      beforeScript=self.script_node_mel_cmd(),
                                      name=ShotMask.COUNTER_SCRIPT_NODE_NAME)
        
        counter_grp = ShotMask.COUNTER_GROUP_NAME
        for i in range(0, ShotMask.counter_padding()):
            place_grp = cmds.group(empty=True, 
                                   name="czShotMaskCounterPlace{0}Grp".format(i), 
                                   parent=counter_grp)
            
            for j in range(0, 10):
                number_grp = self.build_label_group(str(j))
                number_grp = cmds.rename(number_grp, "czShotMaskDigit{0}{1}Grp".format(i, j))
                
                if j != 0:
                    cmds.setAttr("{0}.visibility".format(number_grp), False)
                
                cmds.parent(number_grp, place_grp)

            bounding_box = cmds.exactWorldBoundingBox(place_grp)
            place_width = bounding_box[3] - bounding_box[0]
            place_height = bounding_box[4] - bounding_box[1]
            
            offset = -place_width * (i + 1)
            offset *= 1.05
            cmds.move(offset,
                      0,
                      -self._label_pos_z,
                      place_grp,
                      absolute=True)
            
            cmds.makeIdentity(place_grp, apply=True, translate=True, rotate=True, scale=True, normal=False)
            
            self.assign_shader(ShotMask.LABEL_SHADING_GROUP_NAME, place_grp)
            
        
        counter_position = ShotMask.counter_position()
        
        bb = cmds.exactWorldBoundingBox(counter_grp)
        if counter_position == ShotMask.COUNTER_POSITION_TOP_LEFT or counter_position == ShotMask.COUNTER_POSITION_BOTTOM_LEFT:
            pivots = [bb[0], self._font_min_y, 0]
        else:
            pivots = [bb[3], self._font_min_y, 0]
        
        cmds.xform(counter_grp, pivots=pivots)
        offset = cmds.xform(counter_grp, q=True, pivots=True, worldSpace=True)
        
        position = [0, 0, -self._label_pos_z]
        if counter_position == ShotMask.COUNTER_POSITION_TOP_LEFT:
            position[0] = -offset[0] - self._label_plane_width * 0.5 + self._label_offset
            position[1] = -offset[1] + self._label_plane_height * 0.5 - self._label_plane_border_height
        elif counter_position == ShotMask.COUNTER_POSITION_TOP_RIGHT:
            position[0] = -offset[0] + self._label_plane_width * 0.5 - self._label_offset
            position[1] = -offset[1] + self._label_plane_height * 0.5 - self._label_plane_border_height
        elif counter_position == ShotMask.COUNTER_POSITION_BOTTOM_LEFT:
            position[0] = -offset[0] - self._label_plane_width * 0.5 + self._label_offset
            position[1] = -offset[1] - self._label_plane_height * 0.5
        elif counter_position == ShotMask.COUNTER_POSITION_BOTTOM_RIGHT:
            position[0] = -offset[0] + self._label_plane_width * 0.5 - self._label_offset
            position[1] = -offset[1] - self._label_plane_height * 0.5
        
        position[1] += self._label_offset
        cmds.move(position[0], position[1], position[2], counter_grp, absolute=True)
        
        cmds.scale(self._label_scale, self._label_scale, self._label_scale, counter_grp)
        
        cmds.makeIdentity(counter_grp, apply=True, translate=True, rotate=True, scale=True, normal=False)
        
    def script_node_mel_cmd(self):
        max_value = int(10 ** ShotMask.counter_padding())
        
        cmd = '{\n'
        cmd += '$czSnCurrentTime = `currentTime -q`;\n'
        cmd += '$czSnPlaceIndex = 0;\n'
        cmd += 'for ($i = 1; $i < {0}; $i *= 10) {{\n'.format(max_value)
        cmd += '  $visibleDigit=int($czSnCurrentTime / $i) % 10;\n'
        
        cmd += '  for ($j = 0; $j < 10; $j++) {\n'
        cmd += '    $czDigitGrpVis = "czShotMaskDigit" + $czSnPlaceIndex + $j + "Grp.visibility";\n'
        cmd += '    if (!`objExists $czDigitGrpVis`)\n'
        cmd += '      continue;\n'
        cmd += '    if ($j == $visibleDigit)\n'
        cmd += '      setAttr $czDigitGrpVis 1;\n'
        cmd += '    else\n'
        cmd += '      setAttr $czDigitGrpVis 0;\n'
        cmd += '  }\n'
        
        cmd += '  $czSnPlaceIndex++;\n'
        
        cmd += '}\n}\n'
        return cmd
    
    def constrain_to_camera(self):
        cmds.parentConstraint(self._camera, self._root, weight=1)
    
    
    def query_camera(self, **kwargs):
        return cmds.camera(self._camera, q=True, **kwargs)
        
    def refresh_font_properties(self):
        temp_label = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        temp_grp = self.build_label_group(temp_label)
        bb = cmds.exactWorldBoundingBox(temp_grp)
        self._font_height = bb[4] - bb[1]
        self._font_min_y = bb[1]
        cmds.delete(temp_grp)
        
        
    def refresh_shot_mask_properties(self):

        self._near_clip = self.query_camera(nearClipPlane=True)
        if self._near_clip < 0.1:
            self._near_clip = 0.1
            
        self._border_pos_z = self._near_clip + (self._near_clip * 0.1)
        self._label_pos_z = self._near_clip + (self._near_clip * 0.09)
        self._film_fit = self.query_camera(filmFit=True)
        self._aspect_ratio = cmds.getAttr("defaultResolution.deviceAspectRatio")
        self._camera_aspect_ratio = self.query_camera(aspectRatio=True)
        
        if self.query_camera(orthographic=True):
            self._width = self.query_camera(orthographicWidth=True)
            self._height = self._width / self._aspect_ratio
            self._label_plane_width = self._width
            self._label_plane_height = self._height
            
        else:
            scale = 1.0
            if self._film_fit == "horizontal":
                fov = math.radians(self.query_camera(horizontalFieldOfView=True))
            elif self._film_fit == "vertical":
                fov = math.radians(self.query_camera(verticalFieldOfView=True))
            elif self._film_fit == "fill":
                fov = math.radians(self.query_camera(horizontalFieldOfView=True))
                if self._camera_aspect_ratio > self._aspect_ratio:
                    scale = self._aspect_ratio / self._camera_aspect_ratio
            elif self._film_fit == "overscan":
                fov = math.radians(self.query_camera(horizontalFieldOfView=True))
                if self._camera_aspect_ratio < self._aspect_ratio:
                    scale = self._aspect_ratio / self._camera_aspect_ratio
            
            if self._film_fit == "vertical":
                self._height = 2 * math.tan(fov * 0.5) * self._border_pos_z * scale
                self._width = self._height * self._aspect_ratio
                
                self._label_plane_height = 2 * math.tan(fov * 0.5) * self._label_pos_z * scale
                self._label_plane_width = self._label_plane_height * self._aspect_ratio
            else:
                self._width = 2 * math.tan(fov * 0.5) * self._border_pos_z * scale
                self._height = self._width / self._aspect_ratio
                
                self._label_plane_width = 2 * math.tan(fov * 0.5) * self._label_pos_z * scale
                self._label_plane_height = self._label_plane_width / self._aspect_ratio
        
        # top, left, bottom, right
        self._rect = [self._height * 0.5, -self._width * 0.5, -self._height * 0.5, self._width * 0.5]
        
        self._border_height = ShotMask.border_thickness() * self._height
        self._label_plane_border_height = ShotMask.border_thickness() * self._label_plane_height
        
        self._top_border_center_y = self._rect[0] - (self._border_height * 0.5)
        self._bottom_border_center_y = self._rect[2] + (self._border_height * 0.5)
    
        self._label_offset = ShotMask.DEFAULT_LABEL_PADDING * self._label_plane_border_height
        self._label_scale = self._label_plane_border_height / self._font_height * (1 - ShotMask.DEFAULT_LABEL_PADDING * 2)
    
    def _override_display_type(self, node):
        shape_nodes = cmds.listRelatives(node, shapes=True)
        for shape_node in shape_nodes:
            cmds.setAttr("{0}.overrideEnabled".format(shape_node), True)
            cmds.setAttr("{0}.overrideDisplayType".format(shape_node), 2)
    
    @classmethod
    def author(cls):
        name = chr(67) + chr(104) + chr(114) + chr(105) + chr(115) + chr(32)
        name += chr(90) + chr(117) + chr(114) + chr(98) + chr(114) + chr(105) + chr(103) + chr(103)
        return name
        
    @classmethod
    def website(cls):
        address = chr(104) + chr(116) + chr(116) + chr(112) + chr(58) + chr(47) + chr(47)
        address += chr(122) + chr(117) + chr(114) + chr(98) + chr(114) + chr(105) + chr(103) + chr(103) + chr(46) + chr(99) + chr(111) + chr(109)
        return address
    
    @classmethod
    def create(cls, camera=None):
        sm = ShotMask()
        sm.build(camera)
    
    @classmethod
    def delete(cls):
        # Delete root group
        if cmds.objExists(ShotMask.ROOT_NAME):
            cmds.delete(ShotMask.ROOT_NAME)
            
        # Delete script node
        if cmds.objExists(ShotMask.COUNTER_SCRIPT_NODE_NAME):
            cmds.delete(ShotMask.COUNTER_SCRIPT_NODE_NAME)
        
        # Delete shaders and shading groups
        shader_names = ShotMask.shader_names()
        for shader_name in shader_names:
            if cmds.objExists(shader_name):
                cmds.delete(shader_name)
                
            shading_grp_name = shader_names[shader_name]
            if cmds.objExists(shading_grp_name):
                cmds.delete(shading_grp_name)
    
    @classmethod
    def exists(cls):
        if cmds.objExists(cls.ROOT_NAME):
            return True
        else:
            return False
    
    @classmethod
    def update_settings(cls):
        if not cls.exists():
            return
            
        for shader_name in cls.shader_names():
            color_attr = "{0}.outColor".format(shader_name)
            transparency_attr = "{0}.outTransparency".format(shader_name)
            if shader_name == cls.BORDER_SHADER_NAME:
                color =  cls.border_color()
            elif shader_name == cls.LABEL_SHADER_NAME:
                color = cls.label_color()
            
            cmds.setAttr(color_attr, color[0], color[1], color[2], type="double3")
            cmds.setAttr(transparency_attr, color[3], color[3], color[3], type="double3")
            
        border_vis = cls.border_visible()
        cmds.setAttr("{0}.visibility".format(cls.TOP_BORDER_GEO_NAME), border_vis[0])
        cmds.setAttr("{0}.visibility".format(cls.BOTTOM_BORDER_GEO_NAME), border_vis[1])
        
        scale = cls.border_scale()
        
        cmds.setAttr("{0}.scale".format(cls.TOP_BORDER_GEO_NAME), 1, scale[0], 1)
        cmds.setAttr("{0}.scale".format(cls.BOTTOM_BORDER_GEO_NAME), 1, scale[1], 1)
            
        csettings = cls.counter_settings()
        cmds.setAttr("{0}.visibility".format(cls.COUNTER_GROUP_NAME), csettings[1])
        cmds.setAttr("{0}.scale".format(cls.COUNTER_GROUP_NAME), csettings[2], csettings[2], csettings[2])
        cmds.setAttr("{0}.tx".format(cls.COUNTER_GROUP_NAME), csettings[3])
        cmds.setAttr("{0}.ty".format(cls.COUNTER_GROUP_NAME), csettings[4])
        
        label_names = cls.label_names()
        for i in range(0, len(label_names)):
            label_name = label_names[i]
            if not cmds.objExists(label_name):
                continue
            
            offset = cls.label_offset(i)
            scale = cls.label_scale(i)
            cmds.setAttr("{0}.scale".format(label_name), scale, scale, scale)
            cmds.setAttr("{0}.tx".format(label_name), offset[0])
            cmds.setAttr("{0}.ty".format(label_name), offset[1])
            
        
            
    
    @classmethod
    def active_camera(cls):
        panel = cmds.getPanel(withFocus=True)
        if (cmds.getPanel(typeOf=panel) == "modelPanel"):
            camera = cmds.modelEditor(panel, q=True, camera=True)
        else:
            return None
        
        return camera
    
    @classmethod
    def label_names(cls):
        return [cls.LABEL_TOP_LEFT_GROUP_NAME, 
                cls.LABEL_TOP_CENTER_GROUP_NAME,
                cls.LABEL_TOP_RIGHT_GROUP_NAME,
                cls.LABEL_BOTTOM_LEFT_GROUP_NAME, 
                cls.LABEL_BOTTOM_CENTER_GROUP_NAME,
                cls.LABEL_BOTTOM_RIGHT_GROUP_NAME]
        
    @classmethod
    def shader_names(cls):
        return {cls.BORDER_SHADER_NAME:cls.BORDER_SHADING_GROUP_NAME,
                cls.LABEL_SHADER_NAME:cls.LABEL_SHADING_GROUP_NAME}
        
        
    @classmethod
    def set_label_color(cls, red, green, blue, transparency):
        cmds.optionVar(fv=[cls.OPT_VAR_LABEL_COLOR, red])
        cmds.optionVar(fva=[cls.OPT_VAR_LABEL_COLOR, green])
        cmds.optionVar(fva=[cls.OPT_VAR_LABEL_COLOR, blue])
        cmds.optionVar(fva=[cls.OPT_VAR_LABEL_COLOR, transparency])
        cls.update_settings()
        
    @classmethod
    def label_color(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_COLOR):
            return cmds.optionVar(q=cls.OPT_VAR_LABEL_COLOR)
        else:
            return cls.DEFAULT_LABEL_COLOR
        
    @classmethod
    def set_border_color(cls, red, green, blue, transparency):
        cmds.optionVar(fv=[cls.OPT_VAR_BORDER_COLOR, red])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_COLOR, green])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_COLOR, blue])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_COLOR, transparency])
        cls.update_settings()
        
    @classmethod
    def border_color(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_BORDER_COLOR):
            return cmds.optionVar(q=cls.OPT_VAR_BORDER_COLOR)
        else:
            return cls.DEFAULT_BORDER_COLOR
            
    @classmethod
    def set_border_visible(cls, top, bottom):
        cmds.optionVar(iv=[cls.OPT_VAR_BORDER_VISIBLE, top])
        cmds.optionVar(iva=[cls.OPT_VAR_BORDER_VISIBLE, bottom])
        cls.update_settings()
        
    @classmethod
    def border_visible(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_BORDER_VISIBLE):
            return cmds.optionVar(q=cls.OPT_VAR_BORDER_VISIBLE)
        else:
            return [1, 1]
            
    @classmethod
    def set_border_thickness(cls, thickness):
        scale = cls.border_scale()
        cmds.optionVar(fv=[cls.OPT_VAR_BORDER_SETTINGS, thickness])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_SETTINGS, scale[0]])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_SETTINGS, scale[1]])
        cls.update_settings()
        
    @classmethod
    def border_thickness(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_BORDER_SETTINGS):
            return cmds.optionVar(q=cls.OPT_VAR_BORDER_SETTINGS)[0]
        else:
            return cls.DEFAULT_BORDER_THICKNESS
            
    @classmethod
    def set_border_scale(cls, top_scale, bottom_scale):
        cmds.optionVar(fv=[cls.OPT_VAR_BORDER_SETTINGS, cls.border_thickness()])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_SETTINGS, top_scale])
        cmds.optionVar(fva=[cls.OPT_VAR_BORDER_SETTINGS, bottom_scale])
        cls.update_settings()
        
    @classmethod
    def border_scale(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_BORDER_SETTINGS):
            return cmds.optionVar(q=cls.OPT_VAR_BORDER_SETTINGS)[1:3]
        else:
            return [1.0, 1.0]
            
    @classmethod
    def set_counter_settings(cls, position, visibility, scale, offset_x, offset_y, padding):
        if scale < 0.1:
            scale = 0.1
        
        if padding < cls.COUNTER_PADDING_MIN:
            padding = cls.COUNTER_PADDING_MIN
        if padding > cls.COUNTER_PADDING_MAX:
            padding = cls.COUNTER_PADDING_MAX
        
        cmds.optionVar(fv=[cls.OPT_VAR_COUNTER_SETTINGS, position])        # 0
        cmds.optionVar(fva=[cls.OPT_VAR_COUNTER_SETTINGS, visibility])     # 1
        cmds.optionVar(fva=[cls.OPT_VAR_COUNTER_SETTINGS, scale])          # 2
        cmds.optionVar(fva=[cls.OPT_VAR_COUNTER_SETTINGS, offset_x])       # 3
        cmds.optionVar(fva=[cls.OPT_VAR_COUNTER_SETTINGS, offset_y])       # 4
        cmds.optionVar(fva=[cls.OPT_VAR_COUNTER_SETTINGS, padding])        # 5
        cls.update_settings()
    
    @classmethod
    def counter_settings(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_COUNTER_SETTINGS):
            return cmds.optionVar(q=cls.OPT_VAR_COUNTER_SETTINGS)
        else:
            return [3.0, 1.0, 1.0, 0.0, 0.0, 4.0]
    
    @classmethod
    def counter_position(cls):
        return int(cls.counter_settings()[0])
        
    @classmethod
    def set_counter_position(cls, position):
        settings = cls.counter_settings()
        settings[0] = position
        cls.set_counter_settings(*settings)
        
    @classmethod
    def set_counter_scale(cls, scale):
        settings = cls.counter_settings()
        settings[2] = scale
        cls.set_counter_settings(*settings)

    @classmethod
    def counter_scale(cls):
        return cls.counter_settings()[2]
        
    @classmethod
    def set_counter_offset(cls, offset_x, offset_y):
        settings = cls.counter_settings()
        settings[3] = offset_x
        settings[4] = offset_y
        cls.set_counter_settings(*settings)
        
    @classmethod
    def counter_offset(cls):
        return cls.counter_settings()[3:5]
    
    @classmethod
    def set_counter_padding(cls, padding):
        settings = cls.counter_settings()
        settings[5] = padding
        cls.set_counter_settings(*settings)
        
    @classmethod
    def counter_padding(cls):
        return int(cls.counter_settings()[5])
    
    @classmethod
    def set_label_text(cls, position, text):
        label_text = cls.label_text()
        label_text[position] = text
        
        cmds.optionVar(sv=[cls.OPT_VAR_LABEL_TEXT, label_text[0]])
        for i in range(1, len(label_text)):
            cmds.optionVar(sva=[cls.OPT_VAR_LABEL_TEXT, label_text[i]])
        
    @classmethod
    def label_text(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_TEXT):
            return cmds.optionVar(q=cls.OPT_VAR_LABEL_TEXT)
        else:
            return ["Shot Name", "", "Animator Name", "", "", ""]
    
    @classmethod
    def set_label_settings(cls, position, scale, offset_x, offset_y):
        settings = cls.label_settings()
        start_index = position * 3
        settings[start_index] = scale
        settings[start_index+1] = offset_x
        settings[start_index+2] = offset_y
        
        cmds.optionVar(fv=[cls.OPT_VAR_LABEL_SETTINGS, settings[0]])
        for i in range(1, len(settings)):
            cmds.optionVar(fva=[cls.OPT_VAR_LABEL_SETTINGS, settings[i]])
            
        cls.update_settings()
        
    @classmethod
    def label_settings(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_SETTINGS):
            settings = cmds.optionVar(q=cls.OPT_VAR_LABEL_SETTINGS)
        else:
            settings = []
            for i in range(0, len(cls.label_names())):
                settings.extend([1.0, 0.0, 0.0])
                
        return settings
        
    @classmethod
    def set_label_scale(cls, position, scale):
        offset = cls.label_offset(position)
        cls.set_label_settings(position, scale, offset[0], offset[1])
        
    @classmethod
    def label_scale(cls, position):
        settings = cls.label_settings()
        return settings[position * 3]
        
    @classmethod
    def set_label_offset(cls, position, offset_x, offset_y):
        scale = cls.label_scale(position)
        cls.set_label_settings(position, scale, offset_x, offset_y)
        
    @classmethod
    def label_offset(cls, position):
        settings = cls.label_settings()
        offset_index = position * 3 + 1
        return [settings[offset_index], settings[offset_index+1]]

    @classmethod
    def set_label_font(cls, font):
        cmds.optionVar(sv=[cls.OPT_VAR_LABEL_FONT, font])

    @classmethod
    def label_font(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_LABEL_FONT):
            return cmds.optionVar(q=cls.OPT_VAR_LABEL_FONT)
        else:
            if cmds.about(win=True):
                return "Times New Roman|h-13|w400|c0"
            elif cmds.about(mac=True):
                return "Times New Roman-Regular"
            elif cmds.about(linux=True):
                return "Courier"
            else:
                return "Times-Roman"
            
    @classmethod
    def set_camera_name(cls, name):
        cmds.optionVar(sv=[cls.OPT_VAR_CAMERA_NAME, name])
        
    @classmethod
    def camera_name(cls):
        if cmds.optionVar(exists=cls.OPT_VAR_CAMERA_NAME):
            return cmds.optionVar(q=cls.OPT_VAR_CAMERA_NAME)
        else:
            return ""
    
    
    @classmethod
    def restore_defaults(cls):
        cmds.optionVar(remove=cls.OPT_VAR_BORDER_COLOR)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_COLOR)
        cmds.optionVar(remove=cls.OPT_VAR_COUNTER_SETTINGS)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_TEXT)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_SETTINGS)
        cmds.optionVar(remove=cls.OPT_VAR_LABEL_FONT)
        cmds.optionVar(remove=cls.OPT_VAR_BORDER_VISIBLE)
        cmds.optionVar(remove=cls.OPT_VAR_BORDER_SETTINGS)
        cmds.optionVar(remove=cls.OPT_VAR_CAMERA_NAME)
    
    @classmethod
    def cameras(cls):
        return cmds.listCameras()

    @classmethod
    def author_alt(cls):
        name = chr(67) + chr(104) + chr(114) + chr(105) + chr(115) + chr(32)
        name += chr(90) + chr(117) + chr(114) + chr(98) + chr(114) + chr(105) + chr(103) + chr(103)
        return name
        
    @classmethod
    def website_alt(cls):
        address = chr(104) + chr(116) + chr(116) + chr(112) + chr(58) + chr(47) + chr(47)
        address += chr(122) + chr(117) + chr(114) + chr(98) + chr(114) + chr(105) + chr(103) + chr(103) + chr(46) + chr(99) + chr(111) + chr(109)
        return address
        
class ShotMaskUi(object):
    
    WINDOW_NAME = "czShotMaskUi"
    
    LABELS = ["Top-Left  ", "Top-Center  ", "Top-Right  ", 
              "Bottom-Left  ", "Bottom-Center  ", "Bottom-Right  "]
    
    @classmethod
    def display(cls):
        cls.delete()
        
        print("\nZurbrigg Shot Mask")
        print("Created by: {0} ({1})\n".format(ShotMask.author(), ShotMask.website()))
        
        main_window = cmds.window(cls.WINDOW_NAME, 
                                  title="Zurbrigg Shot Mask (http://zurbrigg.com)",
                                  sizeable=True,
                                  menuBar=True)
        edit_menu = cmds.menu(label="Edit", parent=main_window)
        
        menu_item = cmds.menuItem(label="Reset Settings",
                                  command="ShotMaskUi.reset_settings()",
                                  parent=edit_menu)
        help_menu = cmds.menu(label="Help", parent=main_window)
        menu_item = cmds.menuItem(label="About", 
                                  command="ShotMaskUi.about()",
                                  parent=help_menu)
        
        main_layout = cmds.columnLayout(adjustableColumn=True, parent=main_window)
        
        # Camera Section
        camera_layout = cmds.frameLayout(label="Camera",
                                         borderStyle="in",
                                         parent=main_layout)
        camera_form_layout = cmds.formLayout(parent=camera_layout)
        
        cls.camera_name = cmds.textFieldButtonGrp(label="Name  ",
                                                  buttonLabel=" ... ",
                                                  columnWidth=(1, 90),
                                                  changeCommand="ShotMaskUi.camera_changed()",
                                                  buttonCommand="ShotMaskUi.display_camera_dialog()",
                                                  parent=camera_form_layout)
        
        helper_text = cmds.text(label="(Active viewport camera used if empty or invalid)") 
        
        cmds.formLayout(camera_form_layout, e=True, af=(cls.camera_name, "top", 3))
        cmds.formLayout(camera_form_layout, e=True, af=(cls.camera_name, "left", 0))
        cmds.formLayout(camera_form_layout, e=True, ac=(helper_text, "top", 4, cls.camera_name))
        cmds.formLayout(camera_form_layout, e=True, af=(helper_text, "left", 96))
        cmds.formLayout(camera_form_layout, e=True, af=(helper_text, "bottom", 5))
        
        # Labels Section
        label_layout = cmds.frameLayout(label="Labels",
                                        borderStyle="in",
                                        parent=main_layout)
        label_form_layout = cmds.formLayout(parent=label_layout)
        
        cls.label_text_ctrls = []
        cls.label_settings_scale_ctrls = []
        cls.label_settings_offset_x_ctrls = []
        cls.label_settings_offset_y_ctrls = []
        
        scale_text = cmds.text(label="Scale")
        offset_text = cmds.text(label="Offset")
        
        label_text = ShotMask.label_text()
        
        for i in range(0, len(label_text)):
            cls.create_label_fields(i, label_form_layout);
        
        cls.label_font_tfg = cmds.textFieldButtonGrp(label="Font  ",
                                                     buttonLabel=" ... ",
                                                     columnWidth=(1, 90),
                                                     editable=False,
                                                     buttonCommand="ShotMaskUi.display_font_dialog()",
                                                     parent=label_form_layout)
        
        cls.label_color_csg = cmds.colorSliderGrp(label="Color  ",
                                                  columnWidth=(1,90),
                                                  changeCommand="ShotMaskUi.label_color_changed()",
                                                  dragCommand="ShotMaskUi.label_color_changed()",
                                                  parent=label_form_layout)
        cls.label_trans_csg = cmds.colorSliderGrp(label="Transparency  ",
                                                  columnWidth=(1,90),
                                                  changeCommand="ShotMaskUi.label_color_changed()",
                                                  dragCommand="ShotMaskUi.label_color_changed()",
                                                  parent=label_form_layout)
        
        cmds.formLayout(label_form_layout, e=True, af=(scale_text, "top", 3))
        cmds.formLayout(label_form_layout, e=True, af=(scale_text, "left", 350))
        cmds.formLayout(label_form_layout, e=True, af=(offset_text, "top", 3))
        cmds.formLayout(label_form_layout, e=True, ac=(offset_text, "left", 50, scale_text))
        
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_text_ctrls[0], "top", 0, scale_text))
        cmds.formLayout(label_form_layout, e=True, af=(cls.label_text_ctrls[0], "left", 0))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_settings_scale_ctrls[0], "top", 0, cls.label_text_ctrls[0]))
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_settings_scale_ctrls[0], "left", 0, cls.label_text_ctrls[0]))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_settings_offset_x_ctrls[0], "top", 0, cls.label_text_ctrls[0]))
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_settings_offset_x_ctrls[0], "left", 0, cls.label_settings_scale_ctrls[0]))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_settings_offset_y_ctrls[0], "top", 0, cls.label_text_ctrls[0]))
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_settings_offset_y_ctrls[0], "left", 0, cls.label_settings_offset_x_ctrls[0]))
        #cmds.formLayout(label_form_layout, e=True, af=(cls.label_settings_offset_y_ctrls[0], "right", 8))
        
        label_text_count = len(cls.label_text_ctrls)
        for i in range(1, label_text_count):
            cmds.formLayout(label_form_layout, e=True, ac=(cls.label_text_ctrls[i], "top", 0, cls.label_text_ctrls[i-1]))
            cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_text_ctrls[i], "left", 0, cls.label_text_ctrls[i-1]))
            cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_settings_scale_ctrls[i], "top", 0, cls.label_text_ctrls[i]))
            cmds.formLayout(label_form_layout, e=True, ac=(cls.label_settings_scale_ctrls[i], "left", 0, cls.label_text_ctrls[i]))
            cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_settings_offset_x_ctrls[i], "top", 0, cls.label_text_ctrls[i]))
            cmds.formLayout(label_form_layout, e=True, ac=(cls.label_settings_offset_x_ctrls[i], "left", 0, cls.label_settings_scale_ctrls[i]))
            cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_settings_offset_y_ctrls[i], "top", 0, cls.label_text_ctrls[i]))
            cmds.formLayout(label_form_layout, e=True, ac=(cls.label_settings_offset_y_ctrls[i], "left", 0, cls.label_settings_offset_x_ctrls[i]))
            
        
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_font_tfg, "top", 0, cls.label_text_ctrls[label_text_count-1]))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_font_tfg, "left", 0, cls.label_text_ctrls[label_text_count-1]))
        
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_color_csg, "top", 0, cls.label_font_tfg))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_color_csg, "left", 0, cls.label_font_tfg))
        cmds.formLayout(label_form_layout, e=True, ac=(cls.label_trans_csg, "top", 0, cls.label_color_csg))
        cmds.formLayout(label_form_layout, e=True, aoc=(cls.label_trans_csg, "left", 0, cls.label_color_csg))
        cmds.formLayout(label_form_layout, e=True, af=(cls.label_trans_csg, "bottom", 5))
        
        # Counter Section
        counter_layout = cmds.frameLayout(label="Counter",
                                          borderStyle="in",
                                          parent=main_layout)
        counter_form_layout = cmds.formLayout(parent=counter_layout)
        
        
        cls.counter_vis_cbg = cmds.checkBoxGrp(numberOfCheckBoxes=1,
                                               label="",
                                               label1=("Enable"),
                                               columnWidth2=(90, 60),
                                               changeCommand="ShotMaskUi.counter_settings_changed()",
                                               parent=counter_form_layout)
        cls.counter_position = cmds.radioButtonGrp(numberOfRadioButtons=4,
                                                   label="",
                                                   columnWidth5=(90, 86, 86, 86, 86),
                                                   labelArray4=("Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"),
                                                   changeCommand="ShotMaskUi.counter_settings_changed(rebuild=True)",
                                                   parent=counter_form_layout)
        counter_padding_label = cmds.text("Padding  ", align="right", width=93, parent=counter_form_layout)
        cls.counter_padding = cmds.intField(width=50,
                                            value=1,
                                            minValue=1,
                                            maxValue=6,
                                            step=1,
                                            changeCommand="ShotMaskUi.counter_settings_changed(rebuild=True)",
                                            parent=counter_form_layout)
        counter_scale_label = cmds.text("Scale  ", align="right", width=93, parent=counter_form_layout)
        cls.counter_scale = cmds.floatField(width=50,
                                            value=1,
                                            minValue=0.1,
                                            step=0.01,
                                            precision=2,
                                            dragCommand="ShotMaskUi.counter_settings_changed()",
                                            changeCommand="ShotMaskUi.counter_settings_changed()",
                                            parent=counter_form_layout)
        counter_offset_label = cmds.text("Offset  ", align="right", width=93, parent=counter_form_layout)
        cls.counter_offset_x = cmds.floatField(width=50,
                                               precision=4,
                                               step=0.0001,
                                               dragCommand="ShotMaskUi.counter_settings_changed()",
                                               changeCommand="ShotMaskUi.counter_settings_changed()",
                                               parent=counter_form_layout)
        cls.counter_offset_y = cmds.floatField(width=50,
                                               precision=4,
                                               step=0.0001,
                                               dragCommand="ShotMaskUi.counter_settings_changed()",
                                               changeCommand="ShotMaskUi.counter_settings_changed()",
                                               parent=counter_form_layout)
        

        cmds.formLayout(counter_form_layout, e=True, af=(cls.counter_vis_cbg, "top", 3))
        cmds.formLayout(counter_form_layout, e=True, af=(cls.counter_vis_cbg, "left", 0))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_position, "top", 0, cls.counter_vis_cbg))
        
        cmds.formLayout(counter_form_layout, e=True, ac=(counter_padding_label, "top", 4, cls.counter_position))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_padding, "top", 0, cls.counter_position))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_padding, "left", 0, counter_padding_label))
        
        cmds.formLayout(counter_form_layout, e=True, ac=(counter_scale_label, "top", 4, cls.counter_padding))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_scale, "top", 0, cls.counter_padding))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_scale, "left", 0, counter_scale_label))
        
        cmds.formLayout(counter_form_layout, e=True, ac=(counter_offset_label, "top", 4, cls.counter_scale))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_offset_x, "top", 0, cls.counter_scale))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_offset_x, "left", 0, counter_offset_label))
        cmds.formLayout(counter_form_layout, e=True, af=(cls.counter_offset_x, "bottom", 5))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_offset_y, "top", 0, cls.counter_scale))
        cmds.formLayout(counter_form_layout, e=True, ac=(cls.counter_offset_y, "left", 0, cls.counter_offset_x))
        
        
        # Border Section
        border_layout = cmds.frameLayout(label="Border",
                                         borderStyle="in",
                                         parent=main_layout)
        
        border_form_layout = cmds.formLayout(parent=border_layout)
        cls.border_vis_cbg = cmds.checkBoxGrp(numberOfCheckBoxes=2,
                                              label="",
                                              labelArray2=("Top", "Bottom"),
                                              columnWidth3=(90, 60, 60),
                                              changeCommand="ShotMaskUi.border_visibility_changed()",
                                              parent=border_form_layout)
        border_thickness_label = cmds.text("Thickness  ", align="right", width=93, parent=border_form_layout)
        cls.border_thickness = cmds.floatField(width=50,
                                               value=ShotMask.DEFAULT_BORDER_THICKNESS,
                                               minValue=0.01,
                                               maxValue=1.00,
                                               precision=2,
                                               changeCommand="ShotMaskUi.border_thickness_changed()",
                                               parent=border_form_layout)
        border_top_scale_label = cmds.text("Top Scale  ", align="right", width=93, parent=border_form_layout)
        cls.border_scale_top = cmds.floatField(width=50,
                                               value=1.0,
                                               minValue=0.1,
                                               step=0.01,
                                               precision=2,
                                               changeCommand="ShotMaskUi.border_scale_changed()",
                                               dragCommand="ShotMaskUi.border_scale_changed()",
                                               parent=border_form_layout)
        border_bottom_scale_label = cmds.text("Bottom Scale  ", align="right", width=93, parent=border_form_layout)
        cls.border_scale_bottom = cmds.floatField(width=50,
                                                  value=1.0,
                                                  minValue=0.1,
                                                  step=0.01,
                                                  precision=2,
                                                  changeCommand="ShotMaskUi.border_scale_changed()",
                                                  dragCommand="ShotMaskUi.border_scale_changed()",
                                                  parent=border_form_layout)
        
        border_color = ShotMask.border_color()
        cls.border_color_csg = cmds.colorSliderGrp(label="Color  ",
                                                   columnWidth=(1,90),
                                                   changeCommand="ShotMaskUi.border_color_changed()",
                                                   dragCommand="ShotMaskUi.border_color_changed()",
                                                   parent=border_form_layout)
        cls.border_trans_csg = cmds.colorSliderGrp(label="Transparency  ",
                                                   columnWidth=(1,90),
                                                   changeCommand="ShotMaskUi.border_color_changed()",
                                                   dragCommand="ShotMaskUi.border_color_changed()",
                                                   parent=border_form_layout)
        
        cmds.formLayout(border_form_layout, e=True, af=(cls.border_vis_cbg, "top", 3))
        cmds.formLayout(border_form_layout, e=True, af=(cls.border_vis_cbg, "left", 0))
        cmds.formLayout(border_form_layout, e=True, ac=(border_thickness_label, "top", 4, cls.border_vis_cbg))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_thickness, "top", 0, cls.border_vis_cbg))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_thickness, "left", 0, border_thickness_label))
        
        
        cmds.formLayout(border_form_layout, e=True, ac=(border_top_scale_label, "top", 4, cls.border_thickness))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_scale_top, "top", 0, cls.border_thickness))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_scale_top, "left", 0, border_top_scale_label))
        cmds.formLayout(border_form_layout, e=True, ac=(border_bottom_scale_label, "top", 4, cls.border_scale_top))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_scale_bottom, "top", 0, cls.border_scale_top))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_scale_bottom, "left", 0, border_bottom_scale_label))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_color_csg, "top", 0, cls.border_scale_bottom))
        cmds.formLayout(border_form_layout, e=True, ac=(cls.border_trans_csg, "top", 0, cls.border_color_csg))
        cmds.formLayout(border_form_layout, e=True, af=(cls.border_trans_csg, "bottom", 5))
        
        
        # Buttons
        button_layout = cmds.formLayout(parent=main_layout)
        create_btn = cmds.button(label="Build",
                                 width=80,
                                 command="ShotMaskUi.create_mask()",
                                 parent=button_layout)
        delete_btn = cmds.button(label="Delete",
                                 width=80,
                                 command="ShotMaskUi.delete_mask()",
                                 parent=button_layout)
        cmds.formLayout(button_layout, e=True, af=(delete_btn, "right", 0))
        cmds.formLayout(button_layout, e=True, ac=(create_btn, "right", 0, delete_btn))
        
        cmds.window(main_window, e=True, w=100, h=100)
        cmds.window(main_window, e=True, sizeable=False)
        cmds.window(main_window, e=True, rtf=True)
        
        
        ShotMaskUi.refresh()
        
        cmds.showWindow(main_window)
    
    @classmethod
    def create_label_fields(cls, text_index, parent):
        
        offset = ShotMask.label_offset(text_index)
        text = cmds.textFieldGrp(label=cls.LABELS[text_index],
                                 columnWidth=(1, 90),
                                 changeCommand="ShotMaskUi.label_changed({0})".format(text_index),
                                 parent=parent)
        scale = cmds.floatField(width=50,
                                value=1.0,
                                minValue=0.1,
                                step=0.01,
                                precision=2,
                                dragCommand="ShotMaskUi.label_settings_changed({0})".format(text_index),
                                changeCommand="ShotMaskUi.label_settings_changed({0})".format(text_index),
                                parent=parent)
        offset_x = cmds.floatField(width=50,
                                   value=0.0,
                                   step=0.0001,
                                   precision=4,
                                   dragCommand="ShotMaskUi.label_settings_changed({0})".format(text_index),
                                   changeCommand="ShotMaskUi.label_settings_changed({0})".format(text_index),
                                   parent=parent)
        offset_y = cmds.floatField(width=50,
                                   value=0.0,
                                   step=0.0001,
                                   precision=4,
                                   dragCommand="ShotMaskUi.label_settings_changed({0})".format(text_index),
                                   changeCommand="ShotMaskUi.label_settings_changed({0})".format(text_index),
                                   parent=parent)
        
        
        cls.label_text_ctrls.append(text)
        cls.label_settings_scale_ctrls.append(scale)
        cls.label_settings_offset_x_ctrls.append(offset_x)
        cls.label_settings_offset_y_ctrls.append(offset_y)
    
    @classmethod
    def refresh(cls):
        # Camera Section
        cmds.textFieldGrp(cls.camera_name, e=True, text=ShotMask.camera_name())
        
        # Label Section
        label_text = ShotMask.label_text()
        for i in range(0, len(cls.label_text_ctrls)):
            cmds.textFieldGrp(cls.label_text_ctrls[i], e=True, text=label_text[i])
            offset = ShotMask.label_offset(i)
            cmds.floatField(cls.label_settings_scale_ctrls[i], e=True, value=ShotMask.label_scale(i))
            cmds.floatField(cls.label_settings_offset_x_ctrls[i], e=True, value=offset[0])
            cmds.floatField(cls.label_settings_offset_y_ctrls[i], e=True, value=offset[1])
            
        cmds.textFieldButtonGrp(cls.label_font_tfg, e=True, text=ShotMask.label_font())
        color = ShotMask.label_color()
        cmds.colorSliderGrp(cls.label_color_csg, e=True, rgbValue=(color[0], color[1], color[2]))
        cmds.colorSliderGrp(cls.label_trans_csg, e=True, rgbValue=(color[3], color[3], color[3]))
        
        # Counter Section
        counter_settings = ShotMask.counter_settings()
        cmds.checkBoxGrp(cls.counter_vis_cbg, e=True, value1=counter_settings[1])
        cmds.radioButtonGrp(cls.counter_position, e=True, select=counter_settings[0]+1)
        cmds.intField(cls.counter_padding, e=True, value=counter_settings[5])
        cmds.floatField(cls.counter_scale, e=True, value=counter_settings[2])
        cmds.floatField(cls.counter_offset_x, e=True, value=counter_settings[3])
        cmds.floatField(cls.counter_offset_y, e=True, value=counter_settings[4])
        
        # Border Section
        border_vis = ShotMask.border_visible()
        color = ShotMask.border_color()
        scale = ShotMask.border_scale()
        cmds.checkBoxGrp(cls.border_vis_cbg, e=True, value1=border_vis[0], value2=border_vis[1])
        cmds.floatField(cls.border_thickness, e=True, value=ShotMask.border_thickness())
        cmds.floatField(cls.border_scale_top, e=True, value=scale[0])
        cmds.floatField(cls.border_scale_bottom, e=True, value=scale[1])
        cmds.colorSliderGrp(cls.border_color_csg, e=True, rgbValue=(color[0], color[1], color[2]))
        cmds.colorSliderGrp(cls.border_trans_csg, e=True, rgbValue=(color[3], color[3], color[3]))
        
    @classmethod
    def delete(cls):
        if cmds.window(cls.WINDOW_NAME, exists=True):
            cmds.deleteUI(cls.WINDOW_NAME, window=True)
        
        
    @classmethod
    def create_mask(cls):
        camera = cmds.textFieldGrp(cls.camera_name, q=True, text=True)
        ShotMask.create(camera=camera)
        
    @classmethod
    def delete_mask(cls):
        ShotMask.delete()
        
    @classmethod
    def rebuild_shot_mask(cls):
        if ShotMask.exists():
            camera=ShotMask.last_camera
            ShotMask.create(camera=camera)
        
    @classmethod
    def reset_settings(cls):
        ShotMask.restore_defaults()
        cls.refresh()
        cls.rebuild_shot_mask()
        
    @classmethod
    def label_changed(cls, label_index):
        text = cmds.textFieldGrp(cls.label_text_ctrls[label_index], q=True, text=True)
        ShotMask.set_label_text(label_index, text)
        
        cls.rebuild_shot_mask()
        
    @classmethod
    def label_settings_changed(cls, label_index):
        scale = cmds.floatField(cls.label_settings_scale_ctrls[label_index], q=True, value=True)
        offset_x = cmds.floatField(cls.label_settings_offset_x_ctrls[label_index], q=True, value=True)
        offset_y = cmds.floatField(cls.label_settings_offset_y_ctrls[label_index], q=True, value=True)
        ShotMask.set_label_settings(label_index, scale, offset_x, offset_y)
        
    @classmethod
    def label_color_changed(cls):
        rgb = cmds.colorSliderGrp(cls.label_color_csg, q=True, rgb=True)
        trans = cmds.colorSliderGrp(cls.label_trans_csg, q=True, rgb=True)
        
        ShotMask.set_label_color(rgb[0], rgb[1], rgb[2], trans[0])
        
    @classmethod
    def counter_visibility_changed(cls):
        vis = cmds.checkBoxGrp(cls.counter_vis_cbg, q=True, value1=True)
        
    @classmethod
    def counter_settings_changed(cls, rebuild=False):
        settings = ShotMask.counter_settings()
        settings[0] = cmds.radioButtonGrp(cls.counter_position, q=True, select=True) - 1
        settings[1] = cmds.checkBoxGrp(cls.counter_vis_cbg, q=True, value1=True)
        settings[2] = cmds.floatField(cls.counter_scale, q=True, value=True)
        settings[3] = cmds.floatField(cls.counter_offset_x, q=True, value=True)
        settings[4] = cmds.floatField(cls.counter_offset_y, q=True, value=True)
        settings[5] = cmds.intField(cls.counter_padding, q=True, value=True)
        ShotMask.set_counter_settings(*settings)

        cls.refresh()

        if rebuild:
            cls.rebuild_shot_mask()
        
    @classmethod
    def border_visibility_changed(cls):
        top_vis = cmds.checkBoxGrp(cls.border_vis_cbg, q=True, value1=True)
        bottom_vis = cmds.checkBoxGrp(cls.border_vis_cbg, q=True, value2=True)
        ShotMask.set_border_visible(top_vis, bottom_vis)
        
    @classmethod
    def border_thickness_changed(cls):
        thickness = cmds.floatField(cls.border_thickness, q=True, value=True)
        ShotMask.set_border_thickness(thickness)
        
        cls.rebuild_shot_mask()
        
    @classmethod
    def border_scale_changed(cls):
        ShotMask.set_border_scale(cmds.floatField(cls.border_scale_top, q=True, value=True),
                                  cmds.floatField(cls.border_scale_bottom, q=True, value=True))
        
    @classmethod
    def border_color_changed(cls):
        rgb = cmds.colorSliderGrp(cls.border_color_csg, q=True, rgb=True)
        trans = cmds.colorSliderGrp(cls.border_trans_csg, q=True, rgb=True)
        
        ShotMask.set_border_color(rgb[0], rgb[1], rgb[2], trans[0])
        
    @classmethod
    def camera_changed(cls):
        name = cmds.textFieldGrp(cls.camera_name, q=True, text=True)
        if not name in ShotMask.cameras():
            om.MGlobal.displayWarning("Camera does not exist: {0}".format(name))
        
        ShotMask.set_camera_name(name)
        
        ShotMask.create(name)
        
    @classmethod
    def display_font_dialog(cls):
        font = cmds.fontDialog()
        if font:
            ShotMask.set_label_font(font)
            cls.refresh()
            cls.rebuild_shot_mask()
            
    @classmethod
    def display_camera_dialog(cls):
        result = cmds.layoutDialog(ui="ShotMaskUi.camera_dialog_layout()", 
                                   title="Select Camera",
                                   parent=cls.WINDOW_NAME)
        
        if result not in ["cancel", "dismiss"]:
            cmds.textFieldButtonGrp(cls.camera_name, e=True, text=result)
            cls.camera_changed()
        
    @classmethod
    def camera_dialog_layout(cls):
        cameras = ShotMask.cameras()
        
        layout = cmds.setParent(q=True)
        cmds.formLayout(layout, e=True)
        
        cls.camera_tsl = cmds.textScrollList(numberOfRows=8,
                                             parent=layout)
        for camera in cameras:
            cmds.textScrollList(cls.camera_tsl, 
                                e=True, 
                                append=camera,
                                doubleClickCommand="ShotMaskUi.camera_dialog_ok()")

        current_camera = cmds.textFieldButtonGrp(cls.camera_name, q=True, text=True)
        if current_camera in cameras:
            cmds.textScrollList(cls.camera_tsl, e=True, selectItem=current_camera)
        
        ok_button = cmds.button(label="OK", c="ShotMaskUi.camera_dialog_ok()")
        cancel_button = cmds.button(label="Cancel", c="ShotMaskUi.camera_dialog_cancel()")
        
        cmds.formLayout(layout, e=True, af=(cls.camera_tsl, "top", 0))
        cmds.formLayout(layout, e=True, af=(cls.camera_tsl, "left", 0))
        cmds.formLayout(layout, e=True, af=(cls.camera_tsl, "right", 0))
        
        cmds.formLayout(layout, e=True, ac=(cancel_button, "top", 4, cls.camera_tsl))
        cmds.formLayout(layout, e=True, af=(cancel_button, "right", 0))
        
        cmds.formLayout(layout, e=True, aoc=(ok_button, "top", 0, cancel_button))
        cmds.formLayout(layout, e=True, ac=(ok_button, "right", 0, cancel_button))
    
    @classmethod
    def camera_dialog_ok(cls):
        selection = cmds.textScrollList(cls.camera_tsl, q=True, selectItem=True)
        if not selection:
            camera = ""
        else:
            camera = selection[0]
        cmds.layoutDialog(dismiss=camera)
        
    @classmethod
    def camera_dialog_cancel(cls):
        cmds.layoutDialog(dismiss="cancel")
        
    @classmethod
    def about(cls):
        message = '<h3>Zurbrigg Shot Mask</h3>'
        message += '<p>Version: {0}<br>'.format(ShotMask.VERSION)
        message += 'Author:  Chris Zurbrigg</p>'
        message += '<a style="color:white;" href="http://zurbrigg.com">http://zurbrigg.com</a><br>'
        message += '<p>Copyright &copy; 2014 Chris Zurbrigg</p>'
        
        cmds.confirmDialog(title="About",
                           button="OK",
                           message=message,
                           messageAlign="left",
                           parent=cls.WINDOW_NAME)
        

if __name__ == "__main__":
    ShotMaskUi.display()

