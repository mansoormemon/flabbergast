from abc import ABC

import arcade_curtains as arc_curts


class AbstractScene(arc_curts.BaseScene, ABC):
    def __init__(self, reference, *args, **kwargs):
        self._reference = reference

        super().__init__(*args, **kwargs)

    def get_reference(self):
        return self._reference

    def get_reference_name(self):
        return self._reference.name

    def get_reference_key(self):
        return self._reference.name.lower()

    def on_update(self, delta_time):
        pass
