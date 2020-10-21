
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

        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_monkey_texture]

        monkey = sg.SceneGraphNode('monkey')
        monkey.transform = tr.matmul([tr.translate(0, -1 + 0.1 + 0.2, 0), tr.scale(0.4, 0.4, 0)])
        monkey.childs += [body]

        transform_monkey = sg.SceneGraphNode('monkeyTR')
        transform_monkey.childs += [monkey]

        self.model = transform_monkey
        self.pos = 0

    def draw(self, pipeline_texture):
        glUseProgram(pipeline_texture.shaderProgram)
        sg.drawSceneGraphNode(self.model, pipeline_texture, 'transform')

    def move_left(self):
        self.model.transform = tr.translate(-0.7, 0, 0)
        self.pos = -1

    def move_right(self):
        self.model.transform = tr.translate(0.7, 0, 0)
        self.pos = 1

    def move_center(self):
        self.model.transform = tr.translate(0, 0, 0)
        self.pos = 0


class Structure(object):

    def __init__(self, position_x, position_y):
        gpu_structure = es.toGPUShape(bs.createColorQuad(0.8, 0.8, 0.8))

        structure = sg.SceneGraphNode('structure')
        width = 2/3
        long = 0.1
        structure.transform = tr.scale(width, long, 1)
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
        self.pos_y -= 2*dt + (1/2)*(dt**2)
