import socket
import numpy as np
from utils import Controller, grabScreen, sortByHSV
from tkinter import Tk
import win32clipboard
import os
import time
import uuid
import requests as req
import _thread
import struct
requests = req.Session()
requests.trust_env = False

import json
from ctypes import windll

import subprocess
import win32gui

controller = Controller()

def getWindowLoc(window_name: str):
  try:
    hwnd = win32gui.FindWindow(None, window_name)
    rect = win32gui.GetWindowRect(hwnd)
    return rect
  except:
    return None

def processExists(process_name):
  call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
  # use buildin check_output right away
  output = subprocess.check_output(call).decode()
  # check in last line for process name
  last_line = output.strip().split('\r\n')[-1]
  # because Fail message could be translated
  return last_line.lower().startswith(process_name.lower())


try:
    import cPickle as pickle
except ImportError:
    import pickle

def getParam(action_msg: str, param: str):
  return action_msg.split(f'{param}=')[1].split('&')[0]

coordinator_uri = None


temp = {

}

def loadTemp():
  file = open('./temp.json', encoding='utf-8')
  config = json.load(file)
  file.close()
  global temp
  temp = config

def updateTemp():
  file = open('./temp.json', 'w', encoding='utf-8')
  json.dump(temp, file, ensure_ascii=False, indent=4)
  file.close()

try:
  loadTemp()
except:
  pass


def findCoordinator():
  print(f'looking for coordinator')
  global coordinator_uri
  for i in range(0,255):
    if coordinator_uri is not None: break
    for o in range(0,255):
      if coordinator_uri is not None: break
      uri = f'http://192.168.{i}.{o}:54321'
      try:
        # print(f'looking for coordinator on {uri}')
        response = requests.get(uri+"/ping", timeout=0.01)
      except:
        continue
      if response.text == "coordinator":
        coordinator_uri = uri
        print(f'new coordinator url {coordinator_uri}')

def notifyCoordinator(host,mac_address_hex):
  while True:
    if coordinator_uri is None:
      findCoordinator()
    uri = f'{coordinator_uri}'
    try:
      response = requests.get(uri+f"/getNotificationFromWorker?ip={host}&unique_id={mac_address_hex}", timeout=0.001)
      print(f'successfully notified the coordinator')
    except:
      print(f'unable to notify the coordinator')
      findCoordinator()
      pass
    time.sleep(30)

default_ok_response = b'1'

