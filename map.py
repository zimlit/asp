# Copyright (C) 2025 Devin Rockwell
# 
# asp is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# asp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with asp. If not, see <https://www.gnu.org/licenses/>.

import json
import pyglet
from pyglet import math

import tileset

class Tile:
    def __init__(self, x, y, texture, size=32, batch=None):
        self.x = x
        self.y = y
        self.size = size
        self.texture = texture
        self.sprite = pyglet.sprite.Sprite(
            img=texture,
            x=x * size,
            y=y * size,
            batch=batch
        )

class Map(pyglet.event.EventDispatcher):
    def __init__(self, window, file, zoom=1):
        self.file = file
        self.zoom = zoom
        self.tiles = []
        self.size = (0, 0)
        self.offset = math.Vec2(0, 0)
        self.batch = pyglet.graphics.Batch()
        self.tileset = tileset.TileSet()
        self.map_data = None
        self.register_event_type('on_mouse_press')
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window = window
        self.window.push_handlers(self)
        self.window.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update, 1/30.0)
        self.window.view = math.Mat4.from_scale(math.Vec3(self.zoom, self.zoom, 1)) @ math.Mat4.from_translation(math.Vec3(-self.offset.x, -self.offset.y, 0))
        self.load_map()
        

    def load_map(self):
        self.map_data = json.load(pyglet.resource.file(self.file, 'r'))
        self.size = (self.map_data["width"], self.map_data["height"])
        tiles = self.map_data["tiles"]
        if len(tiles) != self.size[1]:
            raise ValueError("Map data does not match specified size.")
        
        for y, row in enumerate(tiles):
            if len(row) != self.size[0]:
                raise ValueError("Map data does not match specified size.")
            for x, tile_name in enumerate(row):
                if tile_name in self.tileset.tile_images:
                    tile_texture = self.tileset[tile_name]
                    tile = Tile(x, y, tile_texture, size=self.tileset.tilesize, batch=self.batch)
                    self.tiles.append(tile)

    def draw(self):

        self.batch.invalidate()
        self.batch.draw()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.zoom += 1
        elif scroll_y < 0 and self.zoom > 0.2:
            self.zoom -= 1

        self.window.view = math.Mat4.from_scale(math.Vec3(self.zoom, self.zoom, 1)) @ math.Mat4.from_translation(math.Vec3(-self.offset.x, -self.offset.y, 0))
       

    def update(self, dt):
        offset = math.Vec2()
        moved = False
        if self.keys[pyglet.window.key.UP]:
            offset = math.Vec2(offset.x, 1)
            moved = True
        if self.keys[pyglet.window.key.DOWN]:
            offset = math.Vec2(offset.x, -1)
            moved = True
        if self.keys[pyglet.window.key.LEFT]:
            offset = math.Vec2(-1, offset.y)
            moved = True
        if self.keys[pyglet.window.key.RIGHT]:
            offset = math.Vec2(1, offset.y)
            moved = True

        if moved:
            offset = offset.normalize() * 10
            self.offset = self.offset + offset
            self.window.view = math.Mat4.from_scale(math.Vec3(self.zoom, self.zoom, 1)) @ math.Mat4.from_translation(math.Vec3(-self.offset.x, -self.offset.y, 0))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.RIGHT:
            self.offset = self.offset + math.Vec2(dx, dy)
            self.window.view = math.Mat4.from_scale(math.Vec3(self.zoom, self.zoom, 1)) @ math.Mat4.from_translation(math.Vec3(-self.offset.x, -self.offset.y, 0))
