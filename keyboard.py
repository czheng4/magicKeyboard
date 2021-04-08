import sys
import time
from pynput.keyboard import Key, Listener, KeyCode
from pynput import mouse
from time import sleep

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtCore import QMutex, QObject, QThread, pyqtSignal, Qt
import socket




class Worker(QObject):
  finished = pyqtSignal()
  progress = pyqtSignal(bytes)

  def run(self):

    host = '127.0.0.1'
    port = 12001

    # create the server 
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((host, port))
    serv.listen()
    conn, addr = serv.accept()

    # reading events
    while True:
      data = conn.recv(256)
      if (data == b""): break;
      self.progress.emit(data)

    # close the socket
    conn.close()
    self.finished.emit()
    
 


class Keyboard:
  def __init__(self):
    self.key_names = [
      ["esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F2", "home"],
      ["~\n`", "!\n1", "@\n2", "#\n3", "$\n4", "%\n5", "^\n6", "&&\n7", "*\n8", "(\n9", ")\n0", "_\n-", "+\n=", "delete"],
      ["tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{\n[", "}\n]", "|\n\\"],
      ["caps lock", 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ":\n;", "\"\n'", "return"],
      ["shift", 'Z', 'X', 'C', 'V', 'B', 'N', 'M', "<\n,", ">\n.", "?\n/", "shift"],
      ["fn", "control", "option", "command", "space", "command", "option", "left", "up", "down", "right"]
    ]

    self.actual_keys = [ 
      ["Key.esc", "Key.f1", "Key.f2", "Key.f3", "Key.f4", "Key.f5", "Key.f6", "Key.f7", "Key.f8", "Key.f9", "Key.f10", "Key.f11", "Key.f12", "Key.home"], 
      ['~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '=', "Key.backspace"],
      ["Key.tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", '[', ']', '\\'],
      ["Key.caps_lock", 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ";", "'", "Key.enter"],
      ["Key.shift", 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ",", ".", "/", "Key.shift_r"],
      ["fn", "Key.ctrl", "Key.alt", "Key.cmd", "Key.space", "Key.cmd_r", "Key.alt_r", "Key.left", "Key.up", "Key.down", "Key.right"]
    ]

    self.app = QApplication([])
    self.window = QWidget()
    self.window.setWindowTitle("Keyboard")
    self.window.setGeometry(100, 100, 1060, 600)
    self.window.setStyleSheet("background-color:silver")
    self.buttons = {}



  def getUpdate(self):
   
    self.thread = QThread()
    self.worker = Worker()
    self.worker.moveToThread(self.thread)

    # Connect signals and slots
    self.thread.started.connect(self.worker.run)
    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.worker.progress.connect(self.reportProgress)
    self.thread.start()

    self.thread.finished.connect(
      lambda: self.window.close()
    )

  def reportProgress(self, b):
    s = b.decode('utf-8').split('-')
    i = 0
    while (i < len(s)):
      if s[i] == "PRESS":
        self.buttons[s[i+1]].setStyleSheet("font-size:15px; border-radius: 5px; background-color: rgb(170, 170, 170)")
        i+=1
      elif s[i] == "RELEASE":
        self.buttons[s[i+1]].setStyleSheet("font-size:15px; border-radius: 5px; background-color: rgb(230,230,230)")
        i+=1
      elif s[i] == "CLICK":
        self.click.setText("Click at: {} {}".format(s[i+1], s[i+2]))
        i+=2
      elif s[i] == "POS":
        self.cursor.setText("Mouse Position: {}".format(s[i+1]))
        i+=1
      i+=1


  def display(self):

    y = 20
    for rows,rows2 in zip(self.key_names, self.actual_keys):
      x = 20
      for key, actual_key in zip(rows, rows2):
        button = QPushButton(key, parent = self.window)

        button.move(x, y)
        
        self.buttons[actual_key] = button

        if key == "delete" or key == "esc" or key == "tab": 
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 100px; height: 65px; background-color: rgb(230,230,230)")
          x += 100 + 5

        elif key == "caps lock" or key == "return":
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 117.5px; height: 65px; background-color: rgb(230,230,230)")
          x += 117.5 + 5

        elif key == "shift":
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 152.5px; height: 65px; background-color: rgb(230,230,230)")
          x += 152.5 + 5

        elif key == "space":
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 345px; height: 65px; background-color: rgb(230,230,230)")
          x += 345 + 5

        elif key == "command":
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 82.5px; height: 65px; background-color: rgb(230,230,230)")
          x += 82.5 + 5

        elif key == "left":
          button.move(x, y + 35)
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 65px; height: 30px; background-color: rgb(230,230,230)")
          x += 65 + 5

        elif key == "right":
          button.move(x, y + 35)
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 65px; height: 30px; background-color: rgb(230,230,230)")

        elif key == "up":
          button.move(x, y)
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 65px; height: 30px; background-color: rgb(230,230,230)")

        elif key == "down":
          
          button.move(x, y + 35)
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 65px; height: 30px; background-color: rgb(230,230,230)")
          x += 65 + 5

        else:
          button.setStyleSheet("font-size:15px; border-radius: 5px; width: 65px; height: 65px; background-color: rgb(230,230,230)")
          x += 65 + 5
      y += 70

    y += 15
    x = 20
    self.cursor = QLabel("Mouse Position:" , parent = self.window)
    self.cursor.resize(400, 20)
    self.cursor.setStyleSheet("font-size:15px")
    self.cursor.move(x, y)

    y += 30
    self.click = QLabel("Click at:" , parent = self.window)
    self.click.resize(400, 20)
    self.click.setStyleSheet("font-size:15px")
    self.click.move(x, y)
    self.getUpdate()

    self.window.show()
    sys.exit(self.app.exec_())


keyboard = Keyboard()
keyboard.display()




