from threading import Thread
from time import sleep
from typing import List
import ctypes
import os
import json
import time

import requests as req
# disable proxy
requests = req.Session()
requests.trust_env = False
requests.verify = False
class TempSkeleton():

  '''
  reset(self)
  '''

  do_not_save_properties = [
    'unique_id',
    'folder_dir',
    'file_path',
  ]
  filename = 'empty.json'
  temp_name_for_display = 'TempSkeleton'
  def __init__(self, unique_id: str, temp_folder_dir: str = './temp', reset: bool = False):
    self.unique_id = unique_id
    if not os.path.exists(temp_folder_dir):
      os.makedirs(temp_folder_dir)
    self.folder_dir = f'./{temp_folder_dir}/{self.unique_id}'
    self.file_path = self.folder_dir + f'/{self.filename}'
    if reset is True:
      print(f'reset is True, resetting')
      self.reset()
    else:
      try:
        print(f'trying to load {self.temp_name_for_display} uid: {self.unique_id}')
        self.load()
        print(f'loaded {self.temp_name_for_display} uid: {self.unique_id}')
      except Exception:
        print(f'cant load {self.temp_name_for_display} uid: {self.unique_id}')
        print(f'creating new config for {self.temp_name_for_display} uid: {self.unique_id}')
        self.reset()
    self.customInit()
  def customInit(self):
    return False
  def reset(self):
    self.key = 'value'
    self.save()
  def load(self):
    if not os.path.exists(self.folder_dir):
      os.makedirs(self.folder_dir)
    file = open(self.file_path, encoding='utf-8')
    config = json.load(file)
    file.close()
    # assign
    self.fromJson(config)
  def save(self):
    file = open(self.file_path, 'w', encoding='utf-8')
    json_to_save = self.toJson()
    time_now = time.time()
    json_to_save['update_time'] = time_now 
    self.update_time = time_now
    json.dump(json_to_save, file, ensure_ascii=False, indent=4)
    file.close()
  def toJson(self):
    some_dict = copy.copy(vars(self))
    for key in self.do_not_save_properties:
      del some_dict[key]
    return some_dict

  def fromJson(self, config:dict):
    for key, value in config.items():
      setattr(self, key, value )
    # self.stash_tabs_data = config['stash_tabs_data']
class LauncherMapConfigs(TempSkeleton):
  # TODO supposed to be part of global temp, smth like temp["simulacrum"]
  filename = 'mapper_configs.json'
  temp_name_for_display = 'LauncherMapConfigs'

  def reset(self):
    self.mapper_configs = {}
    self.save()
def eternalSleep(msg:str=None):
  if msg:
    print(msg) 
  input("Press enter to close the script")
  exit(1)
def checkIfWindowsLengthLimitDisabled():
  ntdll = ctypes.WinDLL('ntdll')
  if hasattr(ntdll, 'RtlAreLongPathsEnabled'):
    ntdll.RtlAreLongPathsEnabled.restype = ctypes.c_ubyte
    ntdll.RtlAreLongPathsEnabled.argtypes = ()
    def are_long_paths_enabled():
      return bool(ntdll.RtlAreLongPathsEnabled())
  else:
      def are_long_paths_enabled():
        return False
  if are_long_paths_enabled() is False:
    print('windows disable path length limit and restart script')
    print('https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/The-Windows-10-default-path-length-limitation-MAX-PATH-is-256-characters.html')
    print('windows disable path length limit and restart script')
    eternalSleep()
  return 
# load keys and ip from file
# send to coordinator
# coordinator sends back json with 
# - updated configs
# - workers parameters
# update configs if changed
# for worker in workers
#   if worker doesnt exist: new worker thread with parameters
#   if worker command "stop" - wait till script is finished and dont run it anymore
class Launcher:
  all_threads:List[Thread] = []
  def __init__(self, coordinator_ip) -> None:
    checkIfWindowsLengthLimitDisabled()
    self.coordinator_ip:str = coordinator_ip
    self.key_ip_pairs = {}
    self.keys_file_path = "./launcher_keys.txt"
    self.coordinator_timeout = 15
    self.running = False
    self.ready = False
    self.configs = LauncherMapConfigs("launcher")

    self.main_thread:Thread = None
  def start(self):
    print("[launcher] starting")
    self.main_thread = Thread(target=lambda: self.mainThread())
    self.main_thread.start()
    while not self.ready:
      print(f'[launcher] waiting till ready')
      sleep(1)
    print("[launcher] started")
  def stop(self):
    print("[launcher] stopping")
    self.running = False
    # list(map(lambda t: t.stop(), self.all_threads))
    print("[launcher] stopped")
  def mainThread(self):
    self.running = True
    url = f'{self.coordinator_ip}/api/workers/updateAndGetJobs'
    failures_count = 0
    while self.running:
      self.updateKeys()
      try:
        res = requests.post(url, json=self.key_ip_pairs, timeout=3)
        data = res.json()
        print(f'config {data}')
        self.updateConfigs(data['configs'])
        self.updateJobs(data['worker_jobs'])
      except Exception:
        failures_count+=1
        print(f'couldnt parse json from {url} failures_count {failures_count}')
        if failures_count == 10:
          self.stop()
          raise Exception(f'couldnot parse config from {self.coordinator_ip}')
      
      self.ready = True
      for i in range(self.coordinator_timeout):
        if self.running is False:
          break
        sleep(1)

  def updateJobs(self, data:dict):
    pass

  def updateConfigs(self, data:dict):
    configs_changed = False
    if self.configs.mapper_configs == {}:
      print(f'updating mapper_configs empty')
      self.configs.mapper_configs = data["mapper_configs"]
      configs_changed = True
    else:
      if self.configs.mapper_configs != data['mapper_configs']:
        print(f'updating mapper_configs different')
        self.configs.mapper_configs = data["mapper_configs"]
        configs_changed = True

    if configs_changed:
      self.configs.save()
  def updateKeys(self):
    print('updating keys')
    f = open(self.keys_file_path, encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
      splitted_line = line.split("=")
      if len(splitted_line) != 2:
        print(f'ignoring line {line}, incorrect format, supposed to be *mzxcjasiqwe=192.192.192.192*')
        continue
      key = splitted_line[0]
      ip = splitted_line[1]
      self.key_ip_pairs[key] = ip
    print('updated keys')
    self.ready = True
    return True

