import tkinter
import random
from math import exp

WIDTH = 640
HEIGHT = 480
TILE_WIDTH = 32
TILE_HEIGHT = 32
# So it's 20 x 15

window = tkinter.Tk()

window.title("AI Simulation")
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT)

canvas.pack()
# Create a background
canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#d0e19c", width=0)
# Create a checkerboard
for r in range(15):
    for c in range(20):
        if (r + c) % 2 == 0:
            canvas.create_rectangle(
                c * TILE_WIDTH,
                r * TILE_HEIGHT,
                (c + 1) * TILE_WIDTH,
                (r + 1) * TILE_HEIGHT,
                fill = "#a5c54e",
                width = 0
            )

color_hex = lambda r, g, b: "#{:0>6}".format(hex(r * 256 * 256 + g * 256 + b)[2:])
to_half_dark = lambda color: tuple(map(lambda x: x // 2, color))            

ACTION_LIST = ["right", "down", "up", "left", "s_right", "s_left", "s_up", "s_down"]

class Tank:
    turret_coordinate = {
        "right": (16, 12, 28, 20),
        "left": (4, 12, 16, 20),
        "down": (12, 16, 20, 28),
        "up": (12, 4, 20, 16),
    }

    def __init__(self, cv, color, x, y, act_function=None):
        self.cv = cv
        self.color = color
        self.x = x
        self.y = y
        self.act_function = act_function
        self.direction = "right"
        self.body = canvas.create_rectangle(
            x * TILE_WIDTH + 8,
            y * TILE_HEIGHT + 8,
            x * TILE_WIDTH + 24,
            y * TILE_HEIGHT + 24,
            fill=color_hex(*color),
            width=0
        )
        
        x1, y1, x2, y2 = self.turret_coordinate[self.direction]
        self.turret = canvas.create_rectangle(
            x * TILE_WIDTH + x1,
            y * TILE_HEIGHT + y1,
            x * TILE_WIDTH + x2,
            y * TILE_HEIGHT + y2,
            fill=color_hex(*to_half_dark(color)),
            width=0
        )
        
    def move_right(self):
        if self.x < 19:
            self.x += 1
        self.turn_right(update=False)
        self.update()
    
    def move_left(self):
        if self.x > 0:
            self.x -= 1
        self.turn_left(update=False)
        self.update()
        
    def move_up(self):
        if self.y > 0:
            self.y -= 1
        self.turn_up(update=False)
        self.update()
        
    def move_down(self):
        if self.y < 14:
            self.y += 1
        self.turn_down(update=False)
        self.update()
        
    def turn_right(self, update=True):
        self.direction = "right"
        if update:
            self.update()
    
    def turn_left(self, update=True):
        self.direction = "left"
        if update:
            self.update()
        
    def turn_up(self, update=True):
        self.direction = "up"
        if update:
            self.update()
        
    def turn_down(self, update=True):
        self.direction = "down"
        if update:
            self.update()
            
    def shoot_right(self):
        self.turn_right(update=False)
        self.update()
        return Bullet(self.cv, (255, 127, 0), self.x + 1, self.y, "right")
    
    def shoot_left(self):
        self.turn_left(update=False)
        self.update()
        return Bullet(self.cv, (255, 127, 0), self.x - 1, self.y, "left")
        
    def shoot_up(self):
        self.turn_up(update=False)
        self.update()
        return Bullet(self.cv, (255, 127, 0), self.x, self.y - 1, "up")
        
    def shoot_down(self):
        self.turn_down(update=False)
        self.update()
        return Bullet(self.cv, (255, 127, 0), self.x, self.y + 1, "down")
        
    def update(self):
        self.cv.coords(
            self.body,
            self.x * TILE_WIDTH + 8,
            self.y * TILE_HEIGHT + 8,
            self.x * TILE_WIDTH + 24,
            self.y * TILE_HEIGHT + 24,
        )
        
        x1, y1, x2, y2 = self.turret_coordinate[self.direction]
        self.cv.coords(
            self.turret,
            self.x * TILE_WIDTH + x1,
            self.y * TILE_HEIGHT + y1,
            self.x * TILE_WIDTH + x2,
            self.y * TILE_HEIGHT + y2,
        )
        
    def destruct(self):
        print("Destroyed!")
        self.cv.delete(self.body)
        self.cv.delete(self.turret)
    
    def get_action(self, frame, bullets, other_tanks):
        if self.act_function == None:
            return random.choice(ACTION_LIST)
        else:
            return self.act_function(
                {"x": self.x, "y": self.y, "direction": self.direction},
                frame, bullets, other_tanks)
        
class Bullet:
    delta_x = {"right": 1, "left": -1, "up": 0, "down": 0}
    delta_y = {"right": 0, "left": 0, "up": -1, "down": 1}
    def __init__(self, cv, color, x, y, direction):
        self.cv = cv
        self.color = color
        self.x = x
        self.y = y
        self.direction = direction
        if direction in ["right", "left"]:
            self.bullet = canvas.create_rectangle(
                self.x * TILE_WIDTH + 8,
                self.y * TILE_HEIGHT + 15,
                self.x * TILE_WIDTH + 24,
                self.y * TILE_HEIGHT + 17,
                fill=color_hex(*color),
                width=0)
        elif direction in ["up", "down"]:
            self.bullet = canvas.create_rectangle(
                self.x * TILE_WIDTH + 15,
                self.y * TILE_HEIGHT + 8,
                self.x * TILE_WIDTH + 17,
                self.y * TILE_HEIGHT + 24,
                fill=color_hex(*color),
                width=0)
                
    def move(self):
        self.x += self.delta_x[self.direction]
        self.y += self.delta_y[self.direction]
        self.update()
        
    def update(self):
        if self.direction in ["right", "left"]:
            self.cv.coords(
                self.bullet,
                self.x * TILE_WIDTH + 8,
                self.y * TILE_HEIGHT + 15,
                self.x * TILE_WIDTH + 24,
                self.y * TILE_HEIGHT + 17,
            )
        elif self.direction in ["up", "down"]:
            self.cv.coords(
                self.bullet,
                self.x * TILE_WIDTH + 15,
                self.y * TILE_HEIGHT + 8,
                self.x * TILE_WIDTH + 17,
                self.y * TILE_HEIGHT + 24,
            )
            
    def destruct(self):
        self.cv.delete(self.bullet)
        




#bullet = Bullet(canvas, (255, 127, 0), 1, 2, "right")

#color = (0, 0, 127)
#canvas.create_rectangle(8, 8, 24, 24, fill=color_hex(*color), width=0)
#canvas.create_rectangle(16, 12, 28, 20, fill=color_hex(*to_half_dark(color)), width=0)

# Create bullet
#bullet = canvas.create_rectangle(8 + 32, 15, 24 + 32, 17, fill=color_hex(255, 127, 0), width=0)

"""
def right_action(event=None):
    t1.move_right()

def left_action(event=None):
    t1.move_left()
    
def up_action(event=None):
    t1.move_up()
    
def down_action(event=None):
    t1.move_down()
    
def space_action(event=None):
    delta_x = {"right": 1, "left": -1, "up": 0, "down": 0}
    delta_y = {"right": 0, "left": 0, "up": -1, "down": 1}
    
    bullet = Bullet(canvas, (255, 127, 0), t1.x + delta_x[t1.direction], t1.y + delta_y[t1.direction], t1.direction)
    
    def loop(b):
        if b.x >= 0 and b.x < 20 and b.y >= 0 and b.y < 15:
            b.move()
            window.after(100, loop, b)
        else:
            del b
    
    window.after(100, loop, bullet)

window.bind('<Right>', right_action)
window.bind('<Left>', left_action)
window.bind('<Up>', up_action)
window.bind('<Down>', down_action)
window.bind('<space>', space_action)
"""

# canvas.pack()

MS_PER_FRAME = 50



def random_action(tank, frame, bullets, other_tanks):
    return random.choice(ACTION_LIST)

# Create the tank
current_tanks = []

def abdi_act_function(tank, frame, bullets, other_tanks):
    # You can just check the position and direction of the object
    # Check bullet
    if len(bullets) == 0:
        return random.choice(ACTION_LIST)
    else:
        bullet = min(bullets, key=lambda b: min(abs(tank["x"] - b["x"]), abs(tank["y"] - b["y"])))
        if bullet["x"] == tank["x"] and ((tank["y"] < bullet["y"] and bullet["direction"] == "up") or (tank["y"] > bullet["y"] and bullet["direction"] == "down")):
            if tank["x"] == 0:
                return "right"
            elif tank["x"] == 19:
                return "right"
            else:
                return random.choice(["right", "left"])
        elif bullet["y"] == tank["y"] and ((tank["x"] < bullet["x"] and bullet["direction"] == "left") or (tank["x"] > bullet["x"] and bullet["direction"] == "right")):
            if tank["y"] == 0:
                return "down"
            elif tank["y"] == 19:
                return "up"
            else:
                return random.choice(["down", "up"])
        else:
            return random.choice(ACTION_LIST)
            

def attacker_action(tank, frame, bullets, other_tanks, first_target=True):
    # Intinya dia selalu ingin menembak
    dont_stay = any(map(lambda b: (
        (b["direction"] == "up" and b["x"] == tank["x"] and b["y"] == tank["y"] + 1)
        or (b["direction"] == "down" and b["x"] == tank["x"] and b["y"] == tank["y"] - 1)
        or (b["direction"] == "left" and b["y"] == tank["y"] and b["x"] == tank["x"] + 1)
        or (b["direction"] == "right" and b["y"] == tank["y"] and b["x"] == tank["x"] - 1)
    ), bullets))
    dont_up = any(map(lambda b: (
        (b["direction"] == "down" and b["x"] == tank["x"] and (b["y"] == tank["y"] - 1 or b["y"] == tank["y"] - 2))
        or (b["direction"] == "left" and b["y"] == tank["y"] - 1 and b["x"] == tank["x"] + 1)
        or (b["direction"] == "right" and b["y"] == tank["y"] - 1 and b["x"] == tank["x"] - 1)
    ), bullets))
    dont_down = any(map(lambda b: (
        (b["direction"] == "up" and b["x"] == tank["x"] and (b["y"] == tank["y"] + 1 or b["y"] == tank["y"] + 2))
        or (b["direction"] == "left" and b["y"] == tank["y"] + 1 and b["x"] == tank["x"] + 1)
        or (b["direction"] == "right" and b["y"] == tank["y"] + 1 and b["x"] == tank["x"] - 1)
    ), bullets))
    dont_right = any(map(lambda b: (
        (b["direction"] == "left" and b["y"] == tank["y"] and (b["x"] == tank["x"] + 1 or b["x"] == tank["x"] + 2))
        or (b["direction"] == "up" and b["x"] == tank["x"] + 1 and b["y"] == tank["y"] + 1)
        or (b["direction"] == "down" and b["x"] == tank["x"] + 1 and b["y"] == tank["y"] - 1)
    ), bullets))
    dont_left = any(map(lambda b: (
        (b["direction"] == "right" and b["y"] == tank["y"] and (b["x"] == tank["x"] - 1 or b["x"] == tank["x"] - 2))
        or (b["direction"] == "up" and b["x"] == tank["x"] - 1 and b["y"] == tank["y"] + 1)
        or (b["direction"] == "down" and b["x"] == tank["x"] - 1 and b["y"] == tank["y"] - 1)
    ), bullets))
    
    if dont_stay:
        next_target = None
            
    elif len(other_tanks) == 0:
        return None
        
    else:
        next_target = min(other_tanks, key=lambda t: abs(tank["x"] - t["x"]) + abs(tank["y"] - t["y"]))
        if tank["x"] == next_target["x"]:
            if tank["y"] < next_target["y"]:
                # Check down direction
                if len(list(filter(lambda b: b["direction"] == "down" and b["x"] == next_target["x"] and b["y"] < next_target["y"], bullets))) > 0:
                    new_other_tanks = other_tanks[:]
                    new_other_tanks.remove(next_target)
                    action = attacker_action(tank, frame, bullets, new_other_tanks, False)
                    if action != None or not first_target:
                        return action
                else:
                    return "s_down"
            else:
                # Check up direction
                if len(list(filter(lambda b: b["direction"] == "up" and b["x"] == next_target["x"] and b["y"] > next_target["y"], bullets))) > 0:
                    new_other_tanks = other_tanks[:]
                    new_other_tanks.remove(next_target)
                    action = attacker_action(tank, frame, bullets, new_other_tanks, False)
                    if action != None or not first_target:
                        return action
                else:
                    return "s_up"
        elif tank["y"] == next_target["y"]:
            if tank["x"] < next_target["x"]:
                # Check right direction
                if len(list(filter(lambda b: b["direction"] == "right" and b["y"] == next_target["y"] and b["x"] < next_target["x"], bullets))) > 0:
                    new_other_tanks = other_tanks[:]
                    new_other_tanks.remove(next_target)
                    action = attacker_action(tank, frame, bullets, new_other_tanks, False)
                    if action != None or not first_target:
                        return action
                else:
                    return "s_right"
            else:
                # Check left direction
                if len(list(filter(lambda b: b["direction"] == "left" and b["y"] == next_target["y"] and b["x"] > next_target["x"], bullets))) > 0:
                    new_other_tanks = other_tanks[:]
                    new_other_tanks.remove(next_target)
                    action = attacker_action(tank, frame, bullets, new_other_tanks, False)
                    if action != None or not first_target:
                        return action
                else:
                    return "s_left"
                    
        elif abs(tank["x"] - next_target["x"]) < abs(tank["y"] - next_target["y"]):
            if tank["x"] < next_target["x"]:
                if not dont_right:
                    return "right"
            else:
                if not dont_left:
                    return "left"
        else:
            if tank["y"] < next_target["y"]:
                if not dont_down:
                    return "down"
            else:
                if not dont_up:
                    return "up"
                    
    # Collect good actions if not return yet
    good_actions = []
    if not dont_stay:
        good_actions.append(None)
    if not dont_up and tank["y"] > 0:
        good_actions.append("up")
    if not dont_down and tank["y"] < 14:
        good_actions.append("down")
    if not dont_right and tank["x"] < 19:
        good_actions.append("right")
    if not dont_left and tank["x"] > 0:
        good_actions.append("left")
        
    if next_target == None:
        if len(good_actions) > 0:
            return random.choice(good_actions)
        else:
            return None
    else:
        # Go to target as near as possible
        random.shuffle(good_actions)
        best_action = None
        distance = abs(tank["x"] - next_target["x"]) + abs(tank["y"] - next_target["y"])
        
        for action in good_actions:
            if action == "right":
                new_distance = abs(tank["x"] + 1 - next_target["x"]) + abs(tank["y"] - next_target["y"])
                if new_distance < distance:
                    best_action = action
                    distance = new_distance
            elif action == "left":
                new_distance = abs(tank["x"] - 1 - next_target["x"]) + abs(tank["y"] - next_target["y"])
                if new_distance < distance:
                    best_action = action
                    distance = new_distance
            elif action == "up":
                new_distance = abs(tank["x"] - next_target["x"]) + abs(tank["y"] - 1 - next_target["y"])
                if new_distance < distance:
                    best_action = action
                    distance = new_distance
            elif action == "down":
                new_distance = abs(tank["x"] - next_target["x"]) + abs(tank["y"] + 1 - next_target["y"])
                if new_distance < distance:
                    best_action = action
                    distance = new_distance
        
        return best_action
                    
        
     

def dodge_action(tank, frame, bullets, other_tanks, first_target=True):
    # Intinya dia selalu ingin menghindar
    dont_stay = any(map(lambda b: (
        (b["direction"] == "up" and b["x"] == tank["x"] and b["y"] == tank["y"] + 1)
        or (b["direction"] == "down" and b["x"] == tank["x"] and b["y"] == tank["y"] - 1)
        or (b["direction"] == "left" and b["y"] == tank["y"] and b["x"] == tank["x"] + 1)
        or (b["direction"] == "right" and b["y"] == tank["y"] and b["x"] == tank["x"] - 1)
    ), bullets))
    dont_up = any(map(lambda b: (
        (b["direction"] == "down" and b["x"] == tank["x"] and (b["y"] == tank["y"] - 1 or b["y"] == tank["y"] - 2))
        or (b["direction"] == "left" and b["y"] == tank["y"] - 1 and b["x"] == tank["x"] + 1)
        or (b["direction"] == "right" and b["y"] == tank["y"] - 1 and b["x"] == tank["x"] - 1)
    ), bullets))
    dont_down = any(map(lambda b: (
        (b["direction"] == "up" and b["x"] == tank["x"] and (b["y"] == tank["y"] + 1 or b["y"] == tank["y"] + 2))
        or (b["direction"] == "left" and b["y"] == tank["y"] + 1 and b["x"] == tank["x"] + 1)
        or (b["direction"] == "right" and b["y"] == tank["y"] + 1 and b["x"] == tank["x"] - 1)
    ), bullets))
    dont_right = any(map(lambda b: (
        (b["direction"] == "left" and b["y"] == tank["y"] and (b["x"] == tank["x"] + 1 or b["x"] == tank["x"] + 2))
        or (b["direction"] == "up" and b["x"] == tank["x"] + 1 and b["y"] == tank["y"] + 1)
        or (b["direction"] == "down" and b["x"] == tank["x"] + 1 and b["y"] == tank["y"] - 1)
    ), bullets))
    dont_left = any(map(lambda b: (
        (b["direction"] == "right" and b["y"] == tank["y"] and (b["x"] == tank["x"] - 1 or b["x"] == tank["x"] - 2))
        or (b["direction"] == "up" and b["x"] == tank["x"] - 1 and b["y"] == tank["y"] + 1)
        or (b["direction"] == "down" and b["x"] == tank["x"] - 1 and b["y"] == tank["y"] - 1)
    ), bullets))
    

    good_actions = []
    if not dont_stay:
        good_actions.append(None)
    if not dont_up and tank["y"] > 0 and not any(list(map(lambda t: t["x"] == tank["x"] and t["y"] == tank["y"] - 1, other_tanks))):
        good_actions.append("up")
    if not dont_down and tank["y"] < 14 and not any(list(map(lambda t: t["x"] == tank["x"] and t["y"] == tank["y"] + 1, other_tanks))):
        good_actions.append("down")
    if not dont_right and tank["x"] < 19 and not any(list(map(lambda t: t["x"] == tank["x"] + 1 and t["y"] == tank["y"], other_tanks))):
        good_actions.append("right")
    if not dont_left and tank["x"] > 0 and not any(list(map(lambda t: t["x"] == tank["x"] - 1 and t["y"] == tank["y"], other_tanks))):
        good_actions.append("left")
    
    enemy_count = len(bullets) + len(other_tanks)
    if len(good_actions) > 0 and enemy_count > 0:
        # Go from bullet and tank as far as possible
        random.shuffle(good_actions)
        best_action = "null"
        FACTOR = 2
        FACTOR_2 = 2
        problem_x = (sum(list(map(lambda b: b["x"], bullets))) + sum(list(map(lambda t: t["x"], other_tanks)))) / (len(bullets) + len(other_tanks))
        problem_y = (sum(list(map(lambda b: b["y"], bullets))) + sum(list(map(lambda t: t["y"], other_tanks)))) / (len(bullets) + len(other_tanks))
        
        def heuristic_function(x, y):
            score = 0
            # Bullets
            for b in bullets:
                if b["direction"] == "right" and b["y"] == y and b["x"] <= x:
                    score += 1 / (x - b["x"] + 0.1)
                elif b["direction"] == "left" and b["y"] == y and b["x"] >= x:
                    score += 1 / (b["x"] - x + 0.1)
                elif b["direction"] == "down" and b["x"] == x and b["y"] <= y:
                    score += 1 / (y - b["y"] + 0.1)
                elif b["direction"] == "up" and b["x"] == x and b["y"] >= y:
                    score += 1 / (b["y"] - y + 0.1)
                    
            # Tanks
            for t in other_tanks:
                if abs(x - t["x"]) + abs(y - t["y"]) <= 3:
                    score += (len(bullets) + 1) * 10
                    
            return score
                
        scores = list(map(lambda pos: (heuristic_function(*pos), pos), [(i % 20, i // 20) for i in range(300)]))
        min_score = min(scores, key=lambda x: x[0])
        target = list(filter(lambda x: x[0] == min_score[0], scores))
        target = list(map(lambda x: x[1], target))
        target_x, target_y = min(target, key=lambda pos: abs(pos[0] - tank["x"]) + abs(pos[1] - tank["y"]))
        #target_x, target_y = min([(i % 20, i // 20) for i in range(300)], key=lambda pos: heuristic_function(*pos))
        print(target_x, target_y)
        
        next_target = {"x": target_x, "y": target_y}
        
        distance = 0
        
        for action in good_actions:
            if action == "right":
                new_distance = abs(tank["x"] + 1 - next_target["x"]) ** FACTOR + abs(tank["y"] - next_target["y"]) ** FACTOR
                if new_distance < distance or best_action == "null":
                    best_action = action
                    distance = new_distance
            elif action == "left":
                new_distance = abs(tank["x"] - 1 - next_target["x"]) ** FACTOR + abs(tank["y"] - next_target["y"]) ** FACTOR
                if new_distance < distance or best_action == "null":
                    best_action = action
                    distance = new_distance
            elif action == "up":
                new_distance = abs(tank["x"] - next_target["x"]) ** FACTOR + abs(tank["y"] - 1 - next_target["y"]) ** FACTOR
                if new_distance < distance or best_action == "null":
                    best_action = action
                    distance = new_distance
            elif action == "down":
                new_distance = abs(tank["x"] - next_target["x"]) ** FACTOR + abs(tank["y"] + 1 - next_target["y"]) ** FACTOR
                if new_distance < distance or best_action == "null":
                    best_action = action
                    distance = new_distance
            elif action == None:
                new_distance = abs(tank["x"] - next_target["x"]) ** FACTOR + abs(tank["y"] - next_target["y"]) ** FACTOR
                if new_distance < distance or best_action == "null":
                    best_action = action
                    distance = new_distance

        print("Choose:", end=" ")
        print(best_action, distance)
        if best_action == None:
            return ["s_down", "s_left", "s_up", "s_right"][random.randint(0, 3)]
        else:
            return best_action
        
    else:
        return ["s_down", "s_left", "s_up", "s_right"][random.randint(0, 3)]
            

#own_tank = Tank(canvas, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 0, 0, attacker_action)
#current_tanks.append(own_tank)

# Create random tanks
while len(current_tanks) < 2:
    x = random.randint(0, 19)
    y = random.randint(0, 14)
    if not any(map(lambda t: t.x == x and t.y == y, current_tanks)):
        new_tank = Tank(canvas, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), x, y, attacker_action if len(current_tanks) % 2 == 0 else attacker_action)
        current_tanks.append(new_tank)

def update(tanks, frame=0, bullets=[]):
    random.shuffle(tanks)
    new_bullets = []
    for t in tanks:
        action = t.get_action(
            frame,
            [{"x": b.x, "y": b.y, "direction": b.direction} for b in bullets],
            [{"x": t2.x, "y": t2.y, "direction": t2.direction} for t2 in tanks if t2 != t]
        )
        if action == "right":
            if not any(map(lambda t2: t2.x == t.x + 1 and t2.y == t.y and t2 != t, tanks)):
                t.move_right()
        elif action == "left":
            if not any(map(lambda t2: t2.x == t.x - 1 and t2.y == t.y and t2 != t, tanks)):
                t.move_left()
        elif action == "up":
            if not any(map(lambda t2: t2.x == t.x and t2.y == t.y - 1 and t2 != t, tanks)):
                t.move_up()
        elif action == "down":
            if not any(map(lambda t2: t2.x == t.x and t2.y == t.y + 1 and t2 != t, tanks)):
                t.move_down()
        elif action == "s_right":
            bullet = t.shoot_right()
            new_bullets.append(bullet)
        elif action == "s_left":
            bullet = t.shoot_left()
            new_bullets.append(bullet)
        elif action == "s_up":
            bullet = t.shoot_up()
            new_bullets.append(bullet)
        elif action == "s_down":
            bullet = t.shoot_down()
            new_bullets.append(bullet)
        # else: no action
    
    removed_bullets = []
    
    # Melawan bullet
    direction_inv = {
        "right": "left",
        "left": "right",
        "up": "down",
        "down": "up"
    }
    for b in bullets:
        # Asumsikan 1 bulet, 1 tank
        destroyed_tank = None
        for t in tanks:
            if t.x == b.x and t.y == b.y and t.direction == direction_inv[b.direction]:
                # Misalkan tidak hancur
                destroyed_tank = t
                removed_bullets.append(b)
                break
                
        if destroyed_tank != None:
            tanks.remove(destroyed_tank)
            destroyed_tank.destruct()
            
    for b in bullets:
        b.move()
            
    bullets += new_bullets
    
    for b in bullets:
        if not (b.x >= 0 and b.x < 20 and b.y >= 0 and b.y < 15):
            removed_bullets.append(b)
    
    for b in bullets:
        # Asumsikan 1 bulet, 1 tank
        destroyed_tank = None
        for t in tanks:
            if t.x == b.x and t.y == b.y:
                # Misalkan tidak hancur
                destroyed_tank = t
                removed_bullets.append(b)
                break
                
        if destroyed_tank != None:
            tanks.remove(destroyed_tank)
            destroyed_tank.destruct()
            
    for b in removed_bullets:
        bullets.remove(b)
        b.destruct()
        
    # Add minimal bullet existence
    p = exp(-frame / 1000) + (1 if len(tanks) <= 1 else 0)
    while p < random.random():
        bullet_added = False
        while not bullet_added:
            direction = random.choice(["up", "down", "left", "right"])
            if direction == "up":
                x = random.randint(0, 19)
                y = 14
            elif direction == "down":
                x = random.randint(0, 19)
                y = 0
            elif direction == "left":
                x = 19
                y = random.randint(0, 14)
            elif direction == "right":
                x = 0
                y = random.randint(0, 14)
            else:
                print(direction, "what?")
                raise ValueError
            
            if not any(list(map(lambda t: t.x == x and t.y == y, tanks))):
                bullets.append(Bullet(canvas, (255, 127, 0), x, y, direction))
                bullet_added = True
            else:
                print("Bullet conflict with tank")
    
    """
    while p < random.random():
        a = random.randint(0, 12)
        bullets.append(Bullet(canvas, (255, 127, 0), 19, a, "left"))
        bullets.append(Bullet(canvas, (255, 127, 0), 19, a + 1, "left"))
        bullets.append(Bullet(canvas, (255, 127, 0), 19, a + 2, "left"))
    """
    
    window.after(MS_PER_FRAME, update, tanks, frame+1, bullets)

window.after(3000, update, current_tanks)
window.mainloop()