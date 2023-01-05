import arcade as arc
import arcade_curtains as arc_curts

from .cutscene import CutScene
from .dataproxy import Configuration, Meta, User
from .loadingscreen import LoadingScreen
from .mainmenu import MainMenu
from .platformer import Platformer
from .references import SceneList
from .settingspane import SettingsPane


class Flabbergast(arc.Window):
    def __init__(self):
        super().__init__()

        # Load prerequisites.
        # Load order should not be changed.
        self.load_n_apply_configurations()
        self.load_metadata()
        self.load_userdata()

        # Prepare fields.
        self._curtains = arc_curts.Curtains(self)
        self._curtains.add_scenes(
            {
                SceneList.MAINMENU: MainMenu(),
                SceneList.CUTSCENE: CutScene(),
                SceneList.PLATFORMER: Platformer(),
                SceneList.SETTINGSPANE: SettingsPane(),
                SceneList.LOADINGSCREEN: LoadingScreen(),
            }
        )

    def load_n_apply_configurations(self):
        Configuration()
        self.set_caption(Configuration.screen_title())
        self.set_fullscreen(Configuration.fullscreen())

    @staticmethod
    def load_metadata():
        Meta()

    @staticmethod
    def load_userdata():
        User()

    def setup(self):
        self._curtains.set_scene(SceneList.LOADINGSCREEN)

    def on_update(self, delta_time):
        self._curtains.current_scene.on_update(delta_time)

    def launch(self):
        self.setup()
        self.run()
