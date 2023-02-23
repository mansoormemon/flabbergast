import json
from typing import Callable, Optional, Tuple

import arcade as arc

from . import xarcade as xarc
from .assets import (
    AUDIO_THEREISAPATTERN,
    CUTSCENE_OPENING
)
from .assets import asset
from .references import CutSceneList, SceneList

FONT_COLOR: Tuple[int, int, int] = arc.color.WHITE_SMOKE
FONT_NAME: str = "Tekton Display Ssi"

PADDED_SCREEN_WIDTH: Callable = lambda: int(xarc.Meta.screen_width() * 0.9)

OPENING_SCENE_TIME_SPAN: Tuple[int, int] = (0, 2)

TITLE_Y: Callable = lambda: xarc.Meta.screen_height() * 0.8
TITLE_FONT_SIZE: int = 28

BODY_Y: Callable = lambda: xarc.Meta.screen_height() * 0.7
BODY_FONT_SIZE: int = 16

OBJECTIVES_Y: Callable = lambda: xarc.Meta.screen_height() * 0.5
OBJECTIVES_FONT_SIZE: int = 10

FOOTNOTES_Y: Callable = lambda: xarc.Meta.screen_height() * 0.05
FOOTNOTES_FONT_SIZE: int = 8


class _Parser:
    @staticmethod
    def parse(file: str) -> Tuple[str, str, str, str]:
        file = asset(file)
        with open(file) as f:
            data = json.load(f)
            title = data["title"]
            body = data["body"]
            objectives = data["objectives"]
            footnotes = data["footnotes"]

        parsed_title = title
        parsed_body = "\n\n".join(body)
        parsed_objectives = "\n\n".join([f"{n + 1}. {objective}" for n, objective in enumerate(objectives)])
        parsed_footnotes = "\n".join(footnotes)

        return parsed_title, parsed_body, parsed_objectives, parsed_footnotes


class CutScene(xarc.AbstractScene):
    def __init__(self, reference):
        self.timer: Optional[xarc.EventTimer] = None

        super().__init__(reference)

    def setup(self):
        self.timer = xarc.EventTimer()

    def leave_scene(self, previous_scene: xarc.AbstractScene):
        self.timer.reset()

    def on_update(self, delta_time: float):
        self.timer.tick(delta_time)


class OpeningCutScene(CutScene):
    def __init__(self):
        self.sound: Optional[arc.Sound] = None
        self.sound_player: Optional[arc.sound.media.Player] = None
        # self.background: Optional[arc.Texture] = None
        self.title: Optional[arc.Text] = None
        self.body: Optional[arc.Text] = None
        self.objectives: Optional[arc.Text] = None
        self.footnotes: Optional[arc.Text] = None

        super().__init__(CutSceneList.OPENING)

    def setup(self, *args, **kwargs):
        super().setup()

        self.sound = arc.Sound(asset(AUDIO_THEREISAPATTERN))

        # self.background = arc.load_texture(asset(BACKGROUND_ARBITRARY_3))

        parsed_title, parsed_body, parsed_objectives, parsed_footnotes = _Parser.parse(CUTSCENE_OPENING)
        self.title = arc.Text(parsed_title,
                              xarc.Meta.hz_screen_center(),
                              TITLE_Y(),
                              color=FONT_COLOR,
                              font_name=FONT_NAME,
                              font_size=TITLE_FONT_SIZE,
                              anchor_x="center", anchor_y="center")

        self.body = arc.Text(parsed_body,
                             xarc.Meta.hz_screen_center(),
                             BODY_Y(),
                             color=FONT_COLOR,
                             font_name=FONT_NAME,
                             font_size=BODY_FONT_SIZE,
                             anchor_x="center", anchor_y="center",
                             width=PADDED_SCREEN_WIDTH(),
                             multiline=True,
                             align="center")

        self.objectives = arc.Text(parsed_objectives,
                                   xarc.Meta.hz_screen_center(),
                                   OBJECTIVES_Y(),
                                   color=FONT_COLOR,
                                   font_name=FONT_NAME,
                                   font_size=OBJECTIVES_FONT_SIZE,
                                   anchor_x="center", anchor_y="center",
                                   width=PADDED_SCREEN_WIDTH(),
                                   multiline=True)

        self.footnotes = arc.Text(parsed_footnotes,
                                  xarc.Meta.hz_screen_center(),
                                  FOOTNOTES_Y(),
                                  color=FONT_COLOR,
                                  font_name=FONT_NAME,
                                  font_size=FOOTNOTES_FONT_SIZE,
                                  anchor_x="center", anchor_y="center")

    def enter_scene(self, previous_scene):
        self.sound_player = self.sound.play(loop=True)

    def leave_scene(self, previous_scene: xarc.AbstractScene):
        arc.stop_sound(self.sound_player)

    def draw(self):
        # self.background.draw_scaled(xarc.Meta.hz_screen_center(), xarc.Meta.vt_screen_center())
        self.title.draw()
        self.body.draw()
        self.objectives.draw()
        self.footnotes.draw()

        super().draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arc.key.ESCAPE:
            self.curtains.set_scene(SceneList.MAINMENU)
        else:
            self.curtains.set_scene(SceneList.PLATFORMER)
