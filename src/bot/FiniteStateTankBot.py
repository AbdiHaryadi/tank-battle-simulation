from src.enum.BotAction import BotAction

class FiniteStateTankBot:
    def __init__(self, config):
        self.actions = config["actions"]
        self.current_action_name = config["first_action"]
        self.command_index = None
        
    def get_action(self, gp):
        self.set_next_action(gp)
        return self.current_action
    
    def set_next_action(self, gp):
        if self.command_index is not None:
            if self.command_index == self.command_list_length() - 1:
                self.set_next_action_name(gp)
                self.command_index = None
            else:
                self.command_index += 1
                
        if self.command_index is None:
            if self.command_list_length() > 0:
                self.set_next_action_name(gp)
                self.command_index = 0
                
            else:
                # Mulai traverse
                traverse_start_action_name = self.current_action_name
                self.set_next_action_name(gp)
                
                while self.command_list_length() == 0 and self.current_action_name != traverse_start_action_name:
                    self.set_next_action_name(gp)
                
                if self.command_list_length() > 0:
                    self.command_index = 0
                else:
                    print("Warning: infinite loop detected; bot does nothing")
                    
        self.current_action = self.get_current_command()
    
    def command_list_length(self):
        return len(self.actions[self.current_action_name]["commands"])
        
    def set_next_action_name(self, gp):
        transition_index = 0
        condition_satisfied = False
        while transition_index < self.transition_list_length() and not condition_satisfied:
            if self.transition_condition_satisfied(transition_index, gp):
                condition_satisfied = True
            else:
                transition_index += 1
            
        if condition_satisfied:
            self.current_action_name = self.transition_next_action_name(transition_index)
        # else: no change
            
    def transition_list_length(self):
        return len(self.actions[self.current_action_name]["transitions"])
        
    def transition_condition_satisfied(self, index, gp):
        condition = self.transition_condition(index)
        satisfied = None
        context = condition["context"]
        direction = condition["direction"]
        
        if context == "any":
            satisfied = True
            
        if context == "wall":
            row = gp.player_tank.y
            col = gp.player_tank.x
            
            if direction == "north":
                satisfied = (row == 0)
                
            elif direction == "south":
                satisfied = (row == gp.row_count - 1)
                
            elif direction == "west":
                satisfied = (col == 0)
                
            elif direction == "east":
                satisfied = (col == gp.col_count - 1)
                
            else:
                raise ValueError("Unknown direction: {}".format(direction))
                
        if context == "enemy":
            player_row = gp.player_tank.y
            player_col = gp.player_tank.x
            enemies = gp.get_enemies()
            enemy_count = len(enemies)
            
            enemy_index = 0
            satisfied = False
            while enemy_index < enemy_count and not satisfied:
                enemy_row = enemies[enemy_index].y
                enemy_col = enemies[enemy_index].x
                
                if direction == "north":
                    satisfied = (enemy_col == player_col
                                 and enemy_row < player_row)
                    
                elif direction == "south":
                    satisfied = (enemy_col == player_col
                                 and enemy_row > player_row)
                    
                elif direction == "west":
                    satisfied = (enemy_row == player_row
                                 and enemy_col < player_col)
                    
                elif direction == "east":
                    satisfied = (enemy_row == player_row
                                 and enemy_col > player_col)
                    
                else:
                    raise ValueError("Unknown direction: {}".format(direction))
                    
                if not satisfied:
                    enemy_index += 1
                    
        if satisfied is None:
            raise ValueError("Unknown context: {}".format(context))
            
        if condition["negative"]:
            satisfied = not satisfied
        
        return satisfied
        
    def transition_condition(self, index):
        return self.actions[self.current_action_name]["transitions"][index]["condition"]
        
    def transition_next_action_name(self, index):
        return self.actions[self.current_action_name]["transitions"][index]["next_action"]
    
    def get_current_command(self):
        if self.command_index is None:
            return BotAction.DO_NOTHING
        else:
            return self.actions[self.current_action_name]["commands"][self.command_index]