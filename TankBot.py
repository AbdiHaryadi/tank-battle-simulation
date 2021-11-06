from Action import Action
import random

class TankBot:
    def __init__(self):
        pass
        
    def get_action(self, gp):
        if gp.frame % 4 == 0:
            return random.choice(list(Action))
        else:
            return Action.DO_NOTHING
