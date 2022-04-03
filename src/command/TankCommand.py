class TankCommand:
    """
    TankCommand is an unimplemented-execute task for tank command.
    """
    def __init__(self, tank, gp, response={}):
        self.tank = tank
        self.gp = gp
        self.response = response
        
    def execute(self):
        raise NotImplementedError