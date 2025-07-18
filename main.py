import pyglet
import map
import tileset
import cProfile
from pyglet import math
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)

map = map.Map(window, "chapter1/map.json", zoom=8)

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
