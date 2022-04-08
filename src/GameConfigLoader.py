import yaml
from src.BotLoader import BotLoader
from src.GameConfig import GameConfig

class GameConfigLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        self.load_raw_data()
        self.resolve_bots()
        self.convert_frame_rate_to_int()
        return self.data

    def load_raw_data(self):
        with open(self.path, "r") as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
            
    def resolve_bots(self):
        if "teams" not in self.data:
            print("{}: Warning: Game for non-team mode is not implemented.".format(path))
            self.throw_attribute_not_found("teams")
        else:
            for team in self.data["teams"]:
                # TODO: handle error for tanks and bot_path attribute
                for tank in team["tanks"]:
                    tank |= BotLoader(tank["bot_path"]).load()
                    
    def convert_frame_rate_to_int(self):
        if "frame_rate" in self.data:
            self.data["frame_rate"] = int(self.data["frame_rate"])
        else:
            self.throw_attribute_not_found("frame_rate")
            
    def throw_attribute_not_found(self, attribute):
        raise ValueError("{}: Error: Missing \"{}\" value.".format(self.path, attribute))
            