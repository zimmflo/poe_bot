from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
  from .gamehelper import PoeBot

import requests as req
# disable proxy
requests = req.Session()
requests.trust_env = False

class Coordinator():
  poe_bot: PoeBot

  coordinator_endpoint: str
  
  def __init__(self, poe_bot:PoeBot, coordinator_ip = '127.0.0.1') -> None:
    self.poe_bot = poe_bot
    if coordinator_ip is not None:
      self.can_send_msges = True
      self.coordinator_endpoint = f"http://{coordinator_ip}:44321"
    else:
      self.can_send_msges = False
    self.connection_established:bool = None


  def sendMessage(self, message_text:str):
    payload = {
      "uid": self.poe_bot.unique_id,
      "message": message_text
    }
    ping_url = self.coordinator_endpoint+"/sendMessage"
    requests.get(ping_url, data=payload)

  def sendUpdateMessage(self, message):
    pass

  def sendErrorMessage(self, message):
    pass

  def checkIfCanBeExecuted(self):
    if self.coordinator_endpoint == "":
      print(f'coodrinator_ip is not specified, cannot use coordinator functions')
      return False
    
    if self.connection_established is None:
      ping_url = self.coordinator_endpoint+"/ping"
      res = requests.get(ping_url)
      data = res.json()
      if data:
        self.connection_established = True
      else:
        self.connection_established = False
    return self.connection_established
  def getNinjaPrices(self):
    if self.checkIfCanBeExecuted() is False:
      return None
    try:
      r = requests.get(f'{self.coordinator_endpoint}/getNinjaPrices')
      data = r.json()
      return data
    except Exception:
      return None
    

  def getGroupCommand(self):
    try:
      r = requests.get(f'{self.coordinator_endpoint}/groups/getCommand?group={self.poe_bot.group_id}')
      data = r.json()
      command = data['command']
      return command
    except Exception:
      return None
    
  def setGroupCommand(self, new_command):
    try:
      r = requests.get(f'{self.coordinator_endpoint}/groups/setCommand?group={self.poe_bot.group_id}&new_command={new_command}')
      data = r.json()
      return data
    except Exception:
      return None


  def takerSendUpdate(self):
    if self.checkIfCanBeExecuted() is False:
      return None
    try:
      r = requests.get(f'{self.coordinator_endpoint}/takerSendUpdate')
      data = r.json()
      return data
    except Exception:
      return None


  