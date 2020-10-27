import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

from OpenGL.GL import *


class Monkey(object):

    def __init__(self, texture_monkey, texture_monkey_jumping, texture_monkey_left, texture_monkey_right):
        gpu_monkey_texture = es.toGPUShape(bs.createTextureCube(texture_monkey), GL_REPEAT, GL_LINEAR)
        gpu_monkey_texture_jumping = es.toGPUShape(bs.createTextureCube(texture_monkey_jumping), GL_REPEAT, GL_LINEAR)
        gpu_monkey_texture_left = es.toGPUShape(bs.createTextureCube(texture_monkey_left), GL_REPEAT, GL_LINEAR)
        gpu_monkey_texture_right = es.toGPUShape(bs.createTextureCube(texture_monkey_right), GL_REPEAT, GL_LINEAR)

        # Saving textures
        self.gpu_texture_monkey = gpu_monkey_texture
        self.gpu_texture_jumping = gpu_monkey_texture_jumping
        self.gpu_texture_left = gpu_monkey_texture_left
        self.gpu_texture_right = gpu_monkey_texture_right

        # Setting positions
        self.position_x = 0
        self.position_y = -1 + 0.1 + 0.2
        self.position_y_original = self.position_y
        self.position_x_original = self.position_x

        # Setting Graph
        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_monkey_texture]

        monkey = sg.SceneGraphNode('monkey')
        monkey.transform = tr.matmul([tr.translate(self.position_x, self.position_y, 0),
                                      tr.scale(0.4, 0.4, 0)])
        monkey.childs += [body]

        transform_monkey = sg.SceneGraphNode('monkeyTR')
        transform_monkey.childs += [monkey]

        # Setting other useful variables
        self.model = transform_monkey
        self.aiming_x = self.position_x
        self.aiming_y = self.position_y
        self.is_falling = False
        self.is_jumping = False

    def restart(self, ):
        self.position_x = self.position_x_original
        self.aiming_x = self.position_x
        self.position_y = self.position_y_original
        self.aiming_y = self.position_y
        self.is_falling = False
        self.is_jumping = False

    def get_position_x_original(self):
        return self.position_x_original

    def get_position_y_original(self):
        return self.position_y_original

    def get_position_y(self):
        return self.position_y

    def get_aiming_y(self):
        return self.aiming_y

    def get_is_falling(self):
        return self.is_falling

    def get_is_jumping(self):
        return self.is_jumping

    def get_position_x(self):
        return self.position_x

    def draw(self, pipeline_texture):
        monkey_body = sg.findNode(self.model, "body")

        if self.is_jumping or self.is_falling:
            monkey_body.childs = [self.gpu_texture_jumping]
        elif self.position_x > self.aiming_x:
            monkey_body.childs = [self.gpu_texture_left]
        elif self.position_x < self.aiming_x:
            monkey_body.childs = [self.gpu_texture_right]
        else:
            monkey_body.childs = [self.gpu_texture_monkey]

        glUseProgram(pipeline_texture.shaderProgram)
        sg.drawSceneGraphNode(self.model, pipeline_texture, 'transform')

    def move_left(self):
        self.aiming_x -= 0.25
        self.aiming_x = max(self.aiming_x, -0.8)

    def move_right(self):
        self.aiming_x += 0.25
        self.aiming_x = min(self.aiming_x, 0.8)

    def jump(self):
        if not self.is_jumping and not self.is_falling:
            self.is_jumping = True
            self.aiming_y += 0.5
            self.aiming_y = min(0.5 + 0.1 + 0.2, self.aiming_y)

    def fall(self):
        if not self.is_jumping and not self.is_falling:
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

        # Transforming model
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

    def __init__(self, texture, position_x, position_y):
        # gpu_structure = es.toGPUShape(bs.createColorQuad(0.8, 0.8, 0.8))
        gpu_structure = es.toGPUShape(bs.createTextureCube(texture), GL_REPEAT, GL_LINEAR)

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


class EndGame(object):
    def __init__(self, texture_1, texture_2, texture_3, texture_4, texture_5):
        gpu_end_game_1 = es.toGPUShape(bs.createTextureCube(texture_1), GL_REPEAT, GL_LINEAR)
        gpu_end_game_2 = es.toGPUShape(bs.createTextureCube(texture_2), GL_REPEAT, GL_LINEAR)
        gpu_end_game_3 = es.toGPUShape(bs.createTextureCube(texture_3), GL_REPEAT, GL_LINEAR)
        gpu_end_game_4 = es.toGPUShape(bs.createTextureCube(texture_4), GL_REPEAT, GL_LINEAR)
        gpu_end_game_5 = es.toGPUShape(bs.createTextureCube(texture_5), GL_REPEAT, GL_LINEAR)

        # Saving textures
        self.texture_1 = gpu_end_game_1
        self.texture_2 = gpu_end_game_2
        self.texture_3 = gpu_end_game_3
        self.texture_4 = gpu_end_game_4
        self.texture_5 = gpu_end_game_5

        # Setting Graph
        scene = sg.SceneGraphNode('scene')
        scene.transform = tr.uniformScale(2)
        scene.childs += [gpu_end_game_1]

        total_scene = sg.SceneGraphNode('total_scene')
        total_scene.childs += [scene]

        self.model = total_scene

    def draw(self, pipeline_texture, t):
        scene = sg.findNode(self.model, "scene")
        if t < 0.2:
            scene.childs = [self.texture_1]
        elif 0.4 >= t >= 0.2:
            scene.childs = [self.texture_2]
        elif 0.6 >= t >= 0.4:
            scene.childs = [self.texture_3]
        elif 0.8 >= t >= 0.6:
            scene.childs = [self.texture_4]
        else:
            scene.childs = [self.texture_5]
        glUseProgram(pipeline_texture.shaderProgram)
        sg.drawSceneGraphNode(self.model, pipeline_texture, 'transform')


class Banana(object):

    def __init__(self, texture, position_x, position_y):
        gpu_banana = es.toGPUShape(bs.createTextureCube(texture), GL_REPEAT, GL_LINEAR)

        banana = sg.SceneGraphNode('banana')
        width = 2 / 3
        length = 0.3
        banana.transform = tr.scale(width, length, 1)
        banana.childs += [gpu_banana]

        banana_tr = sg.SceneGraphNode('bananaTR')
        banana_tr.childs += [banana]

        self.pos_y = position_y + 0.05 + 0.17  # -1, -0.5, 0, 0.5 / + 0.5 +0.1
        self.pos_x = position_x  # -2/3, 0, 2/3
        self.model = banana_tr

    def draw(self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")