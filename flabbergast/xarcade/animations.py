from typing import Callable, Iterable, Optional

import arcade_curtains as arc_curts


class Alpha:
    INVISIBLE: int = 0
    VISIBLE: int = 255


class Delay:
    VERY_SHORT: float = 0.5
    SHORT: float = 1.0
    MEDIUM: float = 2.0
    LONG: float = 3.0
    VERY_LONG: float = 4.0


class Scale:
    DELTA: float = 0.05
    ONE_HALF: float = 0.5
    UNITY: float = 1.0
    THREE_HAVLES: float = 1.5
    TWICE: float = 2.0
    THRICE: float = 3.0


class Speed:
    VERY_FAST: float = 0.5
    FAST: float = 1.0
    DEFAULT: float = 2.0
    SLOW: float = 3.0
    VERY_SLOW: float = 4.0


class Animation:
    @staticmethod
    def animationsequence(frame_sequence: Callable) -> Callable:
        def impl(*args, speed: float = Speed.DEFAULT, callback: Optional[Callable] = None) -> arc_curts.Sequence:
            time_frames: Iterable = frame_sequence(*args)
            sequence: arc_curts.Sequence = arc_curts.Sequence()
            point_in_time: float = 0.0
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
    @animationsequence.__get__(object)
    def fade_in() -> arc_curts.Sequence:
        return [
            (arc_curts.KeyFrame(alpha=Alpha.INVISIBLE), Delay.SHORT),
            (arc_curts.KeyFrame(alpha=Alpha.VISIBLE), None),
        ]

    @staticmethod
    @animationsequence.__get__(object)
    def fade_in_with_delay() -> arc_curts.Sequence:
        return [
            (arc_curts.KeyFrame(alpha=Alpha.INVISIBLE), Delay.SHORT),
            (arc_curts.KeyFrame(alpha=Alpha.INVISIBLE), Delay.VERY_SHORT),
            (arc_curts.KeyFrame(alpha=Alpha.VISIBLE), None),
        ]

    @staticmethod
    @animationsequence.__get__(object)
    def inflate(begin_scale: float = Scale.UNITY, end_scale: float = Scale.UNITY + Scale.DELTA) -> arc_curts.Sequence:
        return [
            (arc_curts.KeyFrame(scale=begin_scale), Delay.SHORT),
            (arc_curts.KeyFrame(scale=end_scale), None),
        ]

    @staticmethod
    @animationsequence.__get__(object)
    def deflate(begin_scale: float = Scale.UNITY + Scale.DELTA, end_scale: float = Scale.UNITY) -> arc_curts.Sequence:
        return [
            (arc_curts.KeyFrame(scale=begin_scale), Delay.SHORT),
            (arc_curts.KeyFrame(scale=end_scale), None),
        ]

    @staticmethod
    @animationsequence.__get__(object)
    def peek_from_bottom(x: float, y: float) -> arc_curts.Sequence:
        return [
            (arc_curts.KeyFrame(position=(x, -y)), Delay.VERY_SHORT),
            (arc_curts.KeyFrame(position=(x, y)), Delay.MEDIUM),
            (arc_curts.KeyFrame(position=(x, y)), Delay.VERY_SHORT),
            (arc_curts.KeyFrame(position=(x, -y)), None)
        ]
