import random

from src.bot.TankBot import TankBot
from src.enum.BotAction import BotAction
from src.enum.Direction import Direction

class SimpleTankBot(TankBot):
    """
    SimpleTankBot is an example for TankBot implementation.
    This bot just try to avoid bullets which approaching to the tank
    by moving orthogonally to the direction of bullet, randomly.
    If there is no approaching bullet, TankBot will return random action
    if frame can divided by four. If not, TankBot will return do-nothing
    action.
    """
    def __init__(self):
        super().__init__()
        
    def get_action(self, gp):
        # Check bullets
        i = 0
        action = None
        while i < len(gp.bullets) and action == None:
            curr_bullet = gp.bullets[i]
            if curr_bullet.team_id != gp.player_tank.team_id:
                if curr_bullet.direction in [Direction.WEST, Direction.EAST]:
                    # Case: bullet approaching tank one or two tile horizontally
                    if abs(curr_bullet.x - gp.player_tank.x) <= 2:
                        if curr_bullet.y == gp.player_tank.y:
                            if (curr_bullet.x > gp.player_tank.x) == (curr_bullet.direction == Direction.WEST):
                                # Move vertically
                                v_move_actions = [BotAction.MOVE_NORTH, BotAction.MOVE_SOUTH]
                                action = random.choice(v_move_actions)
                            
                else:
                    # Case: bullet approaching tank one or two tile vertically
                    if abs(curr_bullet.y - gp.player_tank.y) <= 2:
                        if curr_bullet.x == gp.player_tank.x:
                            if (curr_bullet.y > gp.player_tank.y) == (curr_bullet.direction == Direction.NORTH):
                                # Move horizontally
                                h_move_actions = [BotAction.MOVE_WEST, BotAction.MOVE_EAST]
                                action = random.choice(h_move_actions)
                
            i += 1
            
        if action != None:
            return action
        
        else:
            if gp.frame % 4 == 0:
                return random.choice(list(BotAction))
            else:
                return BotAction.DO_NOTHING
