"""
Contralor de la aplicación.
"""

import glfw
import sys


class Controller(object):

    def __init__(self):
        self.fill_polygon = True
        self.toggle = {}

    def set_toggle(self, tp, key):
        self.toggle[key] = tp

    def on_key(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return

        if key == glfw.KEY_SPACE:
            self.fill_polygon = not self.fill_polygon

        elif key == glfw.KEY_F:
            self.toggle['face'].toggle()

        elif key == glfw.KEY_A:
            self.toggle['axis'].toggle()

        elif key == glfw.KEY_LEFT:
            self.toggle['face'].face_changer_left()

        elif key == glfw.KEY_RIGHT:
            self.toggle['face'].face_changer_right()

        elif key == glfw.KEY_E:
            self.toggle['face'].expand_arm()

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        else:
            print('Unknown key')
