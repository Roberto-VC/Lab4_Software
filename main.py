import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm

pygame.init()

screen = pygame.display.set_mode(
    (1200, 1200),
    pygame.OPENGL | pygame.DOUBLEBUF
)
# dT = pygame.time.Clock()



vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;

uniform mat4 amatrix;

out vec3 ourColor;


void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    ourColor = vertexColor;

}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform vec3 color;


in vec3 ourColor;

void main()
{
    // fragColor = vec4(ourColor, 1.0f);
    fragColor = vec4(color, 1.0f);
}
"""
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
)

glUseProgram(shader)



vertex_data = numpy.array([
    -1.0,-1.0,-1.0,
    -1.0,-1.0, 1.0,
    -1.0, 1.0, 1.0, 
    1.0, 1.0,-1.0,
    -1.0,-1.0,-1.0,
    -1.0, 1.0,-1.0, 
    1.0,-1.0, 1.0,
    -1.0,-1.0,-1.0,
    1.0,-1.0,-1.0,
    1.0, 1.0,-1.0,
    1.0,-1.0,-1.0,
    -1.0,-1.0,-1.0,
    -1.0,-1.0,-1.0,
    -1.0, 1.0, 1.0,
    -1.0, 1.0,-1.0,
    1.0,-1.0, 1.0,
    -1.0,-1.0, 1.0,
    -1.0,-1.0,-1.0,
    -1.0, 1.0, 1.0,
    -1.0,-1.0, 1.0,
    1.0,-1.0, 1.0,
    1.0, 1.0, 1.0,
    1.0,-1.0,-1.0,
    1.0, 1.0,-1.0,
    1.0,-1.0,-1.0,
    1.0, 1.0, 1.0,
    1.0,-1.0, 1.0,
    1.0, 1.0, 1.0,
    1.0, 1.0,-1.0,
    -1.0, 1.0,-1.0,
    1.0, 1.0, 1.0,
    -1.0, 1.0,-1.0,
    -1.0, 1.0, 1.0,
    1.0, 1.0, 1.0,
    -1.0, 1.0, 1.0,
    1.0,-1.0, 1.0
], dtype=numpy.float32)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(
    GL_ARRAY_BUFFER,  # tipo de datos
    vertex_data.nbytes,  # tamaño de da data en bytes    
    vertex_data, # puntero a la data
    GL_STATIC_DRAW
)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3 * 4,
    ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)


glVertexAttribPointer(
    1,
    3,
    GL_FLOAT,
    GL_FALSE,
    3 * 4,
    ctypes.c_void_p(3)
)
glEnableVertexAttribArray(1)


def calculateMatrix(angle1, angle2, vertical, horizontal):
    i = glm.mat4(1)
    translate1 = glm.translate(i, glm.vec3(vertical, 0, 0))
    translate2 = glm.translate(i, glm.vec3(0, horizontal, 0))
    rotate = glm.rotate(i, glm.radians(angle1), glm.vec3(0, 1, 0))
    rotate1 = glm.rotate(i, glm.radians(angle2), glm.vec3(1, 0, 0))
    scale = glm.scale(i, glm.vec3(1, 1, 1))

    model = translate1 * translate2 * rotate * rotate1 * scale

    view = glm.lookAt(
        glm.vec3(0, 0, 5),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 1, 0)
    )

    projection = glm.perspective(
        glm.radians(45),
        1600/1200,
        0.1,
        1000.0
    )

    amatrix = projection * view * model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'amatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(amatrix)
    )

glViewport(0, 0, 1600, 1200)



running = True

glClearColor(0.5, 1.0, 0.5, 1.0)

r = 0
n = 0
v = 0
h = 0
print("Hola! Bienvenido al Model Viewer!")
print("Utilize WASD para mover el cubo, y las flechas para girarlo")
print("Eliga los siguientes shaders!")
print("1. Un color aleatorio.\n2. Basado en posición del cubo.\n3. Gire el cubo y mire como cambia de colores")
while running:

    glClear(GL_COLOR_BUFFER_BIT)
    calculateMatrix(r, n, h, v)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLES, 0, 12*3)
    pygame.display.flip()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                r -= 10
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_RIGHT:
                r += 10
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_UP:
                n -= 10
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_DOWN:
                n += 10
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_w:
                v += 0.2
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_s:
                v -= 0.2
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_a:
                h -= 0.2
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_d:
                h += 0.2
                calculateMatrix(r, n, h, v)
                pygame.display.flip()
            if event.key == pygame.K_1:
                vertex_shader = """
                #version 460
                layout (location = 0) in vec3 position;
                layout (location = 1) in vec3 vertexColor;

                uniform mat4 amatrix;

                out vec3 ourColor;


                void main()
                {
                    gl_Position = amatrix * vec4(position, 1.0f);
                    ourColor = vertexColor;

                }
                """

                fragment_shader = """
                #version 460

                layout (location = 0) out vec4 fragColor;

                uniform vec3 color;


                in vec3 ourColor;

                void main()
                {
                    // fragColor = vec4(ourColor, 1.0f);
                    fragColor = vec4(color, 1.0f);
                }
                """
                compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
                compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
                shader = compileProgram(
                    compiled_vertex_shader,
                    compiled_fragment_shader
                )

                glUseProgram(shader)



                vertex_data = numpy.array([
                    -1.0,-1.0,-1.0,
                    -1.0,-1.0, 1.0,
                    -1.0, 1.0, 1.0, 
                    1.0, 1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0,-1.0, 
                    1.0,-1.0, 1.0,
                    -1.0,-1.0,-1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0,-1.0,
                    1.0,-1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    -1.0, 1.0,-1.0,
                    1.0,-1.0, 1.0,
                    -1.0,-1.0, 1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    -1.0,-1.0, 1.0,
                    1.0,-1.0, 1.0,
                    1.0, 1.0, 1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0,-1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0, 1.0,
                    1.0,-1.0, 1.0,
                    1.0, 1.0, 1.0,
                    1.0, 1.0,-1.0,
                    -1.0, 1.0,-1.0,
                    1.0, 1.0, 1.0,
                    -1.0, 1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0,
                    -1.0, 1.0, 1.0,
                    1.0,-1.0, 1.0
                ], dtype=numpy.float32)

                vertex_buffer_object = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
                glBufferData(
                    GL_ARRAY_BUFFER,  # tipo de datos
                    vertex_data.nbytes,  # tamaño de da data en bytes    
                    vertex_data, # puntero a la data
                    GL_STATIC_DRAW
                )
                vertex_array_object = glGenVertexArrays(1)
                glBindVertexArray(vertex_array_object)

                glVertexAttribPointer(
                    0,
                    3,
                    GL_FLOAT,
                    GL_FALSE,
                    3 * 4,
                    ctypes.c_void_p(0)
                )
                glEnableVertexAttribArray(0)


                glVertexAttribPointer(
                    1,
                    3,
                    GL_FLOAT,
                    GL_FALSE,
                    3 * 4,
                    ctypes.c_void_p(3)
                )
                glEnableVertexAttribArray(1)


                color1 = random.random()
                color2 = random.random()
                color3 = random.random()

                color = glm.vec3(color1, color2, color3)

                glUniform3fv(
                    glGetUniformLocation(shader,'color'),
                    1,
                    glm.value_ptr(color)
                )

                pygame.time.wait(50)
                glDrawArrays(GL_TRIANGLES, 0, 3)
            if event.key == pygame.K_3:
                vertex_shader = """
                #version 460
                layout (location = 0) in vec3 position;
                layout (location = 2) in vec3 vertexColor;

                uniform mat4 amatrix;

                out vec3 ourColor;


                void main()
                {
                    gl_Position = amatrix * vec4(position, 1.0f);
                    ourColor = vec3(1.0f,1.0f,1.0f);
                    if (gl_Position.y > 0 && gl_Position.y < 1)
                        ourColor.y = 0.0f;
                    if (gl_Position.z > 0 && gl_Position.z < 1)
                        ourColor.x = 0.0f;
                    if (gl_Position.x > 0 && gl_Position.x < 1)
                        ourColor.z= 0.0f;

                }
                """

                fragment_shader = """
                #version 460

                layout (location = 0) out vec4 fragColor;

                uniform vec3 color;


                in vec3 ourColor;

                void main()
                {
                    // fragColor = vec4(ourColor, 1.0f);
                    fragColor = vec4(ourColor, 1.0f);
                }
                """
                compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
                compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
                shader = compileProgram(
                    compiled_vertex_shader,
                    compiled_fragment_shader
                )

                glUseProgram(shader)
                vertex_data = numpy.array([
                    -1.0,-1.0,-1.0,
                    -1.0,-1.0, 1.0,
                    -1.0, 1.0, 1.0, 
                    1.0, 1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0,-1.0, 
                    1.0,-1.0, 1.0,
                    -1.0,-1.0,-1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0,-1.0,
                    1.0,-1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    -1.0, 1.0,-1.0,
                    1.0,-1.0, 1.0,
                    -1.0,-1.0, 1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    -1.0,-1.0, 1.0,
                    1.0,-1.0, 1.0,
                    1.0, 1.0, 1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0,-1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0, 1.0,
                    1.0,-1.0, 1.0,
                    1.0, 1.0, 1.0,
                    1.0, 1.0,-1.0,
                    -1.0, 1.0,-1.0,
                    1.0, 1.0, 1.0,
                    -1.0, 1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0,
                    -1.0, 1.0, 1.0,
                    1.0,-1.0, 1.0
                ], dtype=numpy.float32)

                vertex_buffer_object = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
                glBufferData(
                    GL_ARRAY_BUFFER,  # tipo de datos
                    vertex_data.nbytes,  # tamaño de da data en bytes    
                    vertex_data, # puntero a la data
                    GL_STATIC_DRAW
                )
                vertex_array_object = glGenVertexArrays(1)
                glBindVertexArray(vertex_array_object)

                glVertexAttribPointer(
                    0,
                    3,
                    GL_FLOAT,
                    GL_FALSE,
                    3 * 4,
                    ctypes.c_void_p(0)
                )
                glEnableVertexAttribArray(0)


                glVertexAttribPointer(
                    1,
                    3,
                    GL_FLOAT,
                    GL_FALSE,
                    3 * 4,
                    ctypes.c_void_p(3)
                )
                glEnableVertexAttribArray(1)
            if event.key == pygame.K_2:
                vertex_shader = """
                #version 460
                layout (location = 0) in vec3 position;
                layout (location = 2) in vec3 vertexColor;

                uniform mat4 amatrix;

                out vec3 ourColor;


                void main()
                {
                    gl_Position = amatrix * vec4(position, 1.0f);
                    ourColor = vec3(gl_Position.x,gl_Position.z, gl_Position.y);

                }
                """

                fragment_shader = """
                #version 460

                layout (location = 0) out vec4 fragColor;

                uniform vec3 color;


                in vec3 ourColor;

                void main()
                {
                    // fragColor = vec4(ourColor, 1.0f);
                    fragColor = vec4(ourColor, 1.0f);
                }
                """
                compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
                compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
                shader = compileProgram(
                    compiled_vertex_shader,
                    compiled_fragment_shader
                )

                glUseProgram(shader)
                vertex_data = numpy.array([
                    -1.0,-1.0,-1.0,
                    -1.0,-1.0, 1.0,
                    -1.0, 1.0, 1.0, 
                    1.0, 1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0,-1.0, 
                    1.0,-1.0, 1.0,
                    -1.0,-1.0,-1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0,-1.0,
                    1.0,-1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    -1.0, 1.0,-1.0,
                    1.0,-1.0, 1.0,
                    -1.0,-1.0, 1.0,
                    -1.0,-1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    -1.0,-1.0, 1.0,
                    1.0,-1.0, 1.0,
                    1.0, 1.0, 1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0,-1.0,
                    1.0,-1.0,-1.0,
                    1.0, 1.0, 1.0,
                    1.0,-1.0, 1.0,
                    1.0, 1.0, 1.0,
                    1.0, 1.0,-1.0,
                    -1.0, 1.0,-1.0,
                    1.0, 1.0, 1.0,
                    -1.0, 1.0,-1.0,
                    -1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0,
                    -1.0, 1.0, 1.0,
                    1.0,-1.0, 1.0
                ], dtype=numpy.float32)

                vertex_buffer_object = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
                glBufferData(
                    GL_ARRAY_BUFFER,  # tipo de datos
                    vertex_data.nbytes,  # tamaño de da data en bytes    
                    vertex_data, # puntero a la data
                    GL_STATIC_DRAW
                )
                vertex_array_object = glGenVertexArrays(1)
                glBindVertexArray(vertex_array_object)

                glVertexAttribPointer(
                    0,
                    3,
                    GL_FLOAT,
                    GL_FALSE,
                    3 * 4,
                    ctypes.c_void_p(0)
                )
                glEnableVertexAttribArray(0)


                glVertexAttribPointer(
                    1,
                    3,
                    GL_FLOAT,
                    GL_FALSE,
                    3 * 4,
                    ctypes.c_void_p(3)
                )
                glEnableVertexAttribArray(1)

                

                
            
            
