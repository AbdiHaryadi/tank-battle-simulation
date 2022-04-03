from enum import Enum, auto

class Direction(Enum):
    """
    Enumeration type of direction.
    """
    WEST = auto()
    EAST = auto()
    NORTH = auto()
    SOUTH = auto()
    
    def inverse(self):
        """
        Return inverse of the direction.
        """
        if self is Direction.WEST:
            return Direction.EAST
            
        elif self is Direction.EAST:
            return Direction.WEST
            
        elif self is Direction.NORTH:
            return Direction.SOUTH
            
        elif self is Direction.SOUTH:
            return Direction.NORTH
            
    def norm_vector(self):
        """
        Return vector with form of tuple (x, y).
        Positive-x goes right and positive-y goes down.
        """
        # Return normal vector relative to the coordinate of window
        if self is Direction.WEST:
            return (-1, 0)
            
        elif self is Direction.EAST:
            return (1, 0)
            
        elif self is Direction.NORTH:
            return (0, -1)
            
        elif self is Direction.SOUTH:
            return (0, 1)
