# Tank Battle Simulation

Tank Battle Simulation is a simple Python-Tkinter-based application for simulating tank battle. The rule of the battle is simple: when tank got hit by bullet, it will be eliminated. There are random bullets, also called wild bullets, ready to spawn and eliminate tank if there is no winner. Wild bullets will be more frequent to spawn, depends on how long the battle right now.


## Installation
You need [Python 3](https://www.python.org/downloads/) in your computer. Then, get the clone this repository.
Finally, you need to install `PyYaml` dependencies by run this command:

```
pip install PyYaml
```

## Run
Simple. Go to te root of this program, and run this command:

```
py main.py
```

## Now what?
To make it more interesting, try to implement your own bot! 

Implement it by create a new YAML document. This is the template:
```
first_action: <first-action-name>

actions:
    <action-name-1>:
        commands:
            -   "<command-1>"
            -   "<command-2>"
            # ... and so on.
            
        transitions:
            -   condition: "<condition-1>"
                next_action: <next-action-name-1>
                
            -   condition: "<condition-2>"
                next_action: <next-action-name-2>
                
            # ... and so on.
    
    <action-name-2>:
        commands:
            -   "<command-1>"
            -   "<command-2>"
            # ... and so on.
            
        transitions:
            -   condition: "<condition-1>"
                next_action: <next-action-name-1>
                
            -   condition: "<condition-2>"
                next_action: <next-action-name-2>
                
            # ... and so on.
            
    # ... and so on.
```

### Action
Action includes sequence of commands that should be executed first and transitions. You can name your action freely as long as does not break the YAML syntax. Snake case is recommended. You can say action as a state because it can changed after executing all commands and satisfy particular condition. Do not forget to set the `first_action` too!

### Command
Command determines what tank should do in current action. There are 9 types of commands right now:
- `"move north/south/east/west"`
- `"shoot north/south/east/west"`
- `"wait"`

Just pick one direction for `north/south/east/west`. For example, if your tank want to go north, use `"move north"` command.

`"wait"` is used if you want your tank to do nothing.

### Transition
Transition determines what is the next action of tank and it's condition. There are three type of condition:
- `"wall on north/south/east/west"`
- `"enemy on north/south/east/west"`
- `"any"`

`"any"` is used if you want your tank change state for any condition.

Note that ordering is important in transitions. Also, if there is no condition satisfied, it will stay to current action.

### Game Configuration
After YAML document for bot implemented, give your bot path to `game_config.yaml` by change the value of `bot_path`. You can use one bot for more than one tank.

Here is the example of `game_config.yaml`:
```
window_width: 640
window_height: 480
row_count: 15
col_count: 20
frame_rate: 8
delay_before_start: 3

teams:
    -   name: "Red Team"
        tanks:
            -   bot_path: "examples/bots/guard.yaml"
                initial_position: [0, 0]
                color: [255, 0, 0]
                
            -   bot_path: "examples/bots/defender.yaml"
                initial_position: [1, 1]
                color: [205, 0, 0]
                
            -   bot_path: "examples/bots/defender.yaml"
                initial_position: [2, 2]
                color: [155, 0, 0]
                
    -   name: "Blue Team"
        tanks:
            -   bot_path: "examples/bots/guard.yaml"
                initial_position: [14, 19]
                color: [0, 0, 255]
                
            -   bot_path: "examples/bots/attacker.yaml"
                initial_position: [13, 18]
                color: [0, 0, 205]
                
            -   bot_path: "examples/bots/attacker.yaml"
                initial_position: [12, 17]
                color: [0, 0, 155]
```


Have fun!

## Further development
Solo mode is not supported right now, and the program is not refactored yet. In the future, these issues, and maybe with new features, will be fixed.

## Note to the previous version
Because of this new DSL-feature, Python bot implementation is temporarily disabled. Sorry for the inconvenience. :(
