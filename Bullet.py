import config
from utility import color_hex
from Direction import Direction
from BulletPerception import BulletPerception

class Bullet:
    def __init__(self, cv, x, y, direction, color=(255, 127, 0)):
        self.cv = cv
        self.color = color
        self.x = x
        self.y = y
        self.direction = direction
        if self.cv != None:
            if (direction is Direction.LEFT) or (direction is Direction.RIGHT):
                self.bullet = self.cv.create_rectangle(
                    self.x * config.TILE_WIDTH + 8,
                    self.y * config.TILE_HEIGHT + 15,
                    self.x * config.TILE_WIDTH + 24,
                    self.y * config.TILE_HEIGHT + 17,
                    fill=color_hex(*color),
                    width=0)
            elif (direction is Direction.UP) or (direction is Direction.DOWN):
                self.bullet = self.cv.create_rectangle(
                    self.x * config.TILE_WIDTH + 15,
                    self.y * config.TILE_HEIGHT + 8,
                    self.x * config.TILE_WIDTH + 17,
                    self.y * config.TILE_HEIGHT + 24,
                    fill=color_hex(*color),
                    width=0)
            else:
                print("Unknown", direction)
                raise ValueError
        else:
            self.bullet = None
                
    def move(self):
        dx, dy = self.direction.norm_vector()
        self.x += dx
        self.y += dy
        self.update()
        
    def update(self):
        if self.cv != None:
            if (self.direction is Direction.LEFT) or (self.direction is Direction.RIGHT):
                self.cv.coords(
                    self.bullet,
                    self.x * config.TILE_WIDTH + 8,
                    self.y * config.TILE_HEIGHT + 15,
                    self.x * config.TILE_WIDTH + 24,
                    self.y * config.TILE_HEIGHT + 17,
                )
            elif (self.direction is Direction.UP) or (self.direction is Direction.DOWN):
                self.cv.coords(
                    self.bullet,
                    self.x * config.TILE_WIDTH + 15,
                    self.y * config.TILE_HEIGHT + 8,
                    self.x * config.TILE_WIDTH + 17,
                    self.y * config.TILE_HEIGHT + 24,
                )
            
    def destruct(self):
        if self.cv != None:
            self.cv.delete(self.bullet)
        
    def get_perception(self):
        return BulletPerception(self)
