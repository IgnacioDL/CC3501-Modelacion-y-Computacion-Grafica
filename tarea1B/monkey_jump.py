import glfw
from OpenGL.GL import *
import sys
import csv
from model import *
from controller import Controller


if __name__ == '__main__':

    # Reading the file with the structure for the game
    stage = {}
    with open('structure.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        stage_count = 1
        stage['stage0'] = ['1', '1', '1']
        for row in csv_reader:
            stage[f'stage{stage_count}'] = row
            stage_count += 1
        i = 4
        sublist = stage[f'stage{i // 3}']

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
    controller.create_monkey()
    controller.create_structure()

    # Setting useful variables
    list_stages = ["0" for i in range(12)]

    t0 = glfw.get_time()
    t1 = glfw.get_time()

    while not glfw.window_should_close(window):  # Dibujando --> 1. obtener el input

        # Setting dt
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = glfw.get_time()

        # Preparing structure
        stage_num = controller.get_stage()
        for i in range(12):
            sublist = stage[f'stage{stage_num + i//3}']
            list_stages[i] = sublist[i % 3]

        # Using GLFW to check for input events
        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing models
        controller.draw_structure(pipeline, list_stages)
        controller.draw_monkey(pipeline_texture)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
