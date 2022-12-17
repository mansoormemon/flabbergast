import arcade as arc
import arcade_curtains as arc_curts

from flabbergast.assets import *
from flabbergast.maps import *
from flabbergast.metadata import *
from flabbergast.util import *


class Level(arc_curts.BaseScene):
    class Tile:
        SCALE = 0.36
        SIZE = 64

    PADDING = int(5 / Tile.SCALE)

    def setup(self):
        arc.set_background_color(arc.color.ALMOND)
        self._walls = arc.SpriteList(use_spatial_hash=True)
        self._controls = arc.SpriteList(use_spatial_hash=True)
        self._sprites = arc.SpriteList()

        scaled_tile_size = self.Tile.SIZE * self.Tile.SCALE

        estimated_x_tiles = round_down_to_even(
            int(Metadata.screen_width() // scaled_tile_size) - self.PADDING
        )
        estimated_y_tiles = round_down_to_even(
            int(Metadata.screen_height() // scaled_tile_size) - self.PADDING
        )

        maze_rows, maze_cols = int(half(estimated_y_tiles)), int(
            half(estimated_x_tiles)
        )
        self._maze_map = Map.generate((maze_rows, maze_cols), generator=Maze.Kruskal)

        y_tiles, x_tiles = self._maze_map.shape

        x_span_diff = Metadata.screen_width() - (x_tiles * scaled_tile_size)
        y_span_diff = Metadata.screen_height() - (y_tiles * scaled_tile_size)

        x_offset = half(scaled_tile_size + x_span_diff)
        y_offset = half(scaled_tile_size + y_span_diff)

        for y, row in enumerate(self._maze_map):
            for x, col in enumerate(row):
                tile = (
                    ":resources:images/topdown_tanks/tileSand1.png"
                    if col
                    else ":resources:images/topdown_tanks/tileGrass2.png"
                )
                wall = arc.Sprite(tile, self.Tile.SCALE)
                wall.center_x = (x * scaled_tile_size) + x_offset
                wall.center_y = (y * scaled_tile_size) + y_offset
                self._walls.append(wall)
