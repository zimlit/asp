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
        print(json.dumps(self.tiles, indent=4))

        self.tilesize = self.tiles['tile_size']

        # Create a custom texture atlas with border padding
        atlas = pyglet.image.atlas.TextureAtlas(512, 512)
        
        # Apply texture parameters to the atlas texture
        glBindTexture(atlas.texture.target, atlas.texture.id)
        glTexParameteri(atlas.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(atlas.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(atlas.texture.target, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(atlas.texture.target, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        for tile in self.tiles['tiles']:
            tile_name = tile['name']
            texture_path = tile['texture']
            # Load image without auto-atlas
            tile_image = pyglet.resource.image(texture_path, atlas=False)
            print(f"{tile_image.width}x{tile_image.height} {tile_name} {texture_path}")
            # Convert texture to image data for atlas
            image_data = tile_image.get_image_data()
            # Add to our atlas with 1-pixel border
            tile_region = atlas.add(image_data, border=1)
            self.tile_images[tile_name] = tile_region

    def __getitem__(self, tile_name):
        if tile_name in self.tile_images:
            return self.tile_images[tile_name]
        else:
            raise KeyError(f"Tile '{tile_name}' not found in tileset.")
