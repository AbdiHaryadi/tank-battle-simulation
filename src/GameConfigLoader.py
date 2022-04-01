import yaml
from src.BotLoader import BotLoader

class GameConfigLoader:
    @staticmethod
    def load(path):
        with open(path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            
        if "teams" in data:
            for team in data["teams"]:
                for tank in team["tanks"]:
                    tank |= BotLoader.load(tank["bot_path"])
        
        return data
        