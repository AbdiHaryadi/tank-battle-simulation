from src.App import App
import sys

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