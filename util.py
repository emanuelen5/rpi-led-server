from enum import IntEnum, Enum
import time


class KeyCode(IntEnum):
    RIGHT_ARROW = 65363
    LEFT_ARROW = 65361
    UP_ARROW = 65362
    DOWN_ARROW = 65364

    def __repr__(self):
        return self.name


def max_update_rate(update_rate: float = 1.0):
    def wrapper(f):
        f.last_update_time = 0

        def cache_wrapper(*args, **kwargs):
            now = time.time()
            if now - f.last_update_time > update_rate:
                f.cached_value = f(*args, **kwargs)
                f.last_update_time = now
            return f.cached_value

        return cache_wrapper

    return wrapper


def cycle_enum(enum_value: Enum, forwards: bool = True):
    """
    Gets the consecutive value in the Enum's class
    :param enum_value: An instance of an Enum class
    :param forwards: Whether to get the next or previous enum value
    :return: A neighboring Enum value
    """
    cls = enum_value.__class__
    enums = list(cls)
    idx = enums.index(enum_value)
    if forwards:
        idx_new = (idx + 1) % len(cls)
    else:
        idx_new = (idx - 1) % len(cls)
    return enums[idx_new]