def Main():
  mac_address = uuid.getnode()
  mac_address_hex = ''.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
  port = 50007
  host = '0.0.0.0'
  HOST = socket.gethostbyname(socket.gethostname())
  print(f'[Worker] host:port {HOST}:{port} mac_adress: {mac_address_hex}')
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((host,port))
  print(f"[Worker] Started on {HOST}:{port}")
  s.listen(1)
  c, addr = s.accept()
  print("[Worker] established connection with: " + str(addr))
  s.close()

  def sendBytes(file:bytes):
    file_len = len(file)
    data_size = struct.pack('>I', file_len)
    print(f'[Worker] sending bytes {data_size} {file_len}')
    c.sendall(data_size)
    c.sendall(img)

  while True:
    action_msg = c.recv(1024).decode()
    ### FROM HERE
    print(f"got action {time.time()}:" + action_msg)
    action = action_msg.split('action=')[1].split('&')[0]
    wait_till_recieved = len(action_msg.split("wtr=1&")) != 1
    if wait_till_recieved: c.send(default_ok_response)
    if action == 'mouseClick':
      x = action_msg.split('x=')[1].split('&')[0]
      y = action_msg.split('y=')[1].split('&')[0]
      button = action_msg.split('button=')[1].split('&')[0]
      controller.mouse.click(int(x),int(y), button)
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'mouseSetCursorPos':
      x = action_msg.split('x=')[1].split('&')[0]
      y = action_msg.split('y=')[1].split('&')[0]
      controller.mouse.setCursorPos(int(x),int(y))
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'mouseSetCursorPosSmooth':
      x = action_msg.split('x=')[1].split('&')[0]
      y = action_msg.split('y=')[1].split('&')[0]
      max_time_ms = action_msg.split('mtm=')[1].split('&')[0]
      mouse_speed_mult = action_msg.split('msm=')[1].split('&')[0]
      controller.mouse.setCursorPosSmooth(int(x),int(y), int(max_time_ms), int(mouse_speed_mult))
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'mousePress':
      x = action_msg.split('x=')[1].split('&')[0]
      y = action_msg.split('y=')[1].split('&')[0]
      button = action_msg.split('button=')[1].split('&')[0]
      controller.mouse.press(int(x),int(y), button)
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'mouseRelease':
      button = action_msg.split('button=')[1].split('&')[0]
      controller.mouse.release(button=button)
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'pushButton':
      button_code = action_msg.split('button_code=')[1].split('&')[0]
      controller.keyboard.tapButton(button_code)
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'keyboard_pressKey':
      button_code = action_msg.split('button_code=')[1].split('&')[0]
      controller.keyboard.pressKey(button_code)
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'keyboard_releaseKey':
      button_code = action_msg.split('button_code=')[1].split('&')[0]
      controller.keyboard.releaseKey(button_code)
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'executeCMD':
      task = action_msg.split('task=')[1].split('&')[0]
      os.system(f'cmd /c "{task}"')
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'taskKill':
      task_name = action_msg.split('task_name=')[1].split('&')[0]
      os.system(f'cmd /c "taskkill /IM  {task_name} /F"')
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'setClipboardText':
      clipboard_text = action_msg.split('clipboard_text=')[1].split('&')[0]
      win32clipboard.OpenClipboard()
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardText( clipboard_text, win32clipboard.CF_TEXT )
      win32clipboard.CloseClipboard()
      if wait_till_recieved != True: c.send(default_ok_response)
    elif action == 'restartScript':
      print('[Worker] got restart script')
      if wait_till_recieved != True: c.send(default_ok_response)
      c.close()
      break
    elif action == 'releaseAll':
      controller.releaseAll()
      if wait_till_recieved != True: c.send(default_ok_response)


    elif action == 'getFullScreen':

      img = grabScreen()
      img = pickle.dumps(img)
      sendBytes(img)
    elif action == 'getPartialScreen':
      x1 = int( action_msg.split('x1=')[1].split('&')[0])
      y1 = int( action_msg.split('y1=')[1].split('&')[0])
      x2 = int( action_msg.split('x2=')[1].split('&')[0])
      y2 = int( action_msg.split('y2=')[1].split('&')[0])
      got_screen = False
      for i in range(10):
        print(f'grabbing the screen iter number {i}')
        try:
          img = grabScreen((x1,y1,x2,y2))
          got_screen = True
          break
        except: 
          print('couldnt grab the screen')
          
      if got_screen is False:
        raise 'couldnt grab the screen'
      img = pickle.dumps(img)
      sendBytes(img)
    elif action == 'getSortedByHSV':
      x1 = int( action_msg.split('x1=')[1].split('&')[0])
      y1 = int( action_msg.split('y1=')[1].split('&')[0])
      x2 = int( action_msg.split('x2=')[1].split('&')[0])
      y2 = int( action_msg.split('y2=')[1].split('&')[0])
      
      h1 = int( action_msg.split('h1=')[1].split('&')[0])
      s1 = int( action_msg.split('s1=')[1].split('&')[0])
      v1 = int( action_msg.split('v1=')[1].split('&')[0])
      h2 = int( action_msg.split('h2=')[1].split('&')[0])
      s2 = int( getParam(action_msg, 's2'))
      v2 = int( getParam(action_msg, 'v2'))
      img = grabScreen((x1,y1,x2,y2))
      sorted_hsv = sortByHSV(img,0,255,240,255,255,255)
      data = np.where(sorted_hsv != 0)
      coords = list(zip(data[0], data[1]))
      coords_pickled = pickle.dumps(coords)
      sendBytes(coords_pickled)
    elif action == 'processExists':
      process_name = action_msg.split('process_name=')[1].split('&')[0]
      res = processExists(process_name)
      c.sendall(res)
    elif action == 'getWindowLoc':
      process_name = action_msg.split('window_name=')[1].split('&')[0]
      window_location = getWindowLoc(process_name)
      window_location = pickle.dumps(window_location)
      sendBytes(window_location)
    elif action == 'getClipboardText':
      clipboard_text = None
      try:
        clipboard_text = Tk().clipboard_get()
      except:
        print('no text in a clipboard')
        clipboard_text = None
      data = pickle.dumps(clipboard_text)
      if windll.user32.OpenClipboard(None):
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()
      sendBytes(data)

    elif action == 'checkProxy':
      is_working = False
      try:
        url = 'http://google.com'
        proxies = {
          "http": "http://127.0.0.1:34567",
          "https": "https://127.0.0.1:34567",
        }
        requests.get(url,proxies=proxies, timeout=2)
        is_working = True

      except:
        is_working = False
      data = pickle.dumps(is_working)
      sendBytes(data)
    else:
      print(f'got unknown action: {action}')
      if wait_till_recieved != True: c.send(default_ok_response)


try:
  Main()
except:
  print('releasing all buttons')
  controller.releaseAll()

