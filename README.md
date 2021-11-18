# Tank Battle Simulation

Tank Battle Simulation is a simple Python-Tkinter-based application for simulating tank battle. The rule of the battle is simple: when tank got hit by bullet, it will be eliminated. There are random bullets, also called wild bullets, ready to spawn and eliminate tank if there is no winner. Wild bullets will be more frequent to spawn, depends on how long the battle right now.

You can implement your tank bot by implementing TankBot. See `src/bot/SimpleTankBot` for an example.

## Installation
You just need [Python 3](https://www.python.org/downloads/) in your computer. Then, get the clone this repository and you are ready to go.

## Run
Go to te root of this program, and run this command:

```
py main.py
```

It will shows two tanks battle to survive. It's not interesting yet, by the way.

## Now what?
To make it interesting, try to implement your own bot! Implement it by create a new class inherits from `TankBot` at `src/bot/`, then import your bot to `src/App.py`. You can check `src/bot/SimpleTankBot.py` as an example.

To import, open `src/App.py`, then edit from this:
```
#######
# Put your bot here!
t1 = Tank(self.canvas, (255, 0, 0), 0, 0, bot=MyTankBot()) # <- Pay attention to this line.
t2 = Tank(self.canvas, (0, 0, 255), config.COL_COUNT - 1, config.ROW_COUNT - 1, bot=SimpleTankBot())
self.tanks = [t1, t2]
#######
```

to this:
```
#######
# Put your bot here!
t1 = Tank(self.canvas, (255, 0, 0), 0, 0, bot=YourTankBotClassName()) # <- Pay attention to this line.
t2 = Tank(self.canvas, (0, 0, 255), config.COL_COUNT - 1, config.ROW_COUNT - 1, bot=SimpleTankBot())
self.tanks = [t1, t2]
#######
```

When you see this code, you can also customize your tank color and initial position. The format goes like this:
```
# <...> means template. You need to change it.
t = Tank(
   self.canvas,
   (<red:0-255>, <green:0-255>, <blue:0-255>),
   <x-pos>,
   <y-pos>,
   bot=<class-name-of-your-bot>()
)
```

Have fun!