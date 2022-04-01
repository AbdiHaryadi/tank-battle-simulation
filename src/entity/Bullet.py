from src.enum.Direction import Direction
from src.perception.BulletPerception import BulletPerception
from src.utility import color_hex

class Bullet:
    """
    Class for bullet.
    """
    def __init__(self, cv, x, y, direction, team_id=None, color=(255, 127, 0),
            game_config=None):
        self.cv = cv
        self.color = color
        self.x = x
        self.y = y
        self.direction = direction
        self.team_id = team_id
        
        row_count = game_config["row_count"]
        col_count = game_config["col_count"]
        
        self.game_tile_width = game_config["window_width"] / col_count
        self.game_tile_height = game_config["window_height"] / row_count
        
        if self.cv != None:
            self.bullet = self.cv.create_rectangle(
                *self.get_bullet_coordinates(),
                fill=color_hex(*color),
                width=0
            )
        else:
            self.bullet = None
            
    def get_bullet_coordinates(self):
        if (self.direction is Direction.LEFT) or (self.direction is Direction.RIGHT):
            return (
                self.x * self.game_tile_width + 8,
                self.y * self.game_tile_height + 15,
                self.x * self.game_tile_width + 24,
                self.y * self.game_tile_height + 17
            )
        elif (self.direction is Direction.UP) or (self.direction is Direction.DOWN):
            return (
                self.x * self.game_tile_width + 15,
                self.y * self.game_tile_height + 8,
                self.x * self.game_tile_width + 17,
                self.y * self.game_tile_height + 24
            )
        else:
            print("Unknown", self.direction)
            raise ValueError
                
    def move(self):
        """
        Move one step to its direction.
        """
        dx, dy = self.direction.norm_vector()
        self.x += dx
        self.y += dy
        self.update()
        
    def update(self):
        """
        Update canvas object of bullet.
        """
        if self.cv != None:
            self.cv.coords(self.bullet, *self.get_bullet_coordinates())
            
    def destruct(self):
        """
        Visually destruct the bullet.
        """
        if self.cv != None:
            self.cv.delete(self.bullet)
        
    def get_perception(self):
        """
        Get perception of bullet.
        """
        return BulletPerception(self)
