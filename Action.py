from enum import Enum, auto

class Action(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    SHOOT_LEFT = auto()
    SHOOT_RIGHT = auto()
    SHOOT_UP = auto()
    SHOOT_DOWN = auto()
    DO_NOTHING = auto()
