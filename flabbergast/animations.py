import arcade_curtains as arc_curts


class Alpha:
    INVISIBLE = 0
    VISIBLE = 255


class Delay:
    VERY_SHORT = 0.5
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    VERY_LONG = 4


class Scale:
    DELTA = 0.05
    ONE_HALF = 0.5
    UNITY = 1.0
    THREE_HAVLES = 1.5
    TWICE = 2.0
    THRICE = 3.0


class Speed:
    VERY_FAST = 0.5
    FAST = 1
    DEFAULT = 2
    SLOW = 3
    VERY_SLOW = 4


class Animation:
    @staticmethod
    def animationsequence(frame_sequence):
        def impl(*args, speed=Speed.DEFAULT, callback=None):
            time_frames = frame_sequence(*args)
            sequence = arc_curts.Sequence()
            point_in_time = 0
            for key_frame, span in time_frames:
                sequence.add_keyframe(point_in_time, key_frame)
                if span:
                    point_in_time += span * speed
            if callback is not None:
                func, *args = callback
                sequence.add_callback(sequence.total_time, lambda: func(*args))
            return sequence

        return impl

    @staticmethod
    @animationsequence
    def fade_in():
        return [
            (arc_curts.KeyFrame(alpha=Alpha.INVISIBLE), Delay.SHORT),
            (arc_curts.KeyFrame(alpha=Alpha.VISIBLE), None),
        ]

    @staticmethod
    @animationsequence
    def fade_in_with_pause():
        return [
            (arc_curts.KeyFrame(alpha=Alpha.INVISIBLE), Delay.SHORT),
            (arc_curts.KeyFrame(alpha=Alpha.INVISIBLE), Delay.VERY_SHORT),
            (arc_curts.KeyFrame(alpha=Alpha.VISIBLE), None),
        ]

    @staticmethod
    @animationsequence
    def inflate(begin_scale=Scale.UNITY, end_scale=Scale.UNITY + Scale.DELTA):
        return [
            (arc_curts.KeyFrame(scale=begin_scale), Delay.SHORT),
            (arc_curts.KeyFrame(scale=end_scale), None),
        ]

    @staticmethod
    @animationsequence
    def deflate(begin_scale=Scale.UNITY + Scale.DELTA, end_scale=Scale.UNITY):
        return [
            (arc_curts.KeyFrame(scale=begin_scale), Delay.SHORT),
            (arc_curts.KeyFrame(scale=end_scale), None),
        ]

    @staticmethod
    @animationsequence
    def peek_from_bottom(x, y):
        return [
            (arc_curts.KeyFrame(position=(x, -y)), Delay.VERY_SHORT),
            (arc_curts.KeyFrame(position=(x, y)), Delay.MEDIUM),
            (arc_curts.KeyFrame(position=(x, y)), Delay.VERY_SHORT),
            (arc_curts.KeyFrame(position=(x, -y)), None)
        ]

    @staticmethod
    @animationsequence
    def rotate():
        return [
            (arc_curts.KeyFrame(angle=0), Delay.VERY_SHORT),
            (arc_curts.KeyFrame(angle=360), None)
        ]
