from src.command.TankCommand import TankCommand
from src.utility import same_pos

class MoveWestCommand(TankCommand):
    def execute(self):
        t = self.tank
        if not any(map(
                lambda t2: same_pos(t.x - 1, t.y, t2.x, t2.y),
                self.gp.other_tanks)):
            t.move_west()
