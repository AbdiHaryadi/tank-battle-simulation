class BulletPerception:
    """
    Perception class of bullet.
    """
    def __init__(self, bullet):
        self.x = bullet.x
        self.y = bullet.y
        self.direction = bullet.direction
        
    def __repr__(self):
        return "<BulletPerception: x={}; y={}; direction={}>".format(
            self.x,
            self.y,
            self.direction
        )
