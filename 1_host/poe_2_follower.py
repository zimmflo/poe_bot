#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import sys
from ast import literal_eval

from utils.gamehelper import Poe2Bot, Entity
from utils.combat import AutoFlasks


# In[2]:


notebook_dev = False
# readability
poe_bot_class = Poe2Bot
poe_bot: poe_bot_class


# In[3]:


default_config = {
  "REMOTE_IP": '172.23.107.65', # z2
  "unique_id": "poe_2_test",
  "password": None,
  "force_reset_temp": False,
}



try:
  i = sys.argv[1]
  print(i)
  parsed_config = literal_eval(i)
  print(f'successfully parsed cli config')
  print(f'parsed_config: {parsed_config}')
except:
  print(f'cannot parse config from cli, using default\dev one')
  notebook_dev = True
  parsed_config = default_config
  parsed_config['unique_id'] = poe_bot_class.getDevKey()

config = {

}

for key in default_config.keys():
  config[key] = parsed_config.get(key, default_config[key])

print(f'config to run {config}')


# In[4]:


REMOTE_IP = config['REMOTE_IP'] # REMOTE_IP
UNIQUE_ID = config['unique_id'] # unique id
password = config['password']
force_reset_temp = config['force_reset_temp']
print(f'running follower using: REMOTE_IP: {REMOTE_IP} unique_id: {UNIQUE_ID} force_reset_temp: {force_reset_temp}')


# In[5]:


poe_bot = Poe2Bot(unique_id = UNIQUE_ID, remote_ip = REMOTE_IP, password=password)
poe_bot.refreshAll()
poe_bot.game_data.terrain.getCurrentlyPassableArea()

auto_flasks = AutoFlasks(poe_bot)

def useFlasksOutsideOfHideout():
  if poe_bot.game_data.area_raw_name[:7] != "Hideout":
    auto_flasks.useFlasks()

def mover_default_func(*args, **kwargs):
  useFlasksOutsideOfHideout()
  return False

poe_bot.mover.default_continue_function = mover_default_func



# In[6]:


# settings
poe_bot.mover.setMoveType('wasd')

refresh_area_frequency = 10
min_distance_to_follow = 20

# entity_to_follow_ign = "Skobayashi"
entity_to_follow_ign = None

auto_flasks.life_flask_recovers_es = True
auto_flasks.hp_thresh = 0.75


# In[7]:


# 


# In[8]:


entity_to_follow:Entity = None
id_to_follow:int = None
_i = 0
while True:
  ign_to_follow:str = None
  party_raw:dict = None

  _i += 1
  if _i == refresh_area_frequency:
    poe_bot.refreshAll()
    poe_bot.game_data.terrain.getCurrentlyPassableArea()
    _i = 0
  else:
    poe_bot.refreshInstanceData()
  
  useFlasksOutsideOfHideout()


  

  # if there is a ign in settings, find by ign
  if entity_to_follow_ign != None:
    ign_to_follow = entity_to_follow_ign
  else:
    party_raw = poe_bot.backend.getPartyInfo()
    party_leader = next( (pm for pm in party_raw['party_members'] if pm["is_leader"] == True), None)
    if party_leader:
      ign_to_follow = party_leader['ign']
  if ign_to_follow == None:
    print(f'couldnt find either party leader or entity_to_follow_ign: <{entity_to_follow_ign}> in party')
    continue


  id_to_follow = poe_bot.backend.doRequest(f'{poe_bot.backend.endpoint}/getEntityIdByPlayerName?type={ign_to_follow}&')
  # check if party member to follow in diff loc and portal to that loc is somewhere around
  if id_to_follow == None:
    if party_raw == None:
      party_raw = poe_bot.backend.getPartyInfo()
    party_member_to_follow = next( (pm for pm in party_raw['party_members'] if pm["ign"] == ign_to_follow), None)
    if party_member_to_follow == None:
      print(f'{ign_to_follow} is not in party')
      continue
    member_to_follow_loc = party_member_to_follow['area_raw_name']
    portals_with_similar_area_name = next( (e for e in poe_bot.game_data.entities.town_portals if e.render_name == member_to_follow_loc), None)
    if portals_with_similar_area_name:
      poe_bot.mover.goToEntitysPoint(portals_with_similar_area_name, release_mouse_on_end=True)
      poe_bot.helper_functions.getToPortal(check_for_map_device=False)
    
  prev_entity_to_follow = entity_to_follow
  entity_to_follow = next( (e for e in poe_bot.game_data.entities.all_entities if e.id == id_to_follow), None)
    # else: get party, get leader, get leader ign

  if entity_to_follow:
    if entity_to_follow.distance_to_player > min_distance_to_follow:
      if entity_to_follow.isInRoi() and entity_to_follow.isInLineOfSight():
        poe_bot.mover.move(*entity_to_follow.grid_position.toList())
      else:
        poe_bot.mover.goToEntity(entity_to_follow, min_distance=min_distance_to_follow)
    else:
      poe_bot.mover.stopMoving()

    
  


# In[ ]:


raise 404

