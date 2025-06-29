import pyglet
import map
import tileset
import cProfile
from pyglet import math
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)


map = map.Map(window, "", zoom=8)

fps_display = pyglet.window.FPSDisplay(window=window, color=(0, 255, 255, 255))

@window.event
def on_draw():
    window.clear()
    map.draw()
    camera = window.view
    window.view = math.Mat4()
    fps_display.draw()
    window.view = camera

if __name__ == '__main__':
    pyglet.app.run()
