import arcade_curtains as arc_curts


class Speed:
    VERY_FAST = 0.5
    FAST = 1
    DEFAULT = 2
    SLOW = 3
    VERY_SLOW = 4


class Scale:
    ONE_HALF = 0.5
    UNITY = 1.0
    THREE_HAVLES = 1.5
    TWICE = 2.0


class Alpha:
    INVISIBLE = 0
    VISIBLE = 255


class Animation:
    DEFAULT_DELTA_INFLATE = 0.05
    DEFAULT_DELTA_DEFLATE = 0.05

    @staticmethod
    def inflate(entity, *args, speed=Speed.FAST, delta=DEFAULT_DELTA_INFLATE):
        entity.animate(duration=speed, scale=entity.scale + delta)

    @staticmethod
    def deflate(entity, *args, speed=Speed.FAST, delta=DEFAULT_DELTA_DEFLATE):
        entity.animate(duration=speed, scale=entity.scale - delta)


class AnimationSequence:
    @staticmethod
    def fade_in(speed=Speed.DEFAULT, callback_func=None):
        sequence = arc_curts.Sequence()
        frames = [
            arc_curts.KeyFrame(alpha=Alpha.INVISIBLE),
            arc_curts.KeyFrame(alpha=Alpha.VISIBLE),
        ]
        for n, frame in enumerate(frames):
            sequence.add_keyframe(n * speed, frame)

        if callback_func is not None:
            func, *args = callback_func
            sequence.add_callback(sequence.total_time, lambda: func(*args))
        return sequence

    @staticmethod
    def fade_in_with_pause(speed=Speed.DEFAULT, callback_func=None):
        sequence = arc_curts.Sequence()
        frames = [
            arc_curts.KeyFrame(alpha=Alpha.INVISIBLE),
            arc_curts.KeyFrame(alpha=Alpha.INVISIBLE),
            arc_curts.KeyFrame(alpha=Alpha.VISIBLE),
        ]
        for n, frame in enumerate(frames):
            sequence.add_keyframe(n * speed, frame)
        if callback_func is not None:
            func, *args = callback_func
            sequence.add_callback(sequence.total_time, lambda: func(*args))
        return sequence

    @staticmethod
    def inflate(begin_scale=Scale.ONE_HALF, end_scale=Scale.UNITY, speed=Speed.DEFAULT, callback_func=None):
        sequence = arc_curts.Sequence()
        frames = [
            arc_curts.KeyFrame(scale=begin_scale),
            arc_curts.KeyFrame(scale=end_scale),
        ]
        for n, frame in enumerate(frames):
            sequence.add_keyframe(n * speed, frame)
        if callback_func is not None:
            func, *args = callback_func
            sequence.add_callback(sequence.total_time, lambda: func(*args))
        return sequence
