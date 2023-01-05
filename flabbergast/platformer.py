import arcade as arc

from .assets import asset
from .core import vmath
from .core.mapgenerator import Map, Maze
from .dataproxy import Meta
from .references import SceneList

from . import xarcade as xarc


class Platformer(xarc.AbstractScene):
    class Tile:
        SIZE = 64

    PADDING = 3
    DEFAULT_COMPLEXITY = 0.6

    def __init__(self):
        self._walls = None
        self._controls = None
        self._sprites = None
        self._maze_map = None
        self._complexity = None

        super().__init__(SceneList.PLATFORMER)

    def setup(self, *args, complexity=DEFAULT_COMPLEXITY, **kwargs):
        self._walls = arc.SpriteList(use_spatial_hash=True)
        self._controls = arc.SpriteList(use_spatial_hash=True)
        self._sprites = arc.SpriteList()

        self._complexity = complexity

        scaled_padding = self.PADDING / self._complexity
        scaled_tile_size = self.Tile.SIZE * self._complexity

        estimated_x_tiles = vmath.round_down_to_even(int(Meta.screen_width() // scaled_tile_size) - scaled_padding)
        estimated_y_tiles = vmath.round_down_to_even(int(Meta.screen_height() // scaled_tile_size) - scaled_padding)

        maze_rows, maze_cols = int(vmath.half(estimated_y_tiles)), int(vmath.half(estimated_x_tiles))
        self._maze_map = Map.generate((maze_rows, maze_cols), generator=Maze.Kruskal)

        y_tiles, x_tiles = self._maze_map.shape
        x_span_diff = Meta.screen_width() - (x_tiles * scaled_tile_size)
        y_span_diff = Meta.screen_height() - (y_tiles * scaled_tile_size)
        x_offset = vmath.half(scaled_tile_size + x_span_diff)
        y_offset = vmath.half(scaled_tile_size + y_span_diff)
        for y, row in enumerate(self._maze_map):
            for x, col in enumerate(row):
                if col:
                    tile = asset("textures/floortexture31.png")
                else:
                    tile = asset("textures/floortexture8.png")
                wall = arc.Sprite(tile, self._complexity)
                wall.center_x = (x * scaled_tile_size) + x_offset
                wall.center_y = (y * scaled_tile_size) + y_offset
                self._walls.append(wall)

        self.events.key_up(arc.key.ESCAPE, lambda *_: self.curtains.set_scene(SceneList.MAINMENU))
