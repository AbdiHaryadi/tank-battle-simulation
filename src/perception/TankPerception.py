class TankPerception:
    """
    Perception class of tank.
    """
    def __init__(self, tank):
        self.x = tank.x
        self.y = tank.y
        self.team_id = tank.team_id
        
    def __repr__(self):
        return "<TankPerception: x={}; y={}; team_id={}>".format(
            self.x,
            self.y,
            self.team_id
        )
