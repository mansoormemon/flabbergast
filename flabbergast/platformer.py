import arcade as arc

from . import xarcade as xarc
from .assets import asset
from .core import vmath
from .core.mapgenerator import Map, Maze
from .references import SceneList

PADDING = 3
DEFAULT_COMPLEXITY = 0.6


class Platformer(xarc.AbstractScene):
    class Tile:
        SIZE = 64

    def __init__(self):
        self._complexity = None
        self._walls = None
        self._maze_map = None
        self._sprites = None
        self._player = None
        self._physics_engine = None

        super().__init__(SceneList.PLATFORMER)

    def setup(self, *args, complexity=DEFAULT_COMPLEXITY, **kwargs):
        self._complexity = complexity

        self._walls = arc.SpriteList(use_spatial_hash=True)

        scaled_padding = PADDING / self._complexity
        scaled_tile_size = self.Tile.SIZE * self._complexity

        estimated_x_tiles = vmath.round_down_to_even(
            int((xarc.Meta.screen_width() // scaled_tile_size) - scaled_padding))
        estimated_y_tiles = vmath.round_down_to_even(
            int((xarc.Meta.screen_height() // scaled_tile_size) - scaled_padding))

        maze_rows, maze_cols = int(estimated_y_tiles // 2), int(estimated_x_tiles // 2)
        self._maze_map = Map.generate((maze_rows, maze_cols), generator=Maze.Kruskal)

        y_tiles, x_tiles = self._maze_map.shape
        x_span_diff = xarc.Meta.screen_width() - (x_tiles * scaled_tile_size)
        y_span_diff = xarc.Meta.screen_height() - (y_tiles * scaled_tile_size)
        x_offset = (scaled_tile_size + x_span_diff) / 2
        y_offset = (scaled_tile_size + y_span_diff) / 2
        for y, row in enumerate(self._maze_map):
            for x, col in enumerate(row):
                if col:
                    tile = asset("images/textures/floortexture31.png")
                else:
                    tile = asset("images/textures/floortexture8.png")
                wall = arc.Sprite(tile, self._complexity)
                wall.center_x = (x * scaled_tile_size) + x_offset
                wall.center_y = (y * scaled_tile_size) + y_offset
                self._walls.append(wall)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.ESCAPE:
                self.curtains.set_scene(SceneList.MAINMENU)
