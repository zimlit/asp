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

class TileSet:
    def __init__(self):
        tile_data = pyglet.resource.file('tiles/tiles.json', 'r')
        self.tiles = json.load(tile_data)
        self.tile_images = {}
        print(json.dumps(self.tiles, indent=4))

        self.tilesize = self.tiles['tile_size']

        for tile in self.tiles['tiles']:
            tile_name = tile['name']
            texture_path = tile['texture']
            tile_image = pyglet.resource.image(texture_path)
            print(f"{tile_image.width}x{tile_image.height} {tile_name} {texture_path}")
            self.tile_images[tile_name] = tile_image

    def __getitem__(self, tile_name):
        if tile_name in self.tile_images:
            return self.tile_images[tile_name]
        else:
            raise KeyError(f"Tile '{tile_name}' not found in tileset.")
