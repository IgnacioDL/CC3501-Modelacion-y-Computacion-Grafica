"""
Clase controlador, obtiene el input, lo procesa, y manda los mensajes
a los modelos.
"""

from model import Monkey, Structure
import glfw
import sys


class Controller(object):

    def __init__(self):
        self.monkey = None
        self.structure1 = None
        self.structure2 = None
        self.structure3 = None
        self.structure4 = None
        self.structure5 = None
        self.structure6 = None
        self.structure7 = None
        self.structure8 = None
        self.structure9 = None
        self.structure10 = None
        self.structure11 = None
        self.structure12 = None
        self.stage = 0

    def create_monkey(self):
        self.monkey = Monkey('monkey.png')

    def draw_monkey(self, pipeline):
        self.monkey.draw(pipeline)

    def set_stage(self, n):
        self.stage = n

    def get_stage(self):
        return self.stage

    def create_structure(self):
        self.structure1 = Structure(-2/3, -1)
        self.structure2 = Structure(0, -1)
        self.structure3 = Structure(2/3, -1)
        self.structure4 = Structure(-2/3, -0.5)
        self.structure5 = Structure(0, -0.5)
        self.structure6 = Structure(2/3, -0.5)
        self.structure7 = Structure(-2/3, 0)
        self.structure8 = Structure(0, 0)
        self.structure9 = Structure(2/3, 0)
        self.structure10 = Structure(-2/3, 0.5)
        self.structure11 = Structure(0, 0.5)
        self.structure12 = Structure(2/3, 0.5)

    def draw_structure(self, pipeline, list_stage):
        if list_stage[0] == "1":
            self.structure1.draw(pipeline)
        if list_stage[1] == "1":
            self.structure2.draw(pipeline)
        if list_stage[2] == "1":
            self.structure3.draw(pipeline)
        if list_stage[3] == "1":
            self.structure4.draw(pipeline)
        if list_stage[4] == "1":
            self.structure5.draw(pipeline)
        if list_stage[5] == "1":
            self.structure6.draw(pipeline)
        if list_stage[6] == "1":
            self.structure7.draw(pipeline)
        if list_stage[7] == "1":
            self.structure8.draw(pipeline)
        if list_stage[8] == "1":
            self.structure9.draw(pipeline)
        if list_stage[9] == "1":
            self.structure10.draw(pipeline)
        if list_stage[10] == "1":
            self.structure11.draw(pipeline)
        if list_stage[11] == "1":
            self.structure12.draw(pipeline)

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        # Controlador modifica al modelo
        elif key == glfw.KEY_LEFT and action == glfw.PRESS:
            # print('Move left')
            self.monkey.move_left()

        elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
            # print('Move left')
            self.monkey.move_right()

        # Raton toca la pantalla....
        else:
            print('Unknown key')
