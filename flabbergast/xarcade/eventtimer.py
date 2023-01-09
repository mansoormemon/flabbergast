from typing import Callable, Dict, Tuple

SECONDS_IN_MINUTE: int = 60


class _Event:
    def __init__(self, func: Callable, trigger_once: bool = True, *args, **kwargs):
        self._func: Callable = func
        self._trigger_once = trigger_once
        self._args = args
        self._kwargs = kwargs
        self._triggered: bool = False

    def trigger(self):
        if not self._triggered or not self._trigger_once:
            self._triggered = True
            self._func(*self._args, **self._kwargs)

    def reset(self):
        self._triggered = False


class EventTimer:
    def __init__(self):
        self._elapsed_time: float = 0.0
        self._schedule: Dict[Tuple[int, int], _Event] = {}

    def tick(self, delta_time: float):
        self._elapsed_time += delta_time

        time: Tuple[int, int] = self.minutes(), self.seconds()
        if time in self._schedule:
            self._schedule[time].trigger()

    def minutes(self) -> int:
        return int(self._elapsed_time) // SECONDS_IN_MINUTE

    def seconds(self) -> int:
        return int(self._elapsed_time) % SECONDS_IN_MINUTE

    def reset(self):
        self._elapsed_time = 0.0
        for event in self._schedule.values():
            event.reset()

    def register_event(self, time: Tuple[int, int], func: Callable, trigger_once: bool = True, *args, **kwargs):
        self._schedule[time] = _Event(func, trigger_once, *args, **kwargs)
