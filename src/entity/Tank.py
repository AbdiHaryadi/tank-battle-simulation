from src.bot.SimpleTankBot import SimpleTankBot
from src.command import *
from src.entity.Bullet import Bullet
from src.enum.BotAction import BotAction
from src.enum.Direction import Direction
from src.perception.TankPerception import TankPerception
from src.utility import color_hex, to_half_dark

class Tank:
    """
    Class for tank.
    """
    TURRET_COORDINATES = {
        Direction.WEST: (4, 12, 16, 20),
        Direction.EAST: (16, 12, 28, 20),
        Direction.NORTH: (12, 4, 20, 16),
        Direction.SOUTH: (12, 16, 20, 28)
    }

    def __init__(self, cv, color, x, y, team_id, bot=None,
            game_config=None):
        self.cv = cv
        self.color = color
        self.x = x
        self.y = y
        self.team_id = team_id
        if bot == None:
            self.bot = SimpleTankBot()
        else:
            self.bot = bot
            
        self.direction = Direction.EAST
        self.game_config = game_config
        
        self.game_row_count = game_config["row_count"]
        self.game_col_count = game_config["col_count"]
        
        self.game_tile_width = game_config["window_width"] / self.game_col_count
        self.game_tile_height = game_config["window_height"] / self.game_row_count
        
        if self.cv != None:
            self.body = self.cv.create_rectangle(
                *self.get_body_coordinates(),
                fill=color_hex(*color),
                width=0
            )
            
            x1, y1, x2, y2 = self.TURRET_COORDINATES[self.direction]
            self.turret = self.cv.create_rectangle(
                *self.get_turret_coordinates(),
                fill=color_hex(*to_half_dark(color)),
                width=0
            )
        else:
            self.body = None
            self.turret = None
    
    def get_body_coordinates(self):
        return (
            self.x * self.game_tile_width + 8,
            self.y * self.game_tile_height + 8,
            self.x * self.game_tile_width + 24,
            self.y * self.game_tile_height + 24
        )
    
    def get_turret_coordinates(self):
        x1, y1, x2, y2 = self.TURRET_COORDINATES[self.direction]
        return (
            self.x * self.game_tile_width + x1,
            self.y * self.game_tile_height + y1,
            self.x * self.game_tile_width + x2,
            self.y * self.game_tile_height + y2,
        )
        
    def destruct(self):
        """
        Visually destruct the tank.
        """
        if self.cv != None:
            self.cv.delete(self.body)
            self.cv.delete(self.turret)
    
    
    def get_action(self, game_perception):
        """
        [Deprecated]
        Get action from bot.
        """
        raise
        return self.bot.get_action(game_perception)
        
    def get_command(self, game_perception, response={}):
        """
        Get command from bot.
        """
        action = self.bot.get_action(game_perception)
        if action is BotAction.MOVE_WEST:
            command = MoveWestCommand(self, game_perception, response)
        elif action is BotAction.MOVE_EAST:
            command = MoveEastCommand(self, game_perception, response)
        elif action is BotAction.MOVE_NORTH:
            command = MoveNorthCommand(self, game_perception, response)
        elif action is BotAction.MOVE_SOUTH:
            command = MoveSouthCommand(self, game_perception, response)
        elif action is BotAction.SHOOT_WEST:
            command = ShootWestCommand(self, game_perception, response)
        elif action is BotAction.SHOOT_EAST:
            command = ShootEastCommand(self, game_perception, response)
        elif action is BotAction.SHOOT_NORTH:
            command = ShootNorthCommand(self, game_perception, response)
        elif action is BotAction.SHOOT_SOUTH:
            command = ShootSouthCommand(self, game_perception, response)
        elif action is BotAction.DO_NOTHING:
            command = DoNothingCommand(self, game_perception, response)
        else:
            raise ValueError("Unknown action: {}".format(action))
            
        return command
                
    def update(self):
        """
        Update canvas object of tank.
        """
        
        if self.cv != None:
            self.cv.coords(
                self.body,
                *self.get_body_coordinates()
            )
            
            x1, y1, x2, y2 = self.TURRET_COORDINATES[self.direction]
            self.cv.coords(
                self.turret,
                *self.get_turret_coordinates()
            )
        
    def get_perception(self):
        """
        Get perception of tank.
        """
        return TankPerception(self)
    
    # Move method
    def move_west(self):
        """
        Move one tile to left (west). Does not move if it hits wall.
        """
        self.turn_west(update=False)
        if self.x > 0:
            self.x -= 1
        self.update()
        
    def move_east(self):
        """
        Move one tile to right (east). Does not move if it hits wall.
        """
        self.turn_east(update=False)
        if self.x < self.game_col_count - 1:
            self.x += 1
        self.update()
        
    def move_north(self):
        """
        Move one tile to up (north). Does not move if it hits wall.
        """
        self.turn_north(update=False)
        if self.y > 0:
            self.y -= 1
        self.update()
        
    def move_south(self):
        """
        Move one tile to down (south). Does not move if it hits wall.
        """
        self.turn_south(update=False)
        if self.y < self.game_row_count - 1:
            self.y += 1
        self.update()
        
    def shoot_west(self):
        """
        Spawn and return one bullet to left (west) direction.
        """
        self.turn_west(update=False)
        self.update()
        return Bullet(self.cv, self.x - 1, self.y, Direction.WEST, self.team_id, color=self.color, game_config=self.game_config)
            
    def shoot_east(self):
        """
        Spawn and return one bullet to right (east) direction.
        """
        self.turn_east(update=False)
        self.update()
        return Bullet(self.cv, self.x + 1, self.y, Direction.EAST, self.team_id, color=self.color, game_config=self.game_config)
        
    def shoot_north(self):
        """
        Spawn and return one bullet to up (north) direction.
        """
        self.turn_north(update=False)
        self.update()
        return Bullet(self.cv, self.x, self.y - 1, Direction.NORTH, self.team_id, color=self.color, game_config=self.game_config)
        
    def shoot_south(self):
        """
        Spawn and return one bullet to down (south) direction.
        """
        self.turn_south(update=False)
        self.update()
        return Bullet(self.cv, self.x, self.y + 1, Direction.SOUTH, self.team_id, color=self.color, game_config=self.game_config)
    
    # Turn method (helper)
    def turn_west(self, update=True):
        """
        Visually turn tank to left (west).
        """
        self.direction = Direction.WEST
        if update:
            self.update()
    
    def turn_east(self, update=True):
        """
        Visually turn tank to right (east).
        """
        self.direction = Direction.EAST
        if update:
            self.update()
        
    def turn_north(self, update=True):
        """
        Visually turn tank to up (north).
        """
        self.direction = Direction.NORTH
        if update:
            self.update()
        
    def turn_south(self, update=True):
        """
        Visually turn tank to south (south).
        """
        self.direction = Direction.SOUTH
        if update:
            self.update()
