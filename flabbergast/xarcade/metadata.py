import arcade as arc


class AtomicData:
    def __init__(self, data):
        self._data = data
        self._initial = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if self._initial is None:
            self._initial = self._data
        self._data = data

    def flush(self):
        self._initial = None

    def stabilize(self):
        if self._initial is not None:
            self._data = self._initial
            self.flush()


class Meta:
    @staticmethod
    def screen_width() -> int:
        return arc.get_window().width

    @staticmethod
    def screen_height() -> int:
        return arc.get_window().height

    @staticmethod
    def screen_size() -> tuple:
        return arc.get_window().get_size()

    @classmethod
    def hz_screen_center(cls) -> float:
        return cls.screen_width() / 2

    @classmethod
    def vt_screen_center(cls) -> float:
        return cls.screen_height() / 2

    @classmethod
    def screen_center(cls) -> tuple:
        return cls.hz_screen_center(), cls.vt_screen_center()
