from enum import Enum, auto

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    
    def inverse(self):
        if self is Direction.LEFT:
            return Direction.RIGHT
            
        elif self is Direction.RIGHT:
            return Direction.LEFT
            
        elif self is Direction.UP:
            return Direction.DOWN
            
        elif self is Direction.DOWN:
            return Direction.UP
            
    def norm_vector(self):
        # Return normal vector relative to the coordinate of window
        if self is Direction.LEFT:
            return (-1, 0)
            
        elif self is Direction.RIGHT:
            return (1, 0)
            
        elif self is Direction.UP:
            return (0, -1)
            
        elif self is Direction.DOWN:
            return (0, 1)
