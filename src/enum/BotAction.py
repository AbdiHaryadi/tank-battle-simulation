from enum import Enum, auto

class BotAction(Enum):
    """
    Enumeration type of action.
    """
    MOVE_WEST = auto()
    MOVE_EAST = auto()
    MOVE_NORTH = auto()
    MOVE_SOUTH = auto()
    SHOOT_WEST = auto()
    SHOOT_EAST = auto()
    SHOOT_NORTH = auto()
    SHOOT_SOUTH = auto()
    DO_NOTHING = auto()
