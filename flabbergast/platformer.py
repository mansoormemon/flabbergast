from .assets import *
from .dataproxy import *
from .core.mapgenerator import *
from .core.vmath import *
from .xarcade import *
from .references import SceneList


class Platformer(AbstractScene):
    class Tile:
        SCALE = 0.36
        SIZE = 64

    PADDING = int(5 / Tile.SCALE)

    def __init__(self):
        self._walls = None
        self._controls = None
        self._sprites = None
        self._maze_map = None

        super().__init__(SceneList.PLATFORMER)

    def setup(self):
        arc.set_background_color(arc.color.ALMOND)
        self._walls = arc.SpriteList(use_spatial_hash=True)
        self._controls = arc.SpriteList(use_spatial_hash=True)
        self._sprites = arc.SpriteList()

        scaled_tile_size = self.Tile.SIZE * self.Tile.SCALE

        estimated_x_tiles = round_down_to_even(
            int(Meta.screen_width() // scaled_tile_size) - self.PADDING
        )
        estimated_y_tiles = round_down_to_even(
            int(Meta.screen_height() // scaled_tile_size) - self.PADDING
        )

        maze_rows, maze_cols = int(half(estimated_y_tiles)), int(
            half(estimated_x_tiles)
        )
        self._maze_map = Map.generate((maze_rows, maze_cols), generator=Maze.Kruskal)

        y_tiles, x_tiles = self._maze_map.shape

        x_span_diff = Meta.screen_width() - (x_tiles * scaled_tile_size)
        y_span_diff = Meta.screen_height() - (y_tiles * scaled_tile_size)

        x_offset = half(scaled_tile_size + x_span_diff)
        y_offset = half(scaled_tile_size + y_span_diff)

        for y, row in enumerate(self._maze_map):
            for x, col in enumerate(row):
                if col:
                    continue
                tile = asset(TEXTURES_FLOORGARDEN)

                wall = arc.Sprite(tile, self.Tile.SCALE)
                wall.center_x = (x * scaled_tile_size) + x_offset
                wall.center_y = (y * scaled_tile_size) + y_offset
                self._walls.append(wall)
