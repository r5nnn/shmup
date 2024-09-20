import os
import sys

import moderngl
import pygame
import numpy as np
import time
from PIL import Image

os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'

pygame.init()
pygame.display.set_mode((2560, 1440), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

class Scene:
    def __init__(self):
        self.ctx = moderngl.get_context()

        # Store the time when the program starts
        self.start_time = time.time()

        self.program = self.ctx.program(
            vertex_shader='''
                #version 330 core
                in vec2 in_vert;
                out vec2 v_text;
                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                    v_text = in_vert.xy;
                }
            ''',
            fragment_shader=open('frag.glsl').read()  # Load the new shader
        )

        # Pass uniforms
        self.iResolution = self.program['iResolution']
        self.iTime = self.program['iTime']
        self.iMouse = self.program['iMouse']
        # self.iChannel0 = self.program['iChannel0']  # Texture uniform

        # Set up a simple quad (2 triangles) covering the screen
        vertices = np.array([
            -1.0, -1.0,
             1.0, -1.0,
             1.0,  1.0,
            -1.0, -1.0,
             1.0,  1.0,
            -1.0,  1.0
        ], dtype='f4')
        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, 'in_vert')

        # Load texture
        self.texture = self.load_texture('noise.png')  # Replace with your texture

    def load_texture(self, path):
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert('RGB')
        texture = self.ctx.texture(img.size, 3, img.tobytes())
        texture.build_mipmaps()
        return texture

    def render(self):
        self.ctx.clear(0.0, 0.0, 0.0)

        # Update uniforms
        self.iResolution.value = (2560, 1440)

        # Calculate elapsed time and pass it to iTime
        elapsed_time = time.time() - self.start_time
        self.iTime.value = elapsed_time

        # Get mouse position and pass it to iMouse
        mouse_pos = pygame.mouse.get_pos()
        self.iMouse.value = (mouse_pos[0], 800 - mouse_pos[1], 0, 0)  # iMouse.xy is mouse position, iMouse.zw not used

        # Bind texture to iChannel0
        self.texture.use(location=0)  # Texture unit 0
        # self.iChannel0.value = 0  # Use texture unit 0 for iChannel0

        self.vao.render(moderngl.TRIANGLES)

scene = Scene()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.render()
    pygame.display.flip()