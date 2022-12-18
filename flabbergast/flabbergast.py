from enum import Enum

from flabbergast.level import *
from flabbergast.mainmenu import *
from flabbergast.settingsmenu import *


class Flabbergast(arc.Window):
    class ConfigurationList(Enum):
        SCREEN_TITLE = 0
        IS_FULLSCREEN = 1

    def __init__(self):
        super().__init__()

        # Load prerequisites.
        # Load order should not be changed.
        self.load_configurations()
        self.load_metadata()

        # Prepare fields.
        self._curtains = arc_curts.Curtains(self)
        self._curtains.add_scenes(
            {
                Scene.MAIN_MENU: MainMenu(),
                Scene.LEVEL: Level(),
                Scene.SETTINGS: SettingsMenu()
            }
        )

    def load_configurations(self):
        self.set_caption(get_config(self.ConfigurationList.SCREEN_TITLE.name))
        self.set_fullscreen(get_config(self.ConfigurationList.IS_FULLSCREEN.name, bool))

    def load_metadata(self):
        Metadata.load()

    def setup(self):
        self._curtains.set_scene(Scene.MAIN_MENU)

    def launch(self):
        self.setup()
        self.run()
