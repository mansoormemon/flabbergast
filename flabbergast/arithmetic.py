ORIGIN = 0, 0


def center(x):
    return x / 2


def half(x):
    return x / 2


def is_even(x):
    return x % 2 == 0


def is_odd(x):
    return x % 2 != 0


def round_up_to_even(x):
    return x if is_even(x) else x + 1


def round_down_to_even(x):
    return x if is_even(x) else x - 1
