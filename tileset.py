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
from pyglet.gl import *

class TileSet:
    def __init__(self):
        tile_data = pyglet.resource.file('tiles/tiles.json', 'r')
        self.tiles = json.load(tile_data)
        self.tile_images = {}

        self.atlas = pyglet.image.atlas.TextureAtlas()

        glBindTexture(GL_TEXTURE_2D, self.atlas.texture.id) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        self.tilesize = self.tiles['tile_size']

        for tile in self.tiles['tiles']:
            tile_name = tile['name']
            texture_path = tile['texture']
            tile_image = pyglet.resource.image(texture_path, atlas=False)
            image_data = tile_image.get_image_data()
            tile_region = self.atlas.add(image_data, border=1)
            self.tile_images[tile_name] = tile_region

    def __getitem__(self, tile_name):
        if tile_name in self.tile_images:
            return self.tile_images[tile_name]
        else:
            raise KeyError(f"Tile '{tile_name}' not found in tileset.")
