import arcade as arc
import arcade_curtains as arc_curts

from flabbergast.level import *
from flabbergast.mainmenu import *
from flabbergast.metadata import *
from flabbergast.scenes import *
from flabbergast.settingsmenu import *


class Data:
    def __init__(self):
        pass


class Flabbergast(arc.Window):
    def __init__(self):
        super().__init__()

        # Load prerequisites.
        # Load order should not be changed.
        self.load_configurations()
        self.load_metadata()
        self.load_assets()

        # Prepare fields.
        self._curtains = arc_curts.Curtains(self)
        self._curtains.add_scenes(
            {
                Scene.MAIN_MENU: MainMenu(),
                Scene.LEVEL: Level(),
                Scene.SETTINGS: SettingsMenu(),
            }
        )

        self._data = Data()

    def load_configurations(self):
        self.set_caption(get_config("SCREEN_TITLE"))
        self.set_fullscreen(get_config("IS_FULLSCREEN", bool))

    def load_metadata(self):
        Metadata.load()

    def load_assets(self):
        arc.load_font(assets(FONT_PRESS_START_2P))
        arc.load_font(assets(FONT_SILKSCREEN))
        arc.load_font(assets(FONT_TEKTON))

    def setup(self):
        self._curtains.set_scene(Scene.MAIN_MENU)

    def launch(self):
        self.setup()
        self.run()
