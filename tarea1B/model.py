import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

from OpenGL.GL import *
import random
from typing import List


class Monkey(object):

    def __init__(self, texture_monkey):
        # gpu_body_quad = es.toGPUShape(bs.createColorQuad(1, 0.8, 0.8))
        gpu_monkey_texture = es.toGPUShape(bs.createTextureCube(texture_monkey), GL_REPEAT, GL_LINEAR)

        self.position_x = 0
        self.position_y = -1 + 0.1 + 0.2
        self.position_y_original = self.position_y

        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_monkey_texture]

        monkey = sg.SceneGraphNode('monkey')
        monkey.transform = tr.matmul([tr.translate(self.position_x, self.position_y, 0),
                                      tr.scale(0.4, 0.4, 0)])
        monkey.childs += [body]

        transform_monkey = sg.SceneGraphNode('monkeyTR')
        transform_monkey.childs += [monkey]

        self.model = transform_monkey
        self.aiming_x = self.position_x
        self.aiming_y = self.position_y
        self.is_falling = False
        self.is_jumping = False
        self.stage = 0

    def set_is_falling(self):
        self.is_falling = True

    def set_is_jumping(self):
        if self.position_y == self.aiming_y:
            self.is_jumping = True

    def get_is_falling(self):
        return self.is_falling

    def get_is_jumping(self):
        return self.is_jumping

    def get_position_x(self):
        return self.position_x

    def draw(self, pipeline_texture):
        glUseProgram(pipeline_texture.shaderProgram)
        sg.drawSceneGraphNode(self.model, pipeline_texture, 'transform')

    def move_left(self):
        self.aiming_x -= 0.25
        self.aiming_x = max(self.aiming_x, -0.8)

    def move_right(self):
        self.aiming_x += 0.25
        self.aiming_x = min(self.aiming_x, 0.8)

    def jump(self):
        if self.is_jumping == False and self.is_falling == False:
            self.is_jumping = True
            self.aiming_y += 0.5
            self.aiming_y = min(0.5 + 0.1 + 0.2, self.aiming_y)

    def fall(self):
        if self.is_jumping == False and self.is_falling == False:
            self.is_falling = True
            self.aiming_y -= 0.5
            self.aiming_y = max(-1 + 0.1 + 0.2, self.aiming_y)

    def update(self, dt):

        dx = 1 * dt + (1 / 2) * (dt ** 2)
        dy = 0.8 * dt + 2 * (dt ** 2)

        # Actualizing position in x
        if abs(self.position_x - self.aiming_x) < 0.01:
            self.position_x = self.aiming_x
        elif self.aiming_x > self.position_x:
            self.position_x += dx
            self.position_x = min(0.8, self.position_x)
        elif self.aiming_x < self.position_x:
            self.position_x -= dx
            self.position_x = max(-0.8, self.position_x)

        # Actualizing position in y
        # if self.position_y > 0 and self.aiming_y > 0 and self.aiming_y - self.position_y < 0.0001:
        #    self.position_y = self.aiming_y
        # elif self.position_y < 0 and self.aiming_y - self.position_y < 0.0001:
        #    self.position_y = self.aiming_y
        # elif self.aiming_y > self.position_y:
        #    self.position_y += dy
        #    self.position_y = min(0.8, self.position_y)
        if abs(self.position_y - self.aiming_y) < 0.01:
            self.position_y = self.aiming_y
            self.is_jumping = False
            self.is_falling = False
        elif self.aiming_y > self.position_y:
            self.position_y += dy
            self.position_y = min(0.8, self.position_y)
        elif self.aiming_y < self.position_y:
            self.position_y -= dy
            self.position_y = max(-0.8, self.position_y)
        self.model.transform = tr.translate(self.position_x, self.position_y - self.position_y_original, 0)

    def actualize_down(self):
        self.position_y -= 0.5
        self.aiming_y -= 0.5
        self.model.transform = tr.translate(self.position_x, self.position_y, 0)

    def actualize_up(self):
        self.position_y += 0.5
        self.aiming_y += 0.5
        self.model.transform = tr.translate(self.position_x, self.position_y, 0)


class Structure(object):

    def __init__(self, position_x, position_y):
        gpu_structure = es.toGPUShape(bs.createColorQuad(0.8, 0.8, 0.8))

        structure = sg.SceneGraphNode('structure')
        width = 2 / 3
        length = 0.1
        structure.transform = tr.scale(width, length, 1)
        structure.childs += [gpu_structure]

        structure_tr = sg.SceneGraphNode('structureTR')
        structure_tr.childs += [structure]

        self.pos_y = position_y + 0.05  # -1, -0.5, 0, 0.5
        self.pos_x = position_x  # -2/3, 0, 2/3
        self.model = structure_tr

    def draw(self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        # y_0 = 0
        # v_0 = 2
        # a = 1
        self.pos_y -= 2 * dt + (1 / 2) * (dt ** 2)
