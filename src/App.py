import tkinter
import random
from math import exp

from src.bot.SimpleTankBot import SimpleTankBot
from src.entity.Bullet import Bullet
from src.entity.Tank import Tank
from src.enum.Direction import Direction
from src.perception.GamePerception import GamePerception

from src.command import MoveWestCommand

class App(tkinter.Tk):
    """
    Class for main application.
    """
    RANDOM_BULLET_RATE = 0.001
    BG_COLOR_1 = "#d0e19c"
    BG_COLOR_2 = "#b5d55e"

    def __init__(self, mode="1v1", game_config=None):
        super().__init__()
        self.title("AI Simulation")
        self.game_config = game_config
        self.tanks = []
        self.bullets = []
        self.frame = 0
        self.mode = mode
        
    def run(self):
        window_width = self.game_config["window_width"]
        window_height = self.game_config["window_height"]
    
        self.canvas = tkinter.Canvas(
            self,
            width=window_width,
            height=window_height
        )
        self.canvas.pack() # make the window fit to canvas
    
        # Create a checkerboard background
        self.canvas.create_rectangle(
            0, 0,                          # from top-left coordinate
            window_width, window_height,   # to bottom-right coordinate
            fill=self.BG_COLOR_1,
            width=0                        # no border
        )
        
        row_count = self.game_config["row_count"]
        col_count = self.game_config["col_count"]
        
        tile_width = window_width / col_count
        tile_height = window_height / row_count
        
        for r in range(row_count):
            for c in range(col_count):
                if (r + c) % 2 == 0:
                    self.canvas.create_rectangle(
                        c * tile_width,
                        r * tile_height,
                        (c + 1) * tile_width,
                        (r + 1) * tile_height,
                        fill=self.BG_COLOR_2,
                        width=0
                    )

        """
        # Create random tanks
        while len(self.tanks) < 2:
            x = random.randrange(0, col_count)
            y = random.randrange(0, row_count)
            if not any(map(lambda t: t.x == x and t.y == y, self.tanks)):
                random_color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
                new_tank = Tank(self.canvas, random_color, x, y)
                self.tanks.append(new_tank)
        """
        
        # For teams first, self.mode is ignored right now
        for team in self.game_config["teams"]:
            for tank in team["tanks"]:
                self.tanks.append(Tank(
                    self.canvas,
                    tank["color"],
                    *tank["initial_position"],
                    team["name"],
                    bot=SimpleTankBot(), # Test
                    game_config=self.game_config
                ))
                
        #input("So far so good.")
        #raise
        
        """
        if self.mode == "1v1":
            #######
            # Put your bot here!
            t1 = Tank(self.canvas, (255, 0, 0), 0, 0, "RED TEAM", bot=SimpleTankBot())
            t2 = Tank(self.canvas, (0, 0, 255), col_count - 1, row_count - 1, "BLUE TEAM", bot=SimpleTankBot())
            self.tanks = [t1, t2]
            #######
        elif self.mode == "3v3":
            tr1 = Tank(self.canvas, (255, 0, 0), 1, 0, "RED TEAM", bot=SimpleTankBot())
            tr2 = Tank(self.canvas, (255, 127, 0), 1, (row_count - 1) // 2, "RED TEAM", bot=SimpleTankBot())
            tr3 = Tank(self.canvas, (255, 0, 127), 1, row_count - 1, "RED TEAM", bot=SimpleTankBot())
            tb1 = Tank(self.canvas, (0, 0, 255), col_count - 2, 0, "BLUE TEAM", bot=SimpleTankBot())
            tb2 = Tank(self.canvas, (0, 127, 255), col_count - 2, (row_count - 1) // 2, "BLUE TEAM", bot=SimpleTankBot())
            tb3 = Tank(self.canvas, (63, 127, 255), col_count - 2, row_count - 1, "BLUE TEAM", bot=SimpleTankBot())
            self.tanks = [tr1, tr2, tr3, tb1, tb2, tb3]
        else:
            raise ValueError("Mode not supported: {}".format(self.mode))
        """

        self.after(self.game_config["delay_before_start"] * 1000, self.update)
        self.mainloop()
        
    def update(self):
        # Shuffle the tank for fair chance
        random.shuffle(self.tanks)
        
        row_count = self.game_config["row_count"]
        col_count = self.game_config["col_count"]
        
        # Get action of every tanks
        new_bullets = []
        same_pos = lambda x1, y1, x2, y2: x1 == x2 and y1 == y2
        for t in self.tanks:
            # Get action; dictionaries are used so action cannot change the state of tanks and bullets
            gp = GamePerception(
                row_count,
                col_count,
                self.frame,
                t,
                self.bullets,
                [t2 for t2 in self.tanks if t2 != t] # other tanks
            )
            response = {}
            command = t.get_command(gp, response).execute()
            
            if "bullets" in response:
                new_bullets += response["bullets"]
        
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
            if not (b.x >= 0 and b.x < col_count and b.y >= 0 and b.y < row_count):
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
                    if direction == Direction.WEST:
                        x = col_count - 1
                        y = random.randrange(0, row_count)
                    elif direction == Direction.EAST:
                        x = 0
                        y = random.randrange(0, row_count)
                    elif direction == Direction.NORTH:
                        x = random.randrange(0, col_count)
                        y = row_count - 1
                    elif direction == Direction.SOUTH:
                        x = random.randrange(0, col_count)
                        y = 0
                    else:
                        print(direction, "what?")
                        raise ValueError
                    
                    if not any(list(map(lambda t: t.x == x and t.y == y, self.tanks))):
                        self.bullets.append(Bullet(self.canvas, x, y, direction, color=(71, 63, 63),
                            game_config=self.game_config))
                        bullet_added = True
                    # else: player exists there, so do not spawn bullet there.
        
        self.frame += 1
        self.after(1000 // self.game_config["frame_rate"], self.update)

if __name__ == "__main__":
    app = App()
    app.run()
