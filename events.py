from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key, KeyCode
import pyautogui
import socket
import time
import threading
import os


'''
Events listen to mouse and keyboard activity
If the virtual keyboard connects to Events through socket, virtual keyboard will
show what key is being pressed and mouse position.
'''

class Events:
  def __init__(self, log_filename = None):
    self.host = '127.0.0.1'      # The server's hostname or IP address
    self.port = 12001            # The port used by the server
    
    if log_filename != None: self.log = open(log_filename, "w")
    else: self.log = None

    # Create the key map to match to how keyboard.py to store each key board buttons
    # multiple names for one key
    key_map = {
      KeyCode.from_char('~'): '`',
      KeyCode.from_char('`'): '`',
      KeyCode.from_char('!'): '1',
      KeyCode.from_char('@'): '2',
      KeyCode.from_char('#'): '3',
      KeyCode.from_char('$'): '4',
      KeyCode.from_char('%'): '5',
      KeyCode.from_char('^'): '6',
      KeyCode.from_char('&'): '7',
      KeyCode.from_char('*'): '8',
      KeyCode.from_char('('): '9',
      KeyCode.from_char(')'): '0',
      KeyCode.from_char('-'): '_',
      KeyCode.from_char('_'): '_',
      KeyCode.from_char('='): '=',
      KeyCode.from_char('+'): '=',
      KeyCode.from_char('['): '[',
      KeyCode.from_char('{'): '[',
      KeyCode.from_char(']'): ']',
      KeyCode.from_char('}'): ']',
      KeyCode.from_char('\\'): '\\',
      KeyCode.from_char('|'): '\\',
      KeyCode.from_char(';'): ';',
      KeyCode.from_char(':'): ';',
      KeyCode.from_char("'"): "'", 
      KeyCode.from_char('"'): "'",
      KeyCode.from_char(','): ',',
      KeyCode.from_char('<'): ',',
      KeyCode.from_char('.'): '.',
      KeyCode.from_char('>'): '.',
      KeyCode.from_char('/'): '/',
      KeyCode.from_char('?'): '/',
    }

    # letters 
    for i in range(26):
      l = chr(ord('a') + i)
      u = chr(ord('A') + i)
      ctrl_combo = chr(i + 1)
      key_map[KeyCode.from_char(l)] = l
      key_map[KeyCode.from_char(u)] = u
      key_map[KeyCode.from_char(ctrl_combo)] = u

    # CTRL + key
    key_map[KeyCode.from_char(chr(27))] = '['
    key_map[KeyCode.from_char(chr(28))] = '\\'
    key_map[KeyCode.from_char(chr(29))] = ']'
    key_map[KeyCode.from_char(chr(30))] = '^'
    key_map[KeyCode.from_char(chr(31))] = '-'


    # ALT + key - to do
    key_map[KeyCode.from_char('¡')] = '1'
    key_map[KeyCode.from_char('™')] = '2'
    key_map[KeyCode.from_char('£')] = '3'


    # Key enum
    key_map[Key.esc] = 'esc'
    key_map[Key.f1] = 'f1'
    key_map[Key.f2] = 'f2'
    key_map[Key.f3] = 'f3'
    key_map[Key.f4] = 'f4'
    key_map[Key.f5] = 'f5'
    key_map[Key.f6] = 'f6'
    key_map[Key.f7] = 'f7'
    key_map[Key.f8] = 'f8'
    key_map[Key.f9] = 'f9'
    key_map[Key.f10] = 'f10'
    key_map[Key.f11] = 'f11'
    key_map[Key.f12] = 'f12'
    key_map[Key.home] = 'home'
    key_map[Key.backspace] = 'backspace'
    key_map[Key.tab] = 'tab'
    key_map[Key.caps_lock] = 'capslock'
    key_map[Key.enter] = 'enter'
    key_map[Key.shift] = 'shift'
    key_map[Key.shift_r] = 'shift'
    key_map[Key.ctrl] = 'ctrl'
    key_map[Key.alt] = 'alt'
    key_map[Key.cmd] = 'command'
    key_map[Key.space] = 'space'
    key_map[Key.cmd_r] = 'command'
    key_map[Key.alt_r] = 'alt'
    key_map[Key.left] = 'left'
    key_map[Key.right] = 'right'
    key_map[Key.up] = 'up'
    key_map[Key.down] = 'down'


    # NUMBER
    for i in range(10): 
      c = chr(ord('0') + i)
      key_map[KeyCode.from_char(c)] = i

    self.key_map = key_map

    # get all key values
    self.is_pressed = {}
    for val in self.key_map.values():
      self.is_pressed[val] = False

    # get screen and image size
    self.screen_width, self.screen_hegiht = pyautogui.size()
    im = pyautogui.screenshot()
    self.img_width, self.img_height = im.size
    self.width_ratio = self.img_width / self.screen_width
    self.height_ratio = self.img_height / self.screen_hegiht
    self.client = None
    self.starting_time = time.time()


  def accept_connections(self):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((self.host, self.port))
    serv.listen()
    while True:
      self.client, addr = serv.accept()
      print("accept the connections")

    serv.close()

  def key_map_func(self, key):
    
    if key == None: return "fn"
    if key in self.key_map: return self.key_map[key]
    return None

  def on_press(self, key):
    # print("P {} {}".format(key, self.key_map_func(key)))

    key = self.key_map_func(key)
    print(key)
    if key != None and self.is_pressed[key] == False:
      try :
        self.is_pressed[key] = True
        if self.is_pressed['esc'] and self.is_pressed['ctrl']:
          if self.log: self.log.close()
          self.client = None
          self.log = None
          print("Exit", flush= True)
          os._exit(1)
          return False

        self.write_log("PRESS {0} {1:.3f}\n".format(key, time.time() - self.starting_time))
        if self.client != None: self.client.send("PRESS-{0}-".format(key).encode('utf-8'))
      except Exception:
        self.client.close()
        self.client = None
  

  def on_release(self, key):

    
    # print("RELEASE {} {}".format(key, self.key_map_func(key)))
    key = self.key_map_func(key)
    if key != None:
      try:
        self.is_pressed[key] = False
        self.write_log("RELEASE {0} {1:.3f}\n".format(key, time.time() - self.starting_time))
        if self.client != None: self.client.send("RELEASE-{0}-".format(key).encode('utf-8'))
      except Exception:
        self.client.close()
        self.client = None
    
 

  def on_move(self, x, y): 
    
    try:
      self.write_log("POS {0:.1f} {1:.1f} {2:.3f}\n".format(x, y, time.time() - self.starting_time))
      if self.client != None: self.client.send("POS-({0:.1f}, {1:.1f})-".format(x, y).encode('utf-8'))

    except Exception:
      self.client.close()
      self.client = None
    

  def on_click(self, x, y, button, pressed): 
    
    if pressed:
      actual_x = int(x * self.width_ratio)
      actual_y = int(y * self.height_ratio)
      if actual_x >= self.img_width: actual_x = self.img_width - 1
      if actual_y >= self.img_height: actual_y = self.img_height - 1
      p = pyautogui.pixel(actual_x, actual_y)
      
      try :
       self.write_log("CLICK {0:.1f} {1:.1f} {2:.3f}\n".format(x, y, time.time() - self.starting_time))
       if self.client != None: self.client.send("CLICK-({0:.1f}, {1:.1f})-RGB({2}, {3}, {4})-".format(x, y, p.red, p.green, p.blue).encode('utf-8'))

      except Exception:
        self.client.close()
        self.client = None

  
  def write_log(self, log_content):
    if self.log != None: 
      self.log.write(log_content)
      self.log.flush()
      

  def on_scroll(self, x, y, dx, dy):
    pass
    # print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

  def listen(self):
    self.server = threading.Thread(target=self.accept_connections)
    self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
    self.mouse_listener = MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
    self.keyboard_listener.start()
    self.mouse_listener.start()
    self.server.start()

  def join(self):
    self.keyboard_listener.join()
    self.mouse_listener.join()
    self.server.join()



