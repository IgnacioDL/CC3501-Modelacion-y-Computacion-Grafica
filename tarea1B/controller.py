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
        self.max_stage = 0
        self.need_actualize_down = False
        self.need_actualize_up = False
        self.dictionary = None
        self.started = False
        self.game_over = False
        self.win = False

    def get_win(self):
        return self.win

    def get_game_over(self):
        return self.game_over

    def create_monkey(self):
        self.monkey = Monkey('monkey.png', 'monkey_jumping.png', 'monkey_left.png', 'monkey_right.png')

    def draw_monkey(self, pipeline):
        self.monkey.draw(pipeline)

    def update_monkey(self, dt):
        self.monkey.update(dt)
        if self.stage > 0 and self.check_standing():
            self.started = True
        if not self.is_standing():
            self.stage = max(0, self.stage - 1)
            self.monkey.fall()
            if self.stage > 0:
                self.need_actualize_up = True
        if self.need_actualize_down:
            self.actualize_stage_down()
            self.need_actualize_down = False
        elif self.need_actualize_up:
            self.actualize_stage_up()
            self.need_actualize_up = False
        #self.check_defeat()
        #self.check_victory()
        print(self.stage)

    def set_dictionary(self, d):
        self.dictionary = d

    def get_stage(self):
        return self.stage

    def set_max_stage(self, n):
        self.max_stage = n

    def create_structure(self):
        self.structure1 = Structure(-2 / 3, -1)
        self.structure2 = Structure(0, -1)
        self.structure3 = Structure(2 / 3, -1)
        self.structure4 = Structure(-2 / 3, -0.5)
        self.structure5 = Structure(0, -0.5)
        self.structure6 = Structure(2 / 3, -0.5)
        self.structure7 = Structure(-2 / 3, 0)
        self.structure8 = Structure(0, 0)
        self.structure9 = Structure(2 / 3, 0)
        self.structure10 = Structure(-2 / 3, 0.5)
        self.structure11 = Structure(0, 0.5)
        self.structure12 = Structure(2 / 3, 0.5)

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

        elif key == glfw.KEY_LEFT and action == glfw.PRESS:
            self.monkey.move_left()

        elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
            self.monkey.move_right()

        elif key == glfw.KEY_UP and action == glfw.PRESS:
            if self.monkey.get_is_jumping() or self.monkey.get_is_falling() \
                    or self.stage == self.max_stage:
                return
            self.monkey.jump()
            self.stage = min(self.stage + 1, self.max_stage)
            if self.stage > 1:
                self.need_actualize_down = True

        # elif key == glfw.KEY_DOWN and action == glfw.PRESS:
        #     self.monkey.fall()
        #     self.stage = max(0, self.stage - 1)

        # else:
        #    print('Unknown key')

    def actualize_stage_down(self):
        self.monkey.actualize_down()

    def actualize_stage_up(self):
        self.monkey.actualize_up()

    def is_standing(self):
        if self.monkey.get_is_jumping() or self.monkey.get_is_falling() or self.stage == 0:
            return True
        x = self.monkey.get_position_x()
        if self.dictionary[f'stage{self.stage}'][0] == "1":
            if x < -1 + 2 / 3 + 0.05:
                return True
        if self.dictionary[f'stage{self.stage}'][1] == "1":
            if -1 + 2 / 3 < x < 1 / 3:
                return True
        if self.dictionary[f'stage{self.stage}'][2] == "1":
            if x > 1 / 3 - 0.05:
                return True
        return False

    def check_standing(self):
        if not self.monkey.get_is_jumping() and not self.monkey.get_is_falling():
            pos_x = self.monkey.get_position_x()
            if self.stage == 0:
                if self.monkey.get_position_y() == self.monkey.get_position_y_original():
                    return True
            elif self.stage == self.max_stage:
                if self.monkey.get_position_y() == self.monkey.get_aiming_y():
                    return True
            else:
                if self.dictionary[f'stage{self.stage}'][0] == "1":
                    if pos_x < -1 + 2 / 3 + 0.05:
                        return True
                if self.dictionary[f'stage{self.stage}'][1] == "1":
                    if -1 + 2 / 3 < pos_x < 1 / 3:
                        return True
                if self.dictionary[f'stage{self.stage}'][2] == "1":
                    if pos_x > 1 / 3 - 0.05:
                        return True
        return False

    def check_defeat(self):
        if self.started and self.stage == 0 and self.check_standing():
            self.game_over = True

    def check_victory(self):
        if self.stage == self.max_stage and self.check_standing():
            self.win = True
