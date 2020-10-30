"""
Ignacio Díaz Lara
Course: Modelación y Computación Gráfica para Ingenieros CC3501, 2020

This is the view for the Monkey Jump Game.
It sets the the conditions to initiate the game, and creates a controller
which create and interacts with the model objects.
"""

import glfw
from OpenGL.GL import *
import sys
import csv
from model import *
from controller import Controller
import random


if __name__ == '__main__':

    # Reading the file with the structure for the game
    stage = {}
    with open('structure.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        stage_count = 1
        stage['stage0'] = ['0', '0', '0']
        for row in csv_reader:
            stage[f'stage{stage_count}'] = row
            stage_count += 1
        stage[f'stage{stage_count}'] = ['0', '0', '0']
        stage[f'stage{stage_count + 1}'] = ['0', '0', '0']
        i = 4

    # Preparing choose of backgrounds
    background_list = [0]

    for i in range(len(stage) - 1):
        background_list += [random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])]

    background_list += [10]

    # Setting a boolean valor to indicate if it's necessary to reset the background (in case of a new game)
    background_reset = False

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 900

    window = glfw.create_window(width, height, 'Monkey Jump', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Creating the controller
    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
    pipeline_texture = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0, 0, 0, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Allowing transparent textures
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating Objects
    controller.create_background()
    controller.create_monkey()
    controller.create_structure()
    controller.set_max_stage(len(stage) - 3)
    controller.set_dictionary(stage)
    controller.create_game_over()
    controller.create_win()

    # Setting useful variables (time related and stage description)
    list_stages = ["0" for i in range(12)]
    stage_num = None

    t0 = glfw.get_time()
    t1 = glfw.get_time()
    ac_t = 0

    while not glfw.window_should_close(window):

        # Setting dt
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = glfw.get_time()

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        if not controller.get_win() and not controller.get_game_over():

            # re-choosing background in case this is a new game
            if background_reset:
                background_list = [0]

                for i in range(len(stage) - 1):
                    background_list += [random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 3, 5, 6, 5, 6])]

                background_list += [10]

                background_reset = False

            # Drawing Background
            stage_num = controller.get_stage()
            controller.draw_background(pipeline_texture, background_list[stage_num], background_list[stage_num +1],
                                       background_list[stage_num + 2], background_list[stage_num + 3])

            # Preparing structure
            if stage_num == 0:
                pass
            else:
                stage_num -= 1

            for i in range(12):
                sublist = stage[f'stage{stage_num + i // 3}']
                list_stages[i] = sublist[i % 3]

            # Drawing models
            controller.draw_structure(pipeline_texture, pipeline_texture, list_stages)
            controller.draw_monkey(pipeline_texture)
            controller.update_monkey(dt)
            controller.check_defeat()
            controller.check_victory()

        elif controller.get_game_over():
            # Defeat case

            # Setting a time variable
            ac_t += dt
            if ac_t > 1:
                ac_t = 0

            # Drawing defeat animation
            controller.draw_game_over(pipeline_texture, ac_t)

            # Indicating a background reset in case of a new game is initiated
            background_reset = True

        elif controller.get_win():
            # Victory case

            # Setting a time variable
            ac_t += dt
            if ac_t > 1:
                ac_t = 0

            # Drawing defeat animation
            controller.draw_win(pipeline_texture, ac_t)

            # Indicating a background reset in case of a new game is initiated
            background_reset = True

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