def execute_log(log_filename):

  a = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
      ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
      '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
      'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
      'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
      'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
      'browserback', 'browserfavorites', 'browserforward', 'browserhome',
      'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
      'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
      'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
      'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
      'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
      'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
      'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
      'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
      'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
      'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
      'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
      'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
      'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
      'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
      'command', 'option', 'optionleft', 'optionright']


  time.sleep(1)
  # for k in a:
  # k = "ctrlright"
  # pyautogui.keyDown(k, _pause=False)
  # pyautogui.keyUp(k, _pause=False)
    # print("{} ".format(k), end = "")




  f = open(log_filename, "r")
 
  lines = []
  while True:
    line = f.readline()
    if (not line): break
    lines.append(line)
  f.close()

  prev_x = -10000
  prev_y = -10000
  threshold = 10
  t = time.time()
  for line in lines:
    l = line.split()
    actual_rt = float(l[len(l) - 1])
    rt = time.time() - t
    if actual_rt > rt: time.sleep(actual_rt - rt)

    if l[0] == "POS":
      x, y = float(l[1]), float(l[2])
      if (x - prev_x)**2 + (y - prev_y)**2 > threshold**2:
        # print(x, y, time.time() - t)
        pyautogui.moveTo(x, y, _pause=False) 
        prev_x, prev_y = x, y

    elif l[0] == "CLICK":
      x, y = float(l[1]), float(l[2])
      pyautogui.click(x, y, _pause = False)

    elif l[0] == "PRESS":
      pyautogui.keyDown(l[1])

    elif l[0] == "RELEASE":
      pyautogui.keyUp(l[1])


events = Events()
events.listen()
# execute_log("junk.txt")
events.join()




