#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import sys
from ast import literal_eval

from utils.gamehelper import Poe2Bot


# In[2]:


from typing import List


# In[3]:


notebook_dev = False
# readability
poe_bot_class = Poe2Bot
poe_bot: poe_bot_class


# In[4]:


default_config = {
  "REMOTE_IP": '172.23.107.65', # z2
  "unique_id": "poe_2_test",
  "build": "EaBallistasEle",
  "password": None,
  "max_lvl": 101,
  "chromatics_recipe": True,
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


# In[5]:


REMOTE_IP = config['REMOTE_IP'] # REMOTE_IP
UNIQUE_ID = config['unique_id'] # unique id
MAX_LVL = config.get('max_lvl')
CHROMATICS_RECIPE = config['chromatics_recipe']
BUILD_NAME = config['build'] # build_name
password = config['password']
force_reset_temp = config['force_reset_temp']
print(f'running aqueduct using: REMOTE_IP: {REMOTE_IP} unique_id: {UNIQUE_ID} max_lvl: {MAX_LVL} chromatics_recipe: {CHROMATICS_RECIPE} force_reset_temp: {force_reset_temp}')


# In[6]:


poe_bot = Poe2Bot(unique_id = UNIQUE_ID, remote_ip = REMOTE_IP, password=password)
poe_bot.refreshAll()
# poe_bot.game_data.terrain.getCurrentlyPassableArea()


# on map completion if some ritual was completed

# open ritual via ritual button
# TODO open ritual button is visible, screen position

 
poe_bot.ui.ritual_ui.update()
poe_bot.ui.ritual_ui.visible == True
poe_bot.ui.ritual_ui.tribute # current tribute
poe_bot.ui.ritual_ui.reroll_cost # 750 or 1000, depends on raw text
poe_bot.ui.ritual_ui.items # items actually

interesting_items_names = [
  "An Audience with the King",
  "Divine orb"
]

interesting_items = list(filter(lambda i: i.name == interesting_items_names,poe_bot.ui.ritual_ui.items))

for item in interesting_items:
  print(item.raw)
  # do something with them, defer, reroll, buyout, whatever


