from BulletPerception import BulletPerception
from TankPerception import TankPerception
from Direction import Direction

class GamePerception:
    def __init__(self, row_count, col_count, frame, player_tank, bullets,
            other_tanks):
        # row_count: number of row in game (valid row: 0..(row_count - 1))
        # col_count: number of column in game (valid column: 0..(row_count - 1))
        # frame: number of current frame, used as time
        # player_tank: your own Tank
        # bullets: list of all Bullet objects
        # other_tanks: list of all Tank objects not include your Tank
        
        # first row is on the top side (so it is top to bottom)
        # first column is on the left side (so it is left to right)
        
        self.row_count = row_count
        self.col_count = col_count
        self.frame = frame
        self.player_tank = TankPerception(player_tank) if player_tank != None else None
        self.bullets = [BulletPerception(b) for b in bullets]
        self.other_tanks = [TankPerception(t) for t in other_tanks]
        
    def __repr__(self):
        return (
            "<GamePerception: frame={}; player_tank={}; bullets={}; other_tanks={}>".format(
                self.frame, self.player_tank, self.bullets, self.other_tanks
            )
        )
        
    def render(self):
        # Print game perception as a display in command line
        print("#" * (self.col_count + 2))
        objects = self.bullets + self.other_tanks
        if self.player_tank != None:
            objects += [self.player_tank]
        objects.sort(key=lambda o: o.y * self.col_count + o.x)
        
        i = 0 # object index
        len_objects = len(objects)
        for r in range(self.row_count):
            print("#", end="")
            for c in range(self.col_count):
                if i == len_objects:
                    print(".", end="")
                else:
                    if objects[i].x == c and objects[i].y == r:
                        if objects[i] is self.player_tank:
                            # This is the your (player) tank
                            print("P", end="")
                            
                        elif isinstance(objects[i], BulletPerception):
                            if objects[i].direction is Direction.LEFT:
                                print("-", end="")
                            elif objects[i].direction is Direction.RIGHT:
                                print("-", end="")
                            elif objects[i].direction is Direction.UP:
                                print("|", end="")
                            elif objects[i].direction is Direction.DOWN:
                                print("|", end="")
                            else:
                                print("Error: unknown direction")
                                print(objects[i].direction)
                                raise ValueError
                            
                        elif isinstance(objects[i], TankPerception):
                            # This is the other tank
                            print("O", end="")
                            
                        else:
                            print("Error: unknown object")
                            print(objects[i])
                            raise ValueError
                            
                        # Go to next object which is different coordinate
                        while objects[i].x == c and objects[i].y == r and i < len_objects - 1:
                            i += 1
                            
                        if objects[i].x == c and objects[i].y == r:
                            i += 1 # Last index
                        
                    else:
                        print(".", end="")
                    
            print("#") # with newline
        print("#" * (self.col_count + 2))
