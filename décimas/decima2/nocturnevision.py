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
    shader_to_use = 2


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


## P4: Le agregamos una coordenada y a los vértices inferiores, para poder calibrar esta posición.
def createSky(y, b):
    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions  colors
        -1, +y, 0, 1, 1, b,
        1, +y, 0, 1, 1, b,
        1, 1, 0, 0.5, 0.5, b,
        -1, 1, 0, 0.5, 0.5, b
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype=np.uint32)

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


## P5: Entregamos posición y. Fijarse en los índices, cómo definimos que se unen los vértices
def createDunes(y):
    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions    colors
        -1, y, 0, 160 / 255.0, 134 / 255.0, 73 / 255.0,  # v0
        1, y, 0, 168 / 255.0, 121 / 255.0, 11 / 255.0,  # v1
        1, 0, 0, 244 / 255.0, 223 / 255.0, 66 / 255.0,  # v2
        -1, 0, 0, 1, 207 / 255.0, 96 / 255.0  # v3
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(  # definimos cómo se unen los vértices
        [0, 1, 2,
         2, 3, 0], dtype=np.uint32)

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


# P6: Notar que generamos dos triángulos. Ambos se juntan en el vértice superior, pero se definen como distintos vértices
# porque tienen distinto color. Un lado será más oscuro (que no da al sol).
def createPiramid():
    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions        colors
        -0.3, -0.2, 0.0, 1, 207 / 255.0, 96 / 255.0,  # v0
        0.7, -0.2, 0.0, 168 / 255.0, 121 / 255.0, 11 / 255.0,  # v1
        0.2, 0.7, 0.0, 229 / 255.0, 214 / 255.0, 142 / 255.0,  # v2

        0.7, -0.2, 0.0, 122 / 255.0, 89 / 255.0, 13 / 255.0,  # v3
        0.2, 0.7, 0.0, 122 / 255.0, 89 / 255.0, 13 / 255.0,  # v4
        0.9, -0.1, 0.0, 122 / 255.0, 89 / 255.0, 13 / 255.0  # v5
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         3, 4, 5], dtype=np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

    return gpuShape


if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1080
    height = 720

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

    vertex_shader2 = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    void main()
    {
        fragColor = color;
        gl_Position = vec4(2 * position, 1.0f);
    }
    """

    fragment_shader2 = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        float meanColor = (fragColor.r + fragColor.g + fragColor.b) / 3;
        outColor = vec4(meanColor, meanColor, meanColor,  1.0f);
    }
    """

    fragment_shader_night = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor.r * 0.2, fragColor.g * 0.2, (fragColor.b + 0.2) * 0.5, 1.0f);
    }
    """

    fragment_shader_nocturne_vision = """
        #version 130

        in vec3 fragColor;
        out vec4 outColor;

        void main()
        {
            outColor = vec4(fragColor.r * 0.1, fragColor.r * 0.2 + fragColor.b * 0.2 + fragColor.g*0.7, fragColor.b * 0.1, 1.0f);
        }
        """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    shaderProgram2 = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader2, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader2, GL_FRAGMENT_SHADER))

    shaderProgram_night = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_night, GL_FRAGMENT_SHADER))

    shaderProgram_nocturne_vision = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_nocturne_vision, GL_FRAGMENT_SHADER))

# Creating shapes on GPU memory
gpuSky = createSky(0, 1)
gpuDunes = createDunes(-1 )
gpuPiramid = createPiramid()

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

    # Drawing the shapes with a specific shader program depending on the controller state
    if controller.shader_to_use == 1:  # modo gris
        # Telling OpenGL to use our shader program
        glUseProgram(shaderProgram2)
        # Telling OpenGL to draw our shapes using the previous shader program.
        drawShape(shaderProgram2, gpuSky)
        drawShape(shaderProgram2, gpuDunes)
        drawShape(shaderProgram2, gpuPiramid)


    elif controller.shader_to_use == 0:  # modo normal
        # Telling OpenGL to use our shader program
        glUseProgram(shaderProgram)
        # Telling OpenGL to draw our shapes using the previous shader program.
        drawShape(shaderProgram, gpuSky)
        drawShape(shaderProgram, gpuDunes)
        drawShape(shaderProgram, gpuPiramid)

    elif controller.shader_to_use == 2:  # modo normal
        # Telling OpenGL to use our shader program
        glUseProgram(shaderProgram_nocturne_vision)
        # Telling OpenGL to draw our shapes using the previous shader program.
        drawShape(shaderProgram, gpuSky)
        drawShape(shaderProgram, gpuDunes)
        drawShape(shaderProgram, gpuPiramid)

    else:  # modo noche
        # Telling OpenGL to use our shader program
        glUseProgram(shaderProgram_night)
        # Telling OpenGL to draw our shapes using the previous shader program.
        drawShape(shaderProgram_night, gpuSky)
        drawShape(shaderProgram_night, gpuDunes)
        drawShape(shaderProgram_night, gpuPiramid)

    # Once the render is done, buffers are swapped, showing only the complete scene.
    glfw.swap_buffers(window)

glfw.terminate()