import arcade as arc
import arcade_curtains as arc_curts

from flabbergast import curtainscene
from flabbergast import dataproxy
from flabbergast import mainmenu
from flabbergast import platformer
from flabbergast import settingspane


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
                curtainscene.Reference.MAINMENU: mainmenu.Scene(),
                curtainscene.Reference.PLATFORMER: platformer.Scene(),
                curtainscene.Reference.SETTINGSPANE: settingspane.Scene()
            }
        )

    def load_n_apply_configurations(self):
        dataproxy.Configuration.load()
        self.set_caption(dataproxy.Configuration.screen_title())
        self.set_fullscreen(dataproxy.Configuration.fullscreen())

    @staticmethod
    def load_metadata():
        dataproxy.Meta.load()

    @staticmethod
    def load_userdata():
        dataproxy.User.load()

    def setup(self):
        self._curtains.set_scene(curtainscene.Reference.MAINMENU)

    def launch(self):
        self.setup()
        self.run()
