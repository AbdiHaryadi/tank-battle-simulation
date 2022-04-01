import yaml
from src.BotLoader import BotLoader
from src.GameConfig import GameConfig

class GameConfigLoader:
    @staticmethod
    def load(path):
        with open(path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            
        if "teams" in data:
            for team in data["teams"]:
                for tank in team["tanks"]:
                    tank |= BotLoader.load(tank["bot_path"])
                    
        if "frame_rate" in data:
            data["frame_rate"] = int(data["frame_rate"])
        
        return data
        """
        return GameConfig(
            window_width=data["window_width"],
            window_height=data["window_height"],
            row_count=data["row_count"],
            col_count=data["col_count"],
            frame_rate=data["frame_rate"],
            delay_before_start=data["delay_before_start"]
        )
        """
        