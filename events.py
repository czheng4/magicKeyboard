from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key, KeyCode
import pyautogui
import socket



class Events:
  def __init__(self):
    self.host = '127.0.0.1'  # The server's hostname or IP address
    self.port = 12001        # The port used by the server

    # multiple names for one key
    key_map = {
      KeyCode.from_char('~'): '`',
      KeyCode.from_char('!'): 1,
      KeyCode.from_char('@'): 2,
      KeyCode.from_char('#'): 3,
      KeyCode.from_char('$'): 4,
      KeyCode.from_char('%'): 5,
      KeyCode.from_char('^'): 6,
      KeyCode.from_char('&'): 7,
      KeyCode.from_char('*'): 8,
      KeyCode.from_char('('): 9,
      KeyCode.from_char(')'): 0,
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
      key_map[KeyCode.from_char(l)] = u
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


    # NUMBER
    for i in range(10): 
      c = chr(ord('0') + i)
      key_map[KeyCode.from_char(c)] = i

    self.key_map = key_map

    self.screen_width, self.screen_hegiht = pyautogui.size()
    im = pyautogui.screenshot()
    self.img_width, self.img_height = im.size
    self.width_ratio = self.img_width / self.screen_width
    self.height_ratio = self.img_height / self.screen_hegiht


    # connect to keyboard.py
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    trying = 1
    while trying:
      try:
        self.client.connect((self.host, self.port))
        trying = 0
      except Exception:
        trying = 1

  def key_map_func(self, key):
    if (isinstance(key, Key)): return key
    else: 
      if key == None: return "fn"
      if key in self.key_map: return self.key_map[key]
      return None

  def on_press(self, key):
    

    key = self.key_map_func(key)
    if (key != None):
      try :
        self.client.send("PRESS-{0}-".format(key).encode('utf-8'))
      except Exception:
        self.client.close()
        return False

  def on_release(self, key):

    
    key = self.key_map_func(key)
    if (key != None):
      try :
        self.client.send("RELEASE-{0}-".format(key).encode('utf-8'))
      except Exception:
        self.client.close()
        return False   

  def on_move(self, x, y): 
    
    try :
      self.client.send("POS-({0:.1f}, {1:.1f})-".format(x, y).encode('utf-8'))
    except Exception:
      self.client.close()
      return False   


  def on_click(self, x, y, button, pressed): 
    

    if pressed:
      actual_x = int(x * self.width_ratio)
      actual_y = int(y * self.height_ratio)
      if actual_x >= self.img_width: actual_x = self.img_width - 1
      if actual_y >= self.img_height: actual_y = self.img_height - 1
      p = pyautogui.pixel(actual_x, actual_y)
      try :
        self.client.send("CLICK-({0:.1f}, {1:.1f})-RGB({2}, {3}, {4})-".format(x, y, p.red, p.green, p.blue).encode('utf-8'))
      except Exception:
        self.client.close()
        return False   
      

  def on_scroll(self, x, y, dx, dy):
    pass
    # print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

  def listen(self):
    self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
    self.mouse_listener = MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
    self.keyboard_listener.start()
    self.mouse_listener.start()

  def join(self):
    self.keyboard_listener.join()
    self.mouse_listener.join()


events = Events()
events.listen()
events.join()



