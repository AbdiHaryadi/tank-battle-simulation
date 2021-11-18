class TankPerception:
    """
    Perception class of tank.
    """
    def __init__(self, tank):
        self.x = tank.x
        self.y = tank.y
        
    def __repr__(self):
        return "<TankPerception: x={}; y={}>".format(
            self.x,
            self.y
        )
