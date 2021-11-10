from TankBot import TankBot
from Action import Action
from Direction import Direction
import random

class MyTankBot(TankBot):
    def __init__(self):
        super().__init__()
        
    def get_action(self, gp):
        # Your AI goes here! :D
        return Action.DO_NOTHING