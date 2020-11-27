#Ignacio Díaz Lara



import glfw  # Usada para interactuar con un usuario (mouse, teclado, etc)
from OpenGL.GL import *  # importa las funciones de OpenGL
import OpenGL.GL.shaders  # importa el set de shaders de OpenGL.
import numpy as np
import sys  # para hacer handling de eventos, como entradas del sistema,


# o cerrar el programa.

# A class to store the application control
class Controller:
    fillPolygon = True
    shader_to_use = 0


# We will use the global controller as communication with the callback function
controller = Controller()  # Here we declare this as a global variable.


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller  # Declares that we are going to use the global object controller inside this function.

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
        print("Toggle GL_FILL/GL_LINE")

    elif key == glfw.KEY_ENTER:
        # Usamos % 3 para que nunca supere el 3. Será 0, 1 ó 2. Cuando llegue a 3 o algo superior, se volverá a mover a
        # entre 0, 1 ó 2. Compruébelo!
        controller.shader_to_use = (controller.shader_to_use + 1) % 3
        print("Toggle shader program")
        print("Toggle shader program")

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


# A simple class container to reference a shape on GPU memory
class GPUShape:
    def __init__(self):
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.texture = 0
        self.size = 0


def drawShape(shaderProgram, shape):
    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # Setting up the location of the attributes position and color from the VBO
    # A vertex attribute has 3 integers for the position (each is 4 bytes),
    # and 3 numbers to represent the color (each is 4 bytes),
    # Henceforth, we have 3*4 + 3*4 = 24 bytes
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # Render the active element buffer with the active shader program
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


def createRedTriangle():

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
    #   positions        colors
         -0.8, 0.0, 0.0,  1.0, 0.0, 0.0,  # v0 vertex with index 0
         0.0, -0.8, 0.0,  1.0, 0.0, 0.0,  # v1 vertex with index 1
         0.0,  0.8, 0.0,  1.0, 0.0, 0.0]  # v2 vertex with index 2
    # It is important to use 32 bits data
         , dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

    return gpuShape

def createGreenTriangle():

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
    #   positions        colors
        0.6, 0.4, 0.0, 0.0, 1.0, 0.0,  # v0 vertex with index 0
        0.0, -0.8, 0.0, 0.0, 1.0, 0.0,  # v1 vertex with index 1
        0.0, 0.8, 0.0, 0.0, 1.0, 0.0]  # v2 vertex with index 2
    # It is important to use 32 bits data
         , dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

    return gpuShape

def createCircle(N):
    # Here the new shape will be stored
    gpuShape = GPUShape()
    SIZE_IN_BYTES = 4

    # First vertex at the center, white color
    vertices = [0, 0, 0, 1.0, 1.0, 1.0]
    indices = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.8 * np.cos(theta), 0.8 * np.sin(theta), 0,

            # color generates varying between 0 and 1
            1, 1, 1]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i + 1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * SIZE_IN_BYTES, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * SIZE_IN_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, "Window name", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    void main()
    {
        fragColor = color;
        gl_Position = vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


# Creating shapes on GPU memory
gpuCircle = createCircle(100)
gpuTriangle1 = createRedTriangle()
gpuTriangle2 = createGreenTriangle()

while not glfw.window_should_close(window):
    # Using GLFW to check for input events
    glfw.poll_events()

    # Filling or not the shapes depending on the controller state
    if (controller.fillPolygon):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Clearing the screen in both, color and depth
    glClear(GL_COLOR_BUFFER_BIT)

    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)
    # Telling OpenGL to draw our shapes using the previous shader program.
    drawShape(shaderProgram, gpuCircle)
    drawShape(shaderProgram, gpuTriangle1)
    drawShape(shaderProgram, gpuTriangle2)


    # Once the render is done, buffers are swapped, showing only the complete scene.
    glfw.swap_buffers(window)

glfw.terminate()