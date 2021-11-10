import random

import config
from utility import color_hex, to_half_dark
from Action import Action
from Bullet import Bullet
from Direction import Direction
from TankPerception import TankPerception
from SimpleTankBot import SimpleTankBot

class Tank:
    TURRET_COORDINATES = {
        Direction.LEFT: (4, 12, 16, 20),
        Direction.RIGHT: (16, 12, 28, 20),
        Direction.UP: (12, 4, 20, 16),
        Direction.DOWN: (12, 16, 20, 28)
    }

    def __init__(self, cv, color, x, y, bot=None):
        self.cv = cv
        self.color = color
        self.x = x
        self.y = y
        if bot == None:
            self.bot = SimpleTankBot()
        else:
            self.bot = bot
            
        self.direction = Direction.RIGHT
        
        if self.cv != None:
            self.body = self.cv.create_rectangle(
                x * config.TILE_WIDTH + 8,
                y * config.TILE_HEIGHT + 8,
                x * config.TILE_WIDTH + 24,
                y * config.TILE_HEIGHT + 24,
                fill=color_hex(*color),
                width=0
            )
            
            x1, y1, x2, y2 = self.TURRET_COORDINATES[self.direction]
            self.turret = self.cv.create_rectangle(
                x * config.TILE_WIDTH + x1,
                y * config.TILE_HEIGHT + y1,
                x * config.TILE_WIDTH + x2,
                y * config.TILE_HEIGHT + y2,
                fill=color_hex(*to_half_dark(color)),
                width=0
            )
        else:
            self.body = None
            self.turret = None
        
    def destruct(self):
        if self.cv != None:
            self.cv.delete(self.body)
            self.cv.delete(self.turret)
    
    def get_action(self, game_perception):
        return self.bot.get_action(game_perception)
                
    def update(self):
        if self.cv != None:
            self.cv.coords(
                self.body,
                self.x * config.TILE_WIDTH + 8,
                self.y * config.TILE_HEIGHT + 8,
                self.x * config.TILE_WIDTH + 24,
                self.y * config.TILE_HEIGHT + 24,
            )
            
            x1, y1, x2, y2 = self.TURRET_COORDINATES[self.direction]
            self.cv.coords(
                self.turret,
                self.x * config.TILE_WIDTH + x1,
                self.y * config.TILE_HEIGHT + y1,
                self.x * config.TILE_WIDTH + x2,
                self.y * config.TILE_HEIGHT + y2,
            )
        
    def get_perception(self):
        return TankPerception(self)
    
    # Move method
    def move_left(self):
        self.turn_left(update=False)
        if self.x > 0:
            self.x -= 1
        self.update()
        
    def move_right(self):
        self.turn_right(update=False)
        if self.x < config.COL_COUNT - 1:
            self.x += 1
        self.update()
        
    def move_up(self):
        self.turn_up(update=False)
        if self.y > 0:
            self.y -= 1
        self.update()
        
    def move_down(self):
        self.turn_down(update=False)
        if self.y < config.ROW_COUNT - 1:
            self.y += 1
        self.update()
        
    def shoot_left(self):
        self.turn_left(update=False)
        self.update()
        return Bullet(self.cv, self.x - 1, self.y, Direction.LEFT)
            
    def shoot_right(self):
        self.turn_right(update=False)
        self.update()
        return Bullet(self.cv, self.x + 1, self.y, Direction.RIGHT)
        
    def shoot_up(self):
        self.turn_up(update=False)
        self.update()
        return Bullet(self.cv, self.x, self.y - 1, Direction.UP)
        
    def shoot_down(self):
        self.turn_down(update=False)
        self.update()
        return Bullet(self.cv, self.x, self.y + 1, Direction.DOWN)
    
    # Turn method (helper)
    def turn_left(self, update=True):
        self.direction = Direction.LEFT
        if update:
            self.update()
    
    def turn_right(self, update=True):
        self.direction = Direction.RIGHT
        if update:
            self.update()
        
    def turn_up(self, update=True):
        self.direction = Direction.UP
        if update:
            self.update()
        
    def turn_down(self, update=True):
        self.direction = Direction.DOWN
        if update:
            self.update()
