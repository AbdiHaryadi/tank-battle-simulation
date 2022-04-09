import re
import yaml
from src.enum.BotAction import BotAction

class BotLoader:
    def __init__(self, path):
        self.path = path
        
    def load(self):
        path = self.path
        with open(path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            
        # Ambil semua actions
        actions = data["actions"]
        action_list = list(actions.keys())
        
        unused_action_list = action_list.copy()
        
        # Cek aksi pertama
        action = data["first_action"]
        if action not in action_list:
            raise ValueError("{}: Error: Unknown action \"{}\" in actions.{}.transitions.{}".format(path, transition["next_action"], action, transition_index))
        else:
            unused_action_list.remove(action)
        
        for action in action_list:
            transitions = actions[action]["transitions"]
            for transition_index, transition in enumerate(transitions):
                # Resolve semua reference dari condition
                if "condition" not in transition:
                    raise ValueError("{}: Error: Missing \"condition\" value in actions.{}.transitions.{}".format(path, action, transition_index))
                elif transition["condition"] == "any":
                    transition["condition"] = {
                        "negative": False,
                        "context": "any",
                        "direction": None
                    }
                else:
                    pattern = r"(?:(no) )?(?:(.*) on (.*))"
                    condition_match = re.match(pattern, transition["condition"])
                    if condition_match:
                        negative = condition_match.group(1) is not None
                        
                        context = condition_match.group(2)
                        if context not in ["enemy", "wall"]:
                            raise ValueError("{}: Error: Unknown context \"{}\" from condition \"{}\" in actions.{}.transitions.{}".format(path, context, transition["condition"], action, transition_index))
                            
                        direction = condition_match.group(3)
                        if direction not in ["north", "south", "east", "west"]:
                            raise ValueError("{}: Error: Unknown direction \"{}\" from condition \"{}\" in actions.{}.transitions.{}".format(path, direction, transition["condition"], action, transition_index))
                            
                        transition["condition"] = {
                            "negative": negative,
                            "context": context,
                            "direction": direction
                        }
                    else:
                        raise ValueError("{}: Error: Unknown condition \"{}\" in actions.{}.transitions.{}".format(path, transition["condition"], action, transition_index))
                
                # Resolve semua reference dari actions
                if "next_action" not in transition:
                    raise ValueError("{}: Error: Missing \"next_action\" value in actions.{}.transitions.{}".format(path, action, transition_index))
                elif transition["next_action"] not in action_list:
                    raise ValueError("{}: Error: Unknown action \"{}\" in actions.{}.transitions.{}".format(path, transition["next_action"], action, transition_index))
                else:
                    if transition["next_action"] in unused_action_list:
                        unused_action_list.remove(transition["next_action"])
                        
        # Resolve semua reference dari command jika ada
        for action in action_list:
            if action not in unused_action_list:
                action_data = actions[action]
                
                if "commands" not in action_data:
                    action_data["commands"] = []
                else:
                    commands_data = action_data["commands"]
                    if type(commands_data) is not list:
                        raise ValueError("{}: Error: actions.{}.commands is not a list.\n(Hint: Put hyphen (\"-\") as a start for each commands.)".format(path, action))
                    elif len(commands_data) > 0:
                        for command_index, command in enumerate(commands_data):
                            if command == "move west":
                                bot_action = BotAction.MOVE_WEST
                            elif command == "move east":
                                bot_action = BotAction.MOVE_EAST
                            elif command == "move north":
                                bot_action = BotAction.MOVE_NORTH
                            elif command == "move south":
                                bot_action = BotAction.MOVE_SOUTH
                            elif command == "shoot west":
                                bot_action = BotAction.SHOOT_WEST
                            elif command == "shoot east":
                                bot_action = BotAction.SHOOT_EAST
                            elif command == "shoot north":
                                bot_action = BotAction.SHOOT_NORTH
                            elif command == "shoot south":
                                bot_action = BotAction.SHOOT_SOUTH
                            elif command == "wait":
                                bot_action = BotAction.DO_NOTHING
                            else:
                                raise ValueError("{}: Unknown command \"{}\" in actions.{}.commands.{}".format(path, command, action, command_index))
                                
                            commands_data[command_index] = bot_action
                    # else: commands_data == []
        
        # Berikan peringatan untuk action yang tidak di-reference
        for unused_action in unused_action_list:
            print("{}: Warning: Unused action \"{}\"".format(path, unused_action))
            
        return data