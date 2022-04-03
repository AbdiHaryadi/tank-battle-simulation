from src.command.TankCommand import TankCommand
from src.utility import same_pos

class DoNothingCommand(TankCommand):
    def execute(self):
        pass # literally nothing
