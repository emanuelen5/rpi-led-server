from enum import IntEnum


class KeyCode(IntEnum):
    RIGHT_ARROW = 65363
    LEFT_ARROW = 65361
    UP_ARROW = 65362
    DOWN_ARROW = 65364

    def __repr__(self):
        return self.name
