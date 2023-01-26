from typing import Optional, Tuple

import arcade as arc
import numpy as np

from . import xarcade as xarc
from .assets import asset
from .core import vmath
from .core.mapgenerator import Map, Maze
from .player import Player
from .references import SceneList

PADDING: int = 4
DEFAULT_COMPLEXITY: float = 1


class Grid:
    def __init__(self, platform):
        self.scale: float = platform.complexity
        self.shape: Tuple[int, int] = platform.maze_map.shape
        self.block_size: int = platform.Tile.SIZE * self.scale

        rows, cols = self.shape
        width, height = cols * self.block_size, rows * self.block_size
        self.dimensions: Tuple[float, float] = width, height

        self.begin: Tuple[float, float] = (xarc.Meta.hz_screen_center() - (width / 2),
                                           xarc.Meta.vt_screen_center() + (height / 2))

        self.end: Tuple[float, float] = (xarc.Meta.hz_screen_center() + (width / 2),
                                         xarc.Meta.vt_screen_center() - (height / 2))

        self.start: Tuple[float, float] = self.center_of(4, 1)
        self.stop: Tuple[float, float] = self.center_of(self.shape[0] - 2, self.shape[1] - 2)

    def center_of(self, r, c):
        center_x = self.begin[0] + (c * self.block_size) + (self.block_size / 2)
        center_y = self.begin[1] - (r * self.block_size) - (self.block_size / 2)
        return center_x, center_y


class Platformer(xarc.AbstractScene):
    class Tile:
        SIZE: int = 64

    class BlockType:
        WALL = 0
        PATH = 1

    def __init__(self):
        self.complexity: Optional[float] = None
        self.walls: Optional[arc.SpriteList] = None
        self.path: Optional[arc.SpriteList] = None
        self.maze_map: Optional[np.ndarray] = None
        self.sprites: Optional[arc.SpriteList] = None
        self.player: Optional[Player] = None
        self.physics_engine: Optional[arc.PhysicsEngineSimple] = None
        self.grid: Optional[Grid] = None

        super().__init__(SceneList.PLATFORMER)

    def setup(self, *args, complexity=DEFAULT_COMPLEXITY, **kwargs):
        self.complexity = complexity

        self.walls = arc.SpriteList(use_spatial_hash=True)
        self.path = arc.SpriteList(use_spatial_hash=True)

        scaled_padding: float = PADDING / self.complexity
        scaled_tile_size: float = self.Tile.SIZE * self.complexity

        estimated_x_tiles: int = vmath.round_down_to_even(
            int((xarc.Meta.screen_width() // scaled_tile_size) - scaled_padding))
        estimated_y_tiles: int = vmath.round_down_to_even(
            int((xarc.Meta.screen_height() // scaled_tile_size) - scaled_padding))

        maze_rows, maze_cols = int(estimated_y_tiles // 2), int(estimated_x_tiles // 2)
        self.maze_map = Map.generate((maze_rows, maze_cols), generator=Maze.Kruskal)

        y_tiles, x_tiles = self.maze_map.shape
        x_span_diff: float = xarc.Meta.screen_width() - (x_tiles * scaled_tile_size)
        y_span_diff: float = xarc.Meta.screen_height() - (y_tiles * scaled_tile_size)
        x_offset: float = (scaled_tile_size + x_span_diff) / 2
        y_offset: float = (scaled_tile_size + y_span_diff) / 2
        for y, row in enumerate(self.maze_map):
            for x, col in enumerate(row):
                center_x: float = (x * scaled_tile_size) + x_offset
                center_y: float = (y * scaled_tile_size) + y_offset
                block: arc.Sprite
                match col:
                    case self.BlockType.WALL:
                        texture: str = asset("images/textures/floortexture8.png")
                        block = arc.Sprite(texture, self.complexity)
                        self.walls.append(block)
                    case self.BlockType.PATH:
                        texture: str = asset("images/textures/floortexture31.png")
                        block = arc.Sprite(texture, self.complexity)
                        self.path.append(block)
                block.center_x, block.center_y = center_x, center_y

        self.grid = Grid(self)

        self.sprites = arc.SpriteList()

        self.player1 = Player(self.grid, self.grid.stop)
        self.sprites.append(self.player1)

        self.player2 = Player(self.grid, self.grid.start)
        self.sprites.append(self.player2)

        # self.physics_engine = arc.PhysicsEngineSimple(self.player, self.walls)

        begin = arc.SpriteSolidColor(3, 3, arc.color.BLUE)
        begin.center_x, begin.center_y = self.grid.begin
        end = arc.SpriteSolidColor(3, 3, arc.color.GREEN)
        end.center_x, end.center_y = self.grid.end

        self.walls.append(begin)
        self.walls.append(end)

    def draw(self):
        super().draw()
        
        rows, cols = self.maze_map.shape
        for r in range(rows):
            for c in range(cols):
                coords = self.grid.center_of(r, c)
                arc.draw_point(*coords, arc.color.YELLOW, 3)

    def on_update(self, delta_time: float):
        # self.physics_engine.update()
        self.sprites.update()

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.ESCAPE:
                self.curtains.set_scene(SceneList.MAINMENU)
            case arc.key.UP:
                self.player1.move_up()
                self.player2.move_up()
            case arc.key.DOWN:
                self.player1.move_down()
                self.player2.move_down()
            case arc.key.RIGHT:
                self.player1.move_right()
                self.player2.move_right()
            case arc.key.LEFT:
                self.player1.move_left()
                self.player2.move_left()

    def on_key_release(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.UP | arc.key.DOWN:
                self.player1.change_y = 0
                self.player2.change_y = 0
            case arc.key.RIGHT | arc.key.LEFT:
                self.player1.change_x = 0
                self.player2.change_x = 0
