from src.command.TankCommand import TankCommand
from src.utility import same_pos

class ShootEastCommand(TankCommand):
    def execute(self):
        bullet = self.tank.shoot_east()
        if "bullets" not in self.response:
            self.response["bullets"] = []
            
        self.response["bullets"].append(bullet)