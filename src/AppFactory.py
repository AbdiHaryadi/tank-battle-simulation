from src.GameConfigLoader import GameConfigLoader

class AppFactory:
    def __init__(self, game_config_path):
        self.game_config = GameConfigLoader.load(game_config_path)
        
    def create(self):
        pass
        