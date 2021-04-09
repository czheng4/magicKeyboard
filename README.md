# magicKeyboard
This is a virtual keyboard monitor. I wrote this program for several purposes.
1. You can definitely use this to learn typing.
2. The application also monitors the pixel value. You can use this to extract pixel value from your screen easily
3. Make your task auto. The virtual keyboard can record your keyboard and mouse activity, and save them. You can load
this file to repeat the activity.
4. Most importantly, I made this to see how game bot controls the keyboard and mouse for the purpose of debugging.

## Install required lib

```
UNIX> pip install -r requirements.txt
```

## Monitor the mouse and keyboard events
We can save the activity by running the following. Press "CTRL" + "ESC" to stop the program.
```
UNIX> python events.py -s my_events.txt
```

Repeat the activity by running 
```
UNIX> python events.py -l my_events.txt
```

## Run the virtual keyboard

If you wanna see what key is being pressed. Launch the virtual keyboard by doing the following. `keyboard.py` communicates with `events.py` through socket.
```
UNIX> python keyboard.py
```


