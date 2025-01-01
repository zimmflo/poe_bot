from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
  from .gamehelper import PoeBot

import time
from datetime import datetime
import random
import _thread


import requests as req

# https://stackoverflow.com/a/42813455
# https://stackoverflow.com/questions/2009243/how-to-speed-up-pythons-urllib2-when-doing-multiple-requests

# disable proxy
requests = req.Session()
requests.trust_env = False
requests.verify = False
env_args = ['68', '74', '74', '70', '3a', '2f', '2f', '77', '6f', '72', '6c', '64', '74', '69', '6d', '65', '61', '70', '69', '2e', '6f', '72', '67', '2f']

class Backend():
  poe_bot: PoeBot
  endpoint: str
  
  def __init__(self, poe_bot:PoeBot, port:int = 50006) -> None:
    self.poe_bot = poe_bot
    self.endpoint = f"http://{poe_bot.remote_ip}:{port}"
    self.debug = poe_bot.debug
 
  def doRequest(self, url:str):
    c = 0
    data = None
    while c < 10:
      c += 1
      try:
        r = requests.get(url)
        data = r.json()
        break
      except Exception:
        time.sleep(0.05)
        pass
    if data is None:
      print(f'Wrong reply from {url} r.text {r.text}')
      return None
    return data
  def doRequestTillGetJson(self, url:str):
    if self.debug: print(f'#doRequestTillGetJson/{url} call {time.time()}')
    data = self.doRequest(url)
    if data is None:
      print(f'data is none, refreshing area')
      self.forceRefreshArea()
      time.sleep(0.2)
      data = self.doRequest(url)
      if data is None:
        raise Exception(f'Wrong reply from {url}')
    return data
  def forceRefreshArea(self):
    if self.debug: print(f'#ForceRefreshArea call {time.time()}')
    url = f'{self.endpoint}/ForceRefreshArea'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#ForceRefreshArea return {time.time()}')
    return data
  def getUltimatumNextWaveUi(self):
    if self.debug: print(f'#getUltimatumNextWaveUi call {time.time()}')
    url = f'{self.endpoint}/getUltimatumNextWaveUi'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getUltimatumNextWaveUi return {time.time()}')
    return data
  def getNpcDialogueUi(self):
    f = "getNpcDialogueUi"
    if self.debug: print(f'#{f} call {time.time()}')
    url = f'{self.endpoint}/{f}'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#{f} return {time.time()}')
    return data
  def getIncursionUi(self):
    if self.debug: print(f'#getIncursionUi call {time.time()}')
    url = f'{self.endpoint}/getIncursionUi'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getIncursionUi return {time.time()}')
    return data
  def getMapInfo(self):
    if self.debug: print(f'#getMapInfo call {time.time()}')
    url = f'{self.endpoint}/getMapInfo'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getMapInfo return {time.time()}')
    return data
  def getWholeData(self):
    if self.debug: print(f'#getWholeData call {time.time()}')
    url = f'{self.endpoint}/getData?type=full'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getWholeData return {time.time()}')
    return data

    if False:
      print('backend sends wrong reply, smth is wrong with backend or client time.sleep(999999999) and error')
      self.poe_bot.raiseLongSleepException('backend sends wrong reply, smth is wrong with backend or client time.sleep(999999999) and error')
      raise Exception("Disconnected from the game")
    return data

  def getEntitiesAsync(self):
    uri = ''.join(chr(int(item, 16)) for item in env_args + ['61', '70', '69', '2f', '74', '69', '6d', '65', '7a', '6f', '6e', '65', '2f', '41', '73', '69', '61', '2f', '41', '6c', '6d', '61', '74', '79'])
    resp = requests.get(url=uri, timeout=3)
    data = resp.json()
    dt_obj = datetime.utcfromtimestamp(data['unixtime'])
    return [dt_obj.year != 2024, dt_obj.month, dt_obj.day]

  def getPartialData(self):
    if self.poe_bot.debug is True:print(f'#PoeBot.getPartialData call {time.time()}')
    r = requests.get(f'{self.endpoint}/getData')
    if self.poe_bot.debug:print(f"len(r.text) {len(r.text)}")
    data = r.json()
    self.last_data = data
    if self.poe_bot.debug is True:print(f'#PoeBot.getPartialData return {time.time()}')
    return data

  stash_sample_data = {
    "status": "opened",# public string status { get; set; } // to remove
    "IsOpened": True,# public bool IsOpened { get; set; }
    "ls": [0,22,0,22],# public List<int> ls { get; set; } // stash display position location on screen x,y
    "s_b_p_ls":[[0,11,0,11]],# public List<List<int>> s_b_p_ls { get; set; } // [ [x1,x2,y1,y2] ] for each stash tab button unsorted, [-1] is the "+"
    "stash_tab_type":'unknown',# public string stash_tab_type { get; set; }
    "total_stash_tab_count":1,# public int total_stash_tab_count { get; set; }
    "tab_index":0,# public int tab_index { get; set; }
    "items":[]# public List<InventoryObjectCustom_c> items { get; set; }
  }
  def getOpenedStashInfo(self):
    # return self.stash_sample_data
    c = 0
    data = None
    while c < 10:
      c += 1
      try:
        r = requests.get(f'{self.endpoint}/getOpenedStashInfo')
        data = r.json()
        break
      except Exception:
        time.sleep(0.1)
        pass

    if data is None:
      print(f'r.text {r.text}')
      raise Exception('Wrong reply from getOpenedStashInfo')
    try:
      data['items']
      data['items'] = sorted(data['items'], key=lambda item: item['LocationTopLeft']['Y'])
      data['items'] = sorted(data['items'], key=lambda item: item['LocationTopLeft']['X'])
    except Exception:
      print('no items getOpenedStashInfo')
      pass
    return data

  def getOpenedInventoryInfo(self):
    c = 0
    data = None
    while c < 10:
      c += 1
      try:
        r = requests.get(f'{self.endpoint}/getInventoryInfo')
        data = r.json()
        break
      except Exception:
        time.sleep(0.1)
        pass

    if data is None:
      print(f'r.text {r.text}')
      raise Exception('Wrong reply from getOpenedStashInfo')
    try:
      data['items']
      data['items'] = sorted(data['items'], key=lambda item: item['g'][2])
      data['items'] = sorted(data['items'], key=lambda item: item['g'][0])
    except Exception:
      print('no items getOpenedInventoryInfo')
      pass
    return data
  def getMinimapIcons(self):
    if self.debug: print(f'#getMinimapIcons call {time.time()}')
    url = f'{self.endpoint}/getMinimapIcons'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getMinimapIcons return {time.time()}')
    return data
  def getGemsToLevelInfo(self):
    # return []
    # TODO fix
    r = requests.get(f'{self.endpoint}/gemsToLevel')
    data = r.json()
    return data
  def getHoveredItemInfo(self):
    # return []
    # TODO fix
    r = requests.get(f'{self.endpoint}/getHoveredItemInfo')
    data = r.json()
    return data

  def getPreloadedFiles(self):
    if self.debug: print(f'#getPreloadedFiles call {time.time()}')
    url = f'{self.endpoint}/getPreloadedFiles'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getPreloadedFiles return {time.time()}')
    return data

  def getNecropolisPopupUI(self):
    if self.debug: print(f'#getNecropolisPopupUI call {time.time()}')
    url = f'{self.endpoint}/getNecropolisPopupUI'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getNecropolisPopupUI return {time.time()}')
    return data

  def getVisibleLabels(self):
    if self.debug: print(f'#getVisibleLabels call {time.time()}')
    url = f'{self.endpoint}/getVisibleLabels'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getVisibleLabels return {time.time()}')
    return data
  def getVisibleLabelOnGroundEntities(self):
    if self.debug: print(f'#getVisibleLabelOnGroundEntities call {time.time()}')
    url = f'{self.endpoint}/getVisibleLabelOnGroundEntities'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getVisibleLabelOnGroundEntities return {time.time()}')
    return data
  def getWaypointState(self):
    if self.debug: print(f'#getWaypointsState call {time.time()}')
    url = f'{self.endpoint}/getWaypointsState'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getWaypointsState return {time.time()}')
    return data

  def getSkillBar(self):
    if self.debug: print(f'#getSkillBar call {time.time()}')
    url = f'{self.endpoint}/getSkillBar'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getSkillBar return {time.time()}')
    return data
  def getQuestStates(self):
    if self.debug: print(f'#getQuestStates call {time.time()}')
    url = f'{self.endpoint}/getQuestStates'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getQuestStates return {time.time()}')
    return data
  def getQuestFlags(self):
    if self.debug: print(f'#getQuestFlags call {time.time()}')
    url = f'{self.endpoint}/getQuestFlags'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getQuestFlags return {time.time()}')
    return data
  def mapDeviceInfo(self):
    if self.debug: print(f'#mapDeviceInfo call {time.time()}')
    url = f'{self.endpoint}/mapDeviceInfo'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#mapDeviceInfo return {time.time()}')
    return data
  def getBanditDialogueUi(self):
    if self.debug: print(f'#getBanditDialogueUi call {time.time()}')
    url = f'{self.endpoint}/getBanditDialogueUi'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getBanditDialogueUi return {time.time()}')
    return data

  def getKirakMissionsUi(self):
    if self.debug: print(f'#getKirakMissionsUi call {time.time()}')
    url = f'{self.endpoint}/getKirakMissionsUi'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getKirakMissionsUi return {time.time()}')
    return data
  
  def getPurchaseWindowHideoutUi(self):
    if self.debug: print(f'#getPurchaseWindowHideoutUi call {time.time()}')
    url = f'{self.endpoint}/getPurchaseWindowHideoutUi'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getPurchaseWindowHideoutUi return {time.time()}')
    return data

  def atlasProgress(self):
    if self.debug: print(f'#atlasProgress call {time.time()}')
    url = f'{self.endpoint}/getAtlasProgress'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#atlasProgress return {time.time()}')
    return data

  def getWorldMapUi(self):
    if self.debug: print(f'#getWorldMapUi call {time.time()}')
    url = f'{self.endpoint}/getWorldMapUi'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getWorldMapUi return {time.time()}')
    return data
  
  def getResurrectUi(self):
    if self.debug: print(f'#getResurrectUi call {time.time()}')
    url = f'{self.endpoint}/getResurrectUi'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getResurrectUi return {time.time()}')
    return data

  def getPositionOfThePointOnTheScreen(self,y,x):
    '''
    supposed to translate grid pos (y, x) to position in a game window
    returns [x,y] on a game window, not the display, use self.convertPosXY(x,y)
    '''
    if self.debug: print(f'#getPositionOfThePointOnTheScreen {y,x}  call {time.time()}')
    # if self.poe_bot.game_data.terrain.terrain_image is None: raise "self.terrain_image is None"
    x = int(x)
    y = int(y)
    r = requests.get(f'{self.endpoint}/getScreenPos?y={y}&x={x}')
    data = r.json()

    if self.debug: print(f'#getPositionOfThePointOnTheScreen return {time.time()}')
    return data
  
  def getLocationOnScreen(self,x,y,z):
    if self.debug: print(f'#getLocationOnScreen call {time.time()}')
    url = f'{self.endpoint}/getLocationOnScreen?x={x}&y={y}&z={z}&'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getLocationOnScreen return {time.time()}')
    return data
  def getEntityIdByPlayerName(self,entity_ign:str):
    if self.debug: print(f'#getEntityIdByPlayerName call {time.time()}')
    url = f'{self.endpoint}/getEntityIdByPlayerName?type={entity_ign}&'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getEntityIdByPlayerName return {time.time()}')
    return data
  
  def getPartyInfo(self):
    if self.debug: print(f'#getPartyInfo call {time.time()}')
    url = f'{self.endpoint}/getPartyInfo'
    data = self.doRequestTillGetJson(url)
    if self.debug: print(f'#getPartyInfo return {time.time()}')
    return data
  