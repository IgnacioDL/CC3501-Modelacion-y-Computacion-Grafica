"""
Ignacio Díaz Lara
Course: Modelación y Computación Gráfica para Ingenieros CC3501, 2020

This is the controller for the Monkey Jump Game.
It creates the objects from the model and interact with them when necessary.
It also checks victory or defeat conditions.
"""

from model import Monkey, Structure, EndGame, Banana, Background
import glfw
import sys


class Controller(object):
    """
    Class Controller
    It creates objects for the model and interact with them.
    """

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
        self.banana1 = None
        self.banana2 = None
        self.banana3 = None
        self.banana4 = None
        self.banana5 = None
        self.banana6 = None
        self.banana7 = None
        self.banana8 = None
        self.banana9 = None
        self.background1 = None
        self.background2 = None
        self.background3 = None
        self.background4 = None
        self.stage = 0
        self.max_stage = 0
        self.need_actualize_down = False
        self.need_actualize_up = False
        self.dictionary = None
        self.started = False
        self.game_over = False
        self.win = False
        self.scene_end_game = None
        self.scene_win = None

    def set_dictionary(self, d):
        # Sets the a given dictionary with the structure information
        self.dictionary = d

    def set_max_stage(self, n):
        # Sets the max stage allowed
        self.max_stage = n

    def get_stage(self):
        # Returns the actual stage
        return self.stage

    def get_win(self):
        # Returns the state of victory
        return self.win

    def get_game_over(self):
        # Returns the state of defeat
        return self.game_over

    def create_monkey(self):
        # Creates the monkey model object for the game
        self.monkey = Monkey('img/monkey.png', 'img/monkey_jumping.png', 'img/monkey_left.png', 'img/monkey_right.png')

    def create_game_over(self):
        # Creates the defeat animation model object for the game
        self.scene_end_game = EndGame('img/game_over_0.png', 'img/game_over_1.png',  'img/game_over_2.png',
                                      'img/game_over_3.png', 'img/game_over_4.png')

    def create_win(self):
        # Creates the victory animation model object for the game
        self.scene_win = EndGame('img/win_0.png', 'img/win_1.png', 'img/win_2.png', 'img/win_3.png', 'img/win_4.png')

    def create_background(self):
        # Creates the background model object for the game
        self.background1 = Background('img/background_0.png', 'img/background_1.png', 'img/background_2.png',
                                      'img/background_3.png', 'img/background_4.png', 'img/background_5.png',
                                      'img/background_6.png', 'img/background_7.png', 'img/background_8.png',
                                      'img/background_9.png', 'img/background_top.png', 0, -1)
        self.background2 = Background('img/background_0.png', 'img/background_1.png', 'img/background_2.png',
                                      'img/background_3.png', 'img/background_4.png', 'img/background_5.png',
                                      'img/background_6.png', 'img/background_7.png', 'img/background_8.png',
                                      'img/background_9.png', 'img/background_top.png', 0, -0.5)
        self.background3 = Background('img/background_0.png', 'img/background_1.png', 'img/background_2.png',
                                      'img/background_3.png', 'img/background_4.png', 'img/background_5.png',
                                      'img/background_6.png', 'img/background_7.png', 'img/background_8.png',
                                      'img/background_9.png', 'img/background_top.png', 0, 0)
        self.background4 = Background('img/background_0.png', 'img/background_1.png', 'img/background_2.png',
                                      'img/background_3.png', 'img/background_4.png', 'img/background_5.png',
                                      'img/background_6.png', 'img/background_7.png', 'img/background_8.png',
                                      'img/background_9.png', 'img/background_top.png', 0, 0.5)

    def create_structure(self):
        # Creates the structure model object for the game. And it includes banana model when needed
        self.structure1 = Structure('img/structure.png', -2 / 3, -1)
        self.structure2 = Structure('img/structure.png', 0, -1)
        self.structure3 = Structure('img/structure.png', 2 / 3, -1)
        self.structure4 = Structure('img/structure.png', -2 / 3, -0.5)
        self.structure5 = Structure('img/structure.png', 0, -0.5)
        self.structure6 = Structure('img/structure.png', 2 / 3, -0.5)
        self.structure7 = Structure('img/structure.png', -2 / 3, 0)
        self.structure8 = Structure('img/structure.png', 0, 0)
        self.structure9 = Structure('img/structure.png', 2 / 3, 0)
        self.structure10 = Structure('img/structure.png', -2 / 3, 0.5)
        self.structure11 = Structure('img/structure.png', 0, 0.5)
        self.structure12 = Structure('img/structure.png', 2 / 3, 0.5)
        self.banana1 = Banana('img/banana.png', -2 / 3, -0.5)
        self.banana2 = Banana('img/banana.png', 0, -0.5)
        self.banana3 = Banana('img/banana.png', 2 / 3, -0.5)
        self.banana4 = Banana('img/banana.png', -2 / 3, 0)
        self.banana5 = Banana('img/banana.png', 0, 0)
        self.banana6 = Banana('img/banana.png', 2 / 3, 0)
        self.banana7 = Banana('img/banana.png', -2 / 3, 0.5)
        self.banana8 = Banana('img/banana.png', 0, 0.5)
        self.banana9 = Banana('img/banana.png', 2 / 3, 0.5)

    def draw_monkey(self, pipeline):
        # Draws the monkey model with a given pipeline
        self.monkey.draw(pipeline)

    def draw_game_over(self, pipeline, t):
        # Draws the defeat model with a given pipeline and time variable
        self.scene_end_game.draw(pipeline, t)

    def draw_win(self, pipeline, t):
        # Draws the victory model with a given pipeline and time variable
        self.scene_win.draw(pipeline, t)

    def draw_background(self, pipeline, n1, n2, n3, n4):
        # Draws the background model with a given pipeline and stage related variable
        self.background1.draw(pipeline, n1)
        self.background2.draw(pipeline, n2)
        self.background3.draw(pipeline, n3)
        self.background4.draw(pipeline, n4)

    def draw_structure(self, pipeline_structure, pipeline_banana, list_stage):
        # Draws the structure model with a given pipeline and stage related variable.
        # It also draws banana model when needed
        if list_stage[0] == "1":
            self.structure1.draw(pipeline_structure)
        if list_stage[1] == "1":
            self.structure2.draw(pipeline_structure)
        if list_stage[2] == "1":
            self.structure3.draw(pipeline_structure)
        if list_stage[3] == "1":
            self.structure4.draw(pipeline_structure)
            if self.stage == self.max_stage:
                self.banana1.draw(pipeline_banana)
        if list_stage[4] == "1":
            self.structure5.draw(pipeline_structure)
            if self.stage == self.max_stage:
                self.banana2.draw(pipeline_banana)
        if list_stage[5] == "1":
            self.structure6.draw(pipeline_structure)
            if self.stage == self.max_stage:
                self.banana3.draw(pipeline_banana)
        if list_stage[6] == "1":
            self.structure7.draw(pipeline_structure)
            if self.stage == self.max_stage - 1:
                self.banana4.draw(pipeline_banana)
        if list_stage[7] == "1":
            self.structure8.draw(pipeline_structure)
            if self.stage == self.max_stage - 1:
                self.banana5.draw(pipeline_banana)
        if list_stage[8] == "1":
            self.structure9.draw(pipeline_structure)
            if self.stage == self.max_stage - 1:
                self.banana6.draw(pipeline_banana)
        if list_stage[9] == "1":
            self.structure10.draw(pipeline_structure)
            if self.stage == self.max_stage - 2:
                self.banana7.draw(pipeline_banana)
        if list_stage[10] == "1":
            self.structure11.draw(pipeline_structure)
            if self.stage == self.max_stage - 2:
                self.banana8.draw(pipeline_banana)
        if list_stage[11] == "1":
            self.structure12.draw(pipeline_structure)
            if self.stage == self.max_stage - 2:
                self.banana9.draw(pipeline_banana)

    def update_monkey(self, dt):
        # Updates monkey and checks stage related conditions and monkey position related conditions
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

    def actualize_stage_down(self):
        # Actualize scenery conditions in order to move things down
        self.monkey.actualize_down()

    def actualize_stage_up(self):
        # Actualize scenery conditions in order to move things up
        self.monkey.actualize_up()

    def is_standing(self):
        # Checks if the monkey is standing in the structure
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
        # Checks if the monkey is standing in the structure but for winning or losing purpose
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
        # Checks if defeat conditions are met
        if self.started and self.stage == 0 and self.check_standing():
            self.game_over = True

    def check_victory(self):
        # Checks if victory conditions are met
        if self.stage == self.max_stage and self.check_standing():
            self.win = True


    def on_key(self, window, key, scancode, action, mods):
        # Checks what keys are pressed for the user (and how), proceeding to different actions
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            # No key is pressed
            return

        if key == glfw.KEY_A and action == glfw.PRESS:
            # moving monkey to the left
            self.monkey.move_left()

        elif key == glfw.KEY_D and action == glfw.PRESS:
            # moving monkey to the right
            self.monkey.move_right()

        elif key == glfw.KEY_W and action == glfw.PRESS:
            # making monkey to jump if possible
            if self.monkey.get_is_jumping() or self.monkey.get_is_falling() \
                    or self.stage == self.max_stage:
                return
            self.monkey.jump()
            self.stage = min(self.stage + 1, self.max_stage)
            if self.stage > 1:
                self.need_actualize_down = True

        elif key == glfw.KEY_KP_ENTER and action == glfw.PRESS:
            # In case of victory or defeat animation is already showing, this key starts a new game
            if self.game_over or self.win:
                self.monkey.restart()
                self.stage = 0
                self.game_over = False
                self.win = False
                self.need_actualize_down = False
                self.need_actualize_up = False
                self.started = False
