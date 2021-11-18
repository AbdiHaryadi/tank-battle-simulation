import tkinter
import random
from math import exp

from src.bot.SimpleTankBot import SimpleTankBot
from src.bot.MyTankBot import MyTankBot
import src.config as config
from src.entity.Bullet import Bullet
from src.entity.Tank import Tank
from src.enum.Action import Action
from src.enum.Direction import Direction
from src.perception.GamePerception import GamePerception

class App(tkinter.Tk):
    """
    Class for main application.
    """
    RANDOM_BULLET_RATE = 0.001
    BG_COLOR_1 = "#d0e19c"
    BG_COLOR_2 = "#b5d55e"

    def __init__(self, mode="1v1"):
        super().__init__()
        self.title("AI Simulation")
        self.canvas = tkinter.Canvas(
            self, # the window itself
            width=config.WIDTH,
            height=config.HEIGHT
        )
        self.canvas.pack() # make the window fit to canvas
        self.tanks = []
        self.bullets = []
        self.frame = 0
        self.mode = mode
        
    def run(self):
        # Create a checkerboard background
        self.canvas.create_rectangle(
            0, 0,                          # from top-left coordinate
            config.WIDTH, config.HEIGHT,   # to bottom-right coordinate
            fill=self.BG_COLOR_1,
            width=0                        # no border
        )
        
        for r in range(config.ROW_COUNT):
            for c in range(config.COL_COUNT):
                if (r + c) % 2 == 0:
                    self.canvas.create_rectangle(
                        c * config.TILE_WIDTH,
                        r * config.TILE_HEIGHT,
                        (c + 1) * config.TILE_WIDTH,
                        (r + 1) * config.TILE_HEIGHT,
                        fill=self.BG_COLOR_2,
                        width=0
                    )

        """
        # Create random tanks
        while len(self.tanks) < 2:
            x = random.randrange(0, config.COL_COUNT)
            y = random.randrange(0, config.ROW_COUNT)
            if not any(map(lambda t: t.x == x and t.y == y, self.tanks)):
                random_color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
                new_tank = Tank(self.canvas, random_color, x, y)
                self.tanks.append(new_tank)
        """
        
        if self.mode == "1v1":
            #######
            # Put your bot here!
            t1 = Tank(self.canvas, (255, 0, 0), 0, 0, "RED TEAM", bot=MyTankBot())
            t2 = Tank(self.canvas, (0, 0, 255), config.COL_COUNT - 1, config.ROW_COUNT - 1, "BLUE TEAM", bot=SimpleTankBot())
            self.tanks = [t1, t2]
            #######
        elif self.mode == "3v3":
            tr1 = Tank(self.canvas, (255, 0, 0), 0, 0, "RED TEAM", bot=SimpleTankBot())
            tr2 = Tank(self.canvas, (255, 127, 0), 0, (config.ROW_COUNT - 1) // 2, "RED TEAM", bot=SimpleTankBot())
            tr3 = Tank(self.canvas, (255, 0, 127), 0, config.ROW_COUNT - 1, "RED TEAM", bot=SimpleTankBot())
            tb1 = Tank(self.canvas, (0, 0, 255), config.COL_COUNT - 1, 0, "BLUE TEAM", bot=SimpleTankBot())
            tb2 = Tank(self.canvas, (0, 127, 255), config.COL_COUNT - 1, (config.ROW_COUNT - 1) // 2, "BLUE TEAM", bot=SimpleTankBot())
            tb3 = Tank(self.canvas, (63, 127, 255), config.COL_COUNT - 1, config.ROW_COUNT - 1, "BLUE TEAM", bot=SimpleTankBot())
            self.tanks = [tr1, tr2, tr3, tb1, tb2, tb3]
        else:
            raise ValueError("Mode not supported: {}".format(self.mode))

        self.after(config.MS_DELAY, self.update)
        self.mainloop()
        
    def update(self):
        # Shuffle the tank for fair chance
        random.shuffle(self.tanks)
        
        # Get action of every tanks
        new_bullets = []
        same_pos = lambda x1, y1, x2, y2: x1 == x2 and y1 == y2
        for t in self.tanks:
            # Get action; dictionaries are used so action cannot change the state of tanks and bullets
            action = t.get_action(GamePerception(
                config.ROW_COUNT,
                config.COL_COUNT,
                self.frame,
                t,
                self.bullets,
                [t2 for t2 in self.tanks if t2 != t] # other tanks
            ))
            
            if action is Action.MOVE_LEFT:
                if not any(map(lambda t2: same_pos(t.x - 1, t.y, t2.x, t2.y) and t2 != t, self.tanks)):
                    t.move_left()
            elif action is Action.MOVE_RIGHT:
                if not any(map(lambda t2: same_pos(t.x + 1, t.y, t2.x, t2.y) and t2 != t, self.tanks)):
                    t.move_right()
            elif action is Action.MOVE_UP:
                if not any(map(lambda t2: same_pos(t.x, t.y - 1, t2.x, t2.y) and t2 != t, self.tanks)):
                    t.move_up()
            elif action is Action.MOVE_DOWN:
                if not any(map(lambda t2: same_pos(t.x, t.y + 1, t2.x, t2.y) and t2 != t, self.tanks)):
                    t.move_down()
            elif action is Action.SHOOT_LEFT:
                bullet = t.shoot_left()
                new_bullets.append(bullet)
            elif action is Action.SHOOT_RIGHT:
                bullet = t.shoot_right()
                new_bullets.append(bullet)
            elif action is Action.SHOOT_UP:
                bullet = t.shoot_up()
                new_bullets.append(bullet)
            elif action is Action.SHOOT_DOWN:
                bullet = t.shoot_down()
                new_bullets.append(bullet)
            elif action is Action.DO_NOTHING:
                pass # do nothing
            else:
                print("Unknown action: {}".format(action))
            # else: no action
        
        removed_bullets = []
        
        # Destroy the tank which get hitted by old bullet before move
        # and not in the same way
        for b in self.bullets:
            # Assume one bullet for one tank
            destroyed_tank = None
            for t in self.tanks:
                if (same_pos(t.x, t.y, b.x, b.y)
                        and t.direction is b.direction.inverse()):
                    if t.team_id != b.team_id:
                        destroyed_tank = t
                    # else: it is a friendly fire, tank does not destroyed
                    removed_bullets.append(b)
                    
                    # We have got the destroyed tank, go to next step
                    break
                    
                # else: find another tank
                    
            if destroyed_tank != None:
                self.tanks.remove(destroyed_tank)
                destroyed_tank.destruct()
        
        # Update old bullet position 
        for b in self.bullets:
            b.move()
        
        # Add the new bullets
        self.bullets += new_bullets
        
        # Remove the bullet which is out of bound
        for b in self.bullets:
            if not (b.x >= 0 and b.x < config.COL_COUNT and b.y >= 0 and b.y < config.ROW_COUNT):
                removed_bullets.append(b)
        
        # Destroy the tank which get hitted after all old bullet move
        # and new bullet added
        for b in self.bullets:
            # Assume one bullet for one tank
            destroyed_tank = None
            for t in self.tanks:
                if t.x == b.x and t.y == b.y:
                    if t.team_id != b.team_id:
                        destroyed_tank = t
                    # else: it is a friendly fire, tank does not destroyed
                    removed_bullets.append(b)
                    
                    # We have got the destroyed tank, go to next step
                    break
                    
                # else: find another tank
                    
            if destroyed_tank != None:
                self.tanks.remove(destroyed_tank)
                destroyed_tank.destruct()
                
        for b in removed_bullets:
            self.bullets.remove(b)
            b.destruct()
        
        if len(set(map(lambda t: t.team_id, self.tanks))) > 1:
            # Spawn random bullet, increasing rate each time
            p = 1 - exp(-self.frame * self.RANDOM_BULLET_RATE)
            while random.random() < p:
                bullet_added = False
                while not bullet_added:
                    direction = random.choice(list(Direction))
                    if direction == Direction.LEFT:
                        x = config.COL_COUNT - 1
                        y = random.randrange(0, config.ROW_COUNT)
                    elif direction == Direction.RIGHT:
                        x = 0
                        y = random.randrange(0, config.ROW_COUNT)
                    elif direction == Direction.UP:
                        x = random.randrange(0, config.COL_COUNT)
                        y = config.ROW_COUNT - 1
                    elif direction == Direction.DOWN:
                        x = random.randrange(0, config.COL_COUNT)
                        y = 0
                    else:
                        print(direction, "what?")
                        raise ValueError
                    
                    if not any(list(map(lambda t: t.x == x and t.y == y, self.tanks))):
                        self.bullets.append(Bullet(self.canvas, x, y, direction, color=(71, 63, 63)))
                        bullet_added = True
                    # else: player exists there, so do not spawn bullet there.
        
        self.frame += 1
        self.after(config.MS_PER_FRAME, self.update)

if __name__ == "__main__":
    app = App()
    app.run()
