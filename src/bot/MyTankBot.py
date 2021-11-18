import random

from src.bot.TankBot import TankBot
from src.enum.Action import Action
from src.enum.Direction import Direction

class MyTankBot(TankBot):
    def __init__(self):
        super().__init__()
        
    def get_action(self, gp):
        # Your AI goes here! :D
        return Action.DO_NOTHING