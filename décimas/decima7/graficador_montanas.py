# coding=utf-8
"""
Graficador, genera una superficie 3D que representa una función.

@author ppizarror


Modificado por Ignacio Díaz para décima 7 de Modelación y Computación Gráfica.
"""

# Library imports
import glfw
from OpenGL.GL import *
import sys
import numpy as np
import random

import transformations2 as tr2
import easy_shaders as es
import camera as cam
from mathlib import Point3
import basic_shapes_extended as bs_ext
from colors import colorHSV
from model import Axis



# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()

# Create camera
camera = cam.CameraR(r=3.5, center=Point3())
camera.set_r_vel(0.1)


# noinspection PyUnusedLocal
def on_key(window_obj, key, scancode, action, mods):
    global controller

    if action == glfw.REPEAT or action == glfw.PRESS:
        # Move the camera position
        if key == glfw.KEY_LEFT:
            camera.rotate_phi(-4)
        elif key == glfw.KEY_RIGHT:
            camera.rotate_phi(4)
        elif key == glfw.KEY_UP:
            camera.rotate_theta(-4)
        elif key == glfw.KEY_DOWN:
            camera.rotate_theta(4)
        elif key == glfw.KEY_A:
            camera.close()
        elif key == glfw.KEY_D:
            camera.far()

        # Move the center of the camera
        elif key == glfw.KEY_I:
            camera.move_center_x(-0.05)
        elif key == glfw.KEY_K:
            camera.move_center_x(0.05)
        elif key == glfw.KEY_J:
            camera.move_center_y(-0.05)
        elif key == glfw.KEY_L:
            camera.move_center_y(0.05)
        elif key == glfw.KEY_U:
            camera.move_center_z(-0.05)
        elif key == glfw.KEY_O:
            camera.move_center_z(0.05)

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, 'Graficador EPIC', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create models
    obj_axis = Axis()

    # Create the grid of the system
    vertex_grid = []
    width = 33  # should be expressable as n^2+1
    height = 33  # should be expressable as n^2+1
    zlim = [0, 0]

    # Create matrix of z values
    zValues = np.zeros((width, height))

    # Initialize the four corners with a pre-seeded value
    zValues[0][0] = 0.2
    zValues[width-1][0] = 0.1
    zValues[0][height-1] = 0.1
    zValues[width-1][height-1] = 0.2

    lower = 100  # -0.1
    upper = 300  # 0.1
    stepSize = width - 1

    while stepSize > 1:
        halfStep = int(np.floor(stepSize / 2))

        # Diamond step
        for x in range(0, width - 1, stepSize):
            for y in range(0, height - 1, stepSize):
                topLeft = zValues[x][y]
                topRight = zValues[x + stepSize][y]
                botLeft = zValues[x][y + stepSize]
                botRight = zValues[x + stepSize][y + stepSize]

                avg = (topLeft + topRight + botLeft + botRight) / 4
                rand = (random.randrange(lower, upper) / 1000) - 0.2
                zValues[x + halfStep][y + halfStep] = avg + rand

        # Square step
        even = True

        for x in range(0, width - 1, halfStep):
            xStart = 0
            if not even:
                xStart = halfStep
            for y in range(xStart, height - 1, halfStep):
                left = 0
                if not (x - halfStep < 0):
                    left = zValues[x - halfStep][y]
                right = 0
                if not (x + halfStep >= width):
                    right = zValues[x - halfStep][y]
                up = zValues[x][y + halfStep]
                down = zValues[x][y - halfStep]

                avg = (left + right + up + down) / 4
                rand = (random.randrange(lower, upper) / 1000) - 0.2
                zValues[x][y] = avg + rand
            even = not even

        stepSize = int(stepSize/2)
        lower += 10  # 0.009
        upper -= 10  # 0.009

    lower = 100  # -0.1
    upper = 300  # 0.1
    stepSize = width - 1

    # Readjusting corners values
    zValues[0][0] = 0.
    zValues[width - 1][0] = 0
    zValues[0][height - 1] = 0
    zValues[width - 1][height - 1] = 0

    # Filling the grid of the system
    for i in range(width):  # x
        for j in range(height):  # y
            xp = -1 + 2 / (width - 1) * j
            yp = -1 + 2 / (height - 1) * i
            zp = zValues[i][j]
            zlim = [min(zp, zlim[0]), max(zp, zlim[1])]
            vertex_grid.append([xp, yp, zp])

    # Calculate the difference between max and min zvalue
    dz = abs(zlim[1] - zlim[0])
    zmean = (zlim[1] + zlim[0]) / 2
    dzf = min(1.0, 1 / (dz + 0.001))  # Height factor

    # Multiply all values for a factor, so the maximum height will be 1
    # Also the plot is centered
    for i in range(len(vertex_grid)):
        vertex_grid[i][2] = (vertex_grid[i][2] - zmean) * dzf
        zlim = [min(vertex_grid[i][2], zlim[0]), max(vertex_grid[i][2], zlim[1])]
    dz = abs(zlim[1] - zlim[0])

    # Force the color
    color_plot = {
        'enabled': False,
        'color': [1, 1, 1]
    }

    # Create the quads
    quad_shapes = []
    for i in range(width - 1):  # x
        for j in range(height - 1):  # y
            # Select positions
            a = i * height + j
            b = a + 1
            c = (i + 1) * height + j + 1
            d = c - 1

            # Select vertices
            pa = vertex_grid[a]
            pb = vertex_grid[b]
            pc = vertex_grid[c]
            pd = vertex_grid[d]

            # Calculate color from interpolation
            zval = (pa[2] + pb[2] + pc[2] + pd[2]) / 4  # Average height of quad
            zf = (zval - zlim[0]) / (dz + 0.001)
            if not color_plot['enabled']:
                color = colorHSV(1 - zf)
            else:
                color = color_plot['color']

            # Create the figure
            quad_shapes.append(es.toGPUShape(bs_ext.create4VertexColor(pa, pb, pc, pd,
                                                                       color[0], color[1], color[2])))

    # Create main object
    obj_main = bs_ext.AdvancedGPUShape(quad_shapes, shader=colorShaderProgram)

    # Create projection
    # projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
    projection = tr2.perspective(60, float(width) / float(height), 0.1, 10)

    # Main loop
    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Get camera view matrix
        view = camera.get_view()

        # Draw objects
        obj_axis.draw(colorShaderProgram, projection, view)
        obj_main.draw(view, projection)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)

    glfw.terminate()
