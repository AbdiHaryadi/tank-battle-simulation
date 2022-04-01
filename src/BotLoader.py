import yaml

class BotLoader:
    @staticmethod
    def load(path):
        with open(path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            
        return data