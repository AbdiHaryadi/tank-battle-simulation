from src.GameConfigLoader import GameConfigLoader
from src.DisplayConfig import DisplayConfig

class AppFactory:
    def __init__(self, game_config_path):
        self.content = GameConfigLoader.load(game_config_path)
        
    def create(self):
        display_config = DisplayConfig(
            window_width=self.content["window_width"],
            window_height=self.content["window_height"],
            row_count=self.content["row_count"],
            col_count=self.content["col_count"],
            frame_rate=self.content["frame_rate"],
            delay_before_start=self.content["delay_before_start"]
        )
        