import arcade as arc


class Animation:
    DEFAULT_DELTA_INFLATE_DEFLATE = 0.05

    @staticmethod
    def inflate(entity: arc.Sprite, *args, delta=DEFAULT_DELTA_INFLATE_DEFLATE):
        entity.animate(duration=1, scale=entity.scale + delta)

    @staticmethod
    def deflate(entity, *args, delta=DEFAULT_DELTA_INFLATE_DEFLATE):
        entity.animate(duration=1, scale=entity.scale - delta)
