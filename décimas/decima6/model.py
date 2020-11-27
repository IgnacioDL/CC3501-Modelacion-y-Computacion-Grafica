"""
Hacemos los modelos
"""

import scene_graph2 as sg
import basic_shapes as bs
import transformations2 as tr
import easy_shaders as es

from OpenGL.GL import *


class Axis(object):

    def __init__(self):
        self.model = es.toGPUShape(bs.createAxis(1))
        self.show = True

    def toggle(self):
        self.show = not self.show

    def draw(self, pipeline, projection, view):
        if not self.show:
            return
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'model'), 1, GL_TRUE, tr.identity())
        pipeline.drawShape(self.model, GL_LINES)


class Tpose(object):

    def __init__(self, texture_head):
        gpu_body = es.toGPUShape(bs.createColorCube(1, 0, 0))
        gpu_leg = es.toGPUShape(bs.createColorCube(0, 0, 1))
        gpu_skin = es.toGPUShape(bs.createColorCube(1, 1, 0))
        gpu_head = es.toGPUShape(bs.createTextureCube(texture_head), GL_REPEAT, GL_LINEAR)

        # Creamos el nucleo
        core = sg.SceneGraphNode('core')
        core.transform = tr.scale(0.32, 0.5, 0.6)
        core.childs += [gpu_body]

        # Piernas
        leg = sg.SceneGraphNode('leg')
        leg.transform = tr.scale(0.14, 0.14, 0.5)
        leg.childs += [gpu_leg]

        leg_left = sg.SceneGraphNode('leg_left')
        leg_left.transform = tr.translate(0, -0.17, -0.5)
        leg_left.childs += [leg]

        leg_right = sg.SceneGraphNode('leg_right')
        leg_right.transform = tr.translate(0, 0.17, -0.5)
        leg_right.childs += [leg]

        # Brazos
        arm = sg.SceneGraphNode('arm')
        arm.transform = tr.scale(0.13, 0.5, 0.13)
        arm.childs += [gpu_skin]

        arm_left = sg.SceneGraphNode('arm_left')
        arm_left.transform = tr.translate(0, -0.4, 0.23)
        arm_left.childs += [arm]

        arm_right = sg.SceneGraphNode('arm_right')
        arm_right.transform = tr.translate(0, 0.4, 0.23)
        arm_right.childs += [arm]

        # Cuello
        neck = sg.SceneGraphNode('neck')
        neck.transform = tr.matmul([tr.scale(0.12, 0.12, 0.2), tr.translate(0, 0, 1.6)])
        neck.childs += [gpu_skin]

        # Cabeza
        head = sg.SceneGraphNode('head')
        head.transform = tr.matmul([tr.scale(0.35, 0.35, 0.35), tr.translate(-0.08, 0, 1.75)])
        head.childs += [gpu_skin]

        body = sg.SceneGraphNode('body')
        body.childs += [arm_left, arm_right, leg_left, leg_right, core, neck, head]

        face = sg.SceneGraphNode('face')
        face.transform = tr.matmul([tr.scale(0.3, 0.3, 0.3), tr.translate(0, 0, 2)])
        face.childs += [gpu_head]

        body_tr = sg.SceneGraphNode('bodyTR')
        body_tr.childs += [body, face]

        self.face = face
        self.body = body

        self.model = body_tr
        self.show_face = True

    def toggle(self):
        self.show_face = not self.show_face

    def draw(self, pipeline_color, pipeline_texture, projection, view):
        # Dibujamos el mono de color con el pipeline_color
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(sg.findNode(self.model, 'body'), pipeline_color)

        # Dibujamos la cara (texturas)
        if self.show_face:
            glUseProgram(pipeline_texture.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, 'projection'), 1, GL_TRUE,
                               projection)
            glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, 'view'), 1, GL_TRUE, view)
            sg.drawSceneGraphNode(sg.findNode(self.model, 'face'), pipeline_texture)

    def move(self, rotation, size, translation1, translation2, translation3):
        self.face.transform = tr.matmul([tr.scale(size, size, size),
                                         tr.translate(translation1, translation2, translation3),
                                         tr.scale(0.3, 0.3, 0.3), tr.translate(0, 0, 2),
                                         tr.rotationZ(rotation)])
        self.body.transform = tr.matmul([tr.scale(size, size, size),
                                         tr.translate(translation1, translation2, translation3),
                                         tr.rotationZ(rotation)])

