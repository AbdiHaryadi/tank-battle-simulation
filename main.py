from src import App, AppFactory
import sys
import yaml

"""
error = False
mode = "1v1"
if len(sys.argv) == 1:
    pass
    
elif len(sys.argv) == 2:
    mode = sys.argv[1]

else:
    print("Error: does not support more than one argument.")
    error = True
    



app = App(mode=mode)
app.run()
"""

try:
    AppFactory("game_config.yaml")
        
except FileNotFoundError:
    print("Error: \"{}\" is not found.".format(filename))

