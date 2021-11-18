class BulletPerception:
    """
    Perception class of bullet.
    """
    def __init__(self, bullet):
        self.x = bullet.x
        self.y = bullet.y
        self.direction = bullet.direction
        self.team_id = bullet.team_id
        
    def __repr__(self):
        return "<BulletPerception: x={}; y={}; direction={}; team_id={}>".format(
            self.x,
            self.y,
            self.direction,
            self.team_id
        )
