class TankPerception:
    def __init__(self, tank):
        self.x = tank.x
        self.y = tank.y
        self.direction = tank.direction
        
    def __repr__(self):
        return "<TankPerception: x={}; y={}; direction={}>".format(
            self.x,
            self.y,
            self.direction
        )
