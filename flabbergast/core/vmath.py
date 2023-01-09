from typing import Tuple

ORIGIN: Tuple[int, int] = 0, 0


def is_even(x: int) -> bool:
    return x % 2 == 0


def is_odd(x: int) -> bool:
    return x % 2 != 0


def round_up_to_even(x: int) -> int:
    return x if is_even(x) else x + 1


def round_down_to_even(x: int) -> int:
    return x if is_even(x) else x - 1
