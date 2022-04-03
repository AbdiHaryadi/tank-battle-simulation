from src.command.TankCommand import TankCommand
from src.utility import same_pos

class MoveSouthCommand(TankCommand):
    def execute(self):
        t = self.tank
        if not any(map(
                lambda t2: same_pos(t.x, t.y + 1, t2.x, t2.y),
                self.gp.other_tanks)):
            t.move_south()
        