from src.App import App
from src.GameConfigLoader import GameConfigLoader

class AppFactory:
    def __init__(self, game_config_path):
        self.game_config = GameConfigLoader(game_config_path)
        
    def create(self):
        return App(game_config=self.game_config.load())
        