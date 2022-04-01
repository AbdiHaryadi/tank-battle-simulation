class GameConfig:
    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            print(arg, value)
            if arg == "window_width":
                self.window_width = value
            elif arg == "window_height":
                self.window_height = value
            elif arg == "row_count":
                self.row_count = value
            elif arg == "col_count":
                self.col_count = value
            elif arg == "frame_rate":
                self.frame_rate = value
            elif arg == "delay_before_start":
                self.delay_before_start = value
            else:
                print("Warning: Unknown argument \"{}\" ignored.".format())
                