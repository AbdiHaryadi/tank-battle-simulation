import random
from math import exp

import config
from Action import Action
from Bullet import Bullet
from Direction import Direction
from GamePerception import GamePerception
from Tank import Tank
from SimpleTankBot import SimpleTankBot
from MyTankBot import MyTankBot

import time

class CommandLineApp():
    RANDOM_BULLET_RATE = 0.001
    def __init__(self):
        self.tanks = []
        self.bullets = []
        self.frame = 0
        
    def run(self):
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
                new_tank = Tank(None, random_color, x, y)
                self.tanks.append(new_tank)
        """
        
        t1 = Tank(None, (255, 0, 0), 0, 0, bot=MyTankBot())
        t2 = Tank(None, (0, 0, 255), config.COL_COUNT - 1, config.ROW_COUNT - 1, bot=SimpleTankBot())
        self.tanks = [t1, t2]
        
        while len(self.tanks) > 1 or len(self.bullets) > 0:
            self.update()
            time.sleep(config.MS_PER_FRAME / 1000)
        
    def update(self):
        # Render the game perception
        print("Frame {}".format(self.frame))
        GamePerception(
            config.ROW_COUNT,
            config.COL_COUNT,
            self.frame,
            None,
            self.bullets,
            self.tanks
        ).render()
        
        # Shuffle the tank for fair chance
        random.shuffle(self.tanks)
        
        # Get action of every tanks
        new_bullets = []
        same_pos = lambda x1, y1, x2, y2: x1 == x2 and y1 == y2
        for t in self.tanks:
            # Get action; dictionaries are used so action cannot change the state of tanks and bullets
            gp = GamePerception(
                config.ROW_COUNT,
                config.COL_COUNT,
                self.frame,
                t,
                self.bullets,
                [t2 for t2 in self.tanks if t2 != t] # other tanks
            )
            action = t.get_action(gp)
            
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
                if same_pos(t.x, t.y, b.x, b.y) and t.direction is b.direction.inverse():
                    destroyed_tank = t
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
                    destroyed_tank = t
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
        
        if len(self.tanks) > 1:
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
                        self.bullets.append(Bullet(None, x, y, direction))
                        bullet_added = True
                    # else: player exists there, so do not spawn bullet there.
        
        
        self.frame += 1

if __name__ == "__main__":
    app = CommandLineApp()
    app.run()
