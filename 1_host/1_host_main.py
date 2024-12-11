import sys
import time
import random
import _thread
import subprocess
import os
import requests

from utils.controller import VMHostPuppeteer
from utils.temps import StashTempData





workers_dict = {

}



class Worker:
  status = 'sleep'
  thread = None
  process = None
  script = None
  last_msg = ''
  def __init__(self, data: dict) -> None:
    unique_id, remote_ip, script = data['unique_id'], data['remote_ip'], data['script']
    self.unique_id = unique_id
    self.remote_ip = remote_ip
    self.script = data['script']
  
  def start(self):
    '''
    main thread
    '''
    while self.script != 'sleep' and self.status != 'sleep':
      current_dir = os.path.dirname(os.path.realpath(__file__))
      cmd_command = f"python {current_dir}\\{self.script}.py {self.remote_ip} {self.unique_id}" #TODO params
      print(f"{self.unique_id} executing command {cmd_command}")
      process = subprocess.Popen(cmd_command.split(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      while True:
        if self.status == 'sleep':
          print(f'{self.unique_id} self.status changed to "sleep"')
          break
        time.sleep(0.01)
        line = process.stdout.readline().decode('utf-8')
        # (stdout, stderr) = process.communicate()
        if line != '':
          self.last_msg = line
          print(f'{self.unique_id} Line: {line[:-2]}') # :-2 to remove \n or \t or whatever is there
          # continue # TODO need?
        #check if process is still running
        process_is_running = process.poll() is None
        print(f"{self.unique_id} process_is_running {process_is_running}")
        if process_is_running == False:
          print(f"{self.unique_id} rerunning the process")
          break 
    return
    
  def stop(self):
    pass

  def do(self,action = None):
    if self.script == 'sleep':
      # stop script if possible
      self.status = 'sleep'
      self.thread = None
      return
    elif self.script != 'sleep' and self.thread is None:
      self.status = 'running'
      print(f'{self.unique_id} starting new thread')
      self.thread = _thread.start_new_thread(self.start, ())
      print(f'{self.unique_id} started new thread')
      return 
    
    
def getListOfThisMachineGuestsMacAddresses():
  '''
  returns [mac_address] under this host
  '''
  mac_adresses = [
    "00E04CF42DB6",
    "00E04C1BCB8E",
    "00E04C000001",
    "00E04C000002",
    "00E04C000003",
  ]
 
  # TODO cmd_command = 'powershell -command "Get-VM | Get-VMNetworkAdapter | ft MacAddress"    '


  return mac_adresses


def getDataFromCoordinator():
  '''
  get currenct status of jobs, related workers
  '''
  coordinator_response = [
    {
      "unique_id": "5XBYN26LML123123PJ6V2J",
      "remote_ip": "192.168.0.104",
      "assigned_script" : "dummy_script",
      "status" : "sleep"
    },
    {
      "unique_id": "1924934893288fdsau",
      "remote_ip": "192.168.0.105",
      "assigned_script" : "dummy_script",
      "status" : "sleep"
    }
  ]

  # TODO
  # r = requests.get(coordinator_url)
  # data = r.json()
  # TODO sort jobs, get assigned jobs for this machine, so it may be mac adresses under this machine 
  # and also some physical workers assigned for this machine


  return coordinator_response

MAC_ADDRESSES = getListOfThisMachineGuestsMacAddresses()

while True:
  
  jobs = getDataFromCoordinator()
  for job in jobs:
    # check if the worker was initialized
    try:
      workers_dict[job['unique_id']]
    except:
      workers_dict[job['unique_id']] = Worker(job)
    
    worker:Worker = workers_dict[job['unique_id']]
    #update job
    worker.script = job['script']
    worker.do(job['script'])


  time.sleep(5)
