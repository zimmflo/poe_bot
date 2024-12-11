#!/usr/bin/env python
# coding: utf-8

# In[1]:


from typing import List

import pickle
import os
import time
from math import dist
import random
import json
import sys
from ast import literal_eval
import copy
import traceback


import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils.gamehelper import PoeBot, Entity
from utils.controller import VMHostPuppeteer
from utils.utils import cropPath, sortByHSV, alwaysFalseFunction, raiseLongSleepException, createLineIterator, createLineIteratorWithValues, getFourPoints, extendLine
from utils.helper_functions import openStashTabIndexKeryboard, checkIfInventoryOpened, getFilledInventorySlots, openStash, getToHideout, getToPortal, mapDiscoveredForPercent, lvlUpGem, openTradeWithLilly
from utils.constants import FRIENDLY_ENTITIES_PATH_KEYWORDS, MAP_DEVICE_SLOTS, MAP_DEVICE_ACTIVATE_BUTTON, FLASK_NAME_TO_BUFF, BOSS_RENDER_NAMES
from utils.temps import MapsTempData
from utils.pathing import TSP
from utils.mover import Mover


# In[2]:


time_now = 0
notebook_dev = False
# readability
poe_bot: PoeBot
bot_controls:VMHostPuppeteer
mover: Mover


# In[3]:


default_config = {
  "REMOTE_IP": '172.26.26.246', # z2
  "UNIQUE_ID": "price_checker_test",
  "force_reset_temp": False,
  "password": None,
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

config = {

}

for key in default_config.keys():
  try:
    config[key] = parsed_config[key]
  except:
    config[key] = default_config[key]

print(f'config to run {config}')


# In[4]:


REMOTE_IP = config['REMOTE_IP'] # REMOTE_IP
UNIQUE_ID = "price_checker_test" # unique id
force_reset_temp = config['force_reset_temp']
mule_give_category = ["deafing_essences", "gilded_scarabs"]
print(f'running mule_giver_test using: REMOTE_IP: {REMOTE_IP} unique_id: {UNIQUE_ID} force_reset_temp: {force_reset_temp}')


# In[5]:


poe_bot = PoeBot(unique_id=UNIQUE_ID, remote_ip = REMOTE_IP)
bot_controls = poe_bot.bot_controls
stash = poe_bot.ui.stash
inventory = poe_bot.ui.inventory
coordinator = poe_bot.coordinator



# In[6]:


poe_bot.refreshAll()


# In[6]:


ninja_prices = coordinator.getNinjaPrices()
if ninja_prices is None:
  print(f'cannot do stash.priceReport cos coordinator doesnt give prices')
  raise 404
div_price = ninja_prices["Divine Orb"]['chaosValue']


# In[7]:


div_price


# In[ ]:


stash.temp.reset()
stash.updateStashTemp()


# In[9]:


all_items = stash.getAllItems()


# In[ ]:


essences = list(filter(lambda i: "Essence of" in i.name, all_items))
total_price = 0
high_ess_dict = {

}

for category_key in ["Deafening", "Shrieking"]:
  all_items_by_key_name = {}
  category_price = 0
  for item in essences:
    if not category_key in item.name:
      continue
    if all_items_by_key_name.get(item.name, None) is None:
      all_items_by_key_name[item.name] = 0

    all_items_by_key_name[item.name] += item.items_in_stack

  for item_key in all_items_by_key_name.keys():
    count = all_items_by_key_name[item_key]

    ninja_data = ninja_prices[item_key]
    price_per_item = ninja_data['chaosValue']
    total_price_for_stacks = count * price_per_item
    total_price += total_price_for_stacks
    category_price += total_price_for_stacks
    print(f"x{count:<4}| {price_per_item:<4}c | -{int(total_price_for_stacks)}c | {item_key}")
  print(f'{category_key}: {category_price}c')


high_ess_keys = ["Essence of Horror", "Essence of Delirium", "Essence of Hysteria","Essence of Insanity"]
for essence_item in essences:
  if essence_item.name in high_ess_keys:
    key_in_dict = high_ess_dict.get(essence_item.name, None)
    if key_in_dict is None:
      high_ess_dict[essence_item.name] = 0
    high_ess_dict[essence_item.name] += essence_item.items_in_stack

for item_key in high_ess_dict.keys():
  count = high_ess_dict[item_key]
  ninja_data = ninja_prices[item_key]
  price_per_item = ninja_data['chaosValue']
  total_price_for_stacks = count * price_per_item
  total_price += total_price_for_stacks
  category_price += total_price_for_stacks
  print(f"x{count:<4}| {price_per_item:<4}c | -{int(total_price_for_stacks)}c | {item_key}")

print(f'all essences: {total_price}c')
print(f'div_price {div_price}')
for price_multiplier in [1.1,1,0.95,0.9,0.85,0.8,0.75]:
  multiplied_price = total_price * price_multiplier
  price_in_div = int(multiplied_price // div_price)
  left_in_chaos = int(multiplied_price - price_in_div * div_price)
  multiplied_category_price = f'{price_multiplier*100}%: {price_in_div}d + {left_in_chaos} | {int(multiplied_price)}c'
  print(multiplied_category_price)

scarabs = list(filter(lambda i: "Scarab" in i.name, all_items))
total_price = 0
scarabs_dict = {

}
for item in scarabs:
  key_in_dict = scarabs_dict.get(item.name, None)
  if key_in_dict is None:
    scarabs_dict[item.name] = 0
  scarabs_dict[item.name] += item.items_in_stack

for item_key in scarabs_dict.keys():
  count = scarabs_dict[item_key]
  ninja_data = ninja_prices[item_key]
  price_per_item = ninja_data['chaosValue']
  total_price_for_stacks = count * price_per_item
  total_price += total_price_for_stacks
  print(f"x{count:<4}| {price_per_item:<4}c | -{int(total_price_for_stacks):<4}c | {item_key}")

print(f'total scarab price {total_price}c {total_price/div_price}d')
print(f'div_price {div_price}')
for price_multiplier in [0.9, 0.85, 0.8, 0.75, 0.7]:
  multiplied_price = total_price * price_multiplier
  price_in_div = int(multiplied_price // div_price)
  left_in_chaos = int(multiplied_price - price_in_div * div_price)
  multiplied_category_price = f'{price_multiplier*100}%: {price_in_div}d + {left_in_chaos} | {int(multiplied_price)}c'
  print(multiplied_category_price)


# In[ ]:


poe_bot.ui.closeAll()


# In[ ]:


raise "done"


# In[ ]:


for item in all_items:
  print(item.raw)


# In[ ]:


essences = list(filter(lambda i: "Scarab" in i.name, all_items))
total_price = 0
high_ess_dict = {

}

for category_key in ["Deafening", "Shrieking"]:
  all_items_by_key_name = {}
  category_price = 0
  for item in essences:
    if not category_key in item.name:
      continue
    if all_items_by_key_name.get(item.name, None) is None:
      all_items_by_key_name[item.name] = 0

    all_items_by_key_name[item.name] += item.items_in_stack

  for item_key in all_items_by_key_name.keys():
    count = all_items_by_key_name[item_key]

    ninja_data = ninja_prices[item_key]
    price_per_item = ninja_data['chaosValue']
    total_price_for_stacks = count * price_per_item
    total_price += total_price_for_stacks
    category_price += total_price_for_stacks
    print(f"x{count:<4}| {price_per_item:<4}c | -{int(total_price_for_stacks)}c | {item_key}")
  print(f'{category_key}: {category_price}c')


high_ess_keys = ["Essence of Horror", "Essence of Delirium", "Essence of Hysteria","Essence of Insanity"]
for essence_item in essences:
  if essence_item.name in high_ess_keys:
    key_in_dict = high_ess_dict.get(essence_item.name, None)
    if key_in_dict is None:
      high_ess_dict[essence_item.name] = 0
    high_ess_dict[essence_item.name] += essence_item.items_in_stack

for item_key in high_ess_dict.keys():
  count = high_ess_dict[item_key]
  ninja_data = ninja_prices[item_key]
  price_per_item = ninja_data['chaosValue']
  total_price_for_stacks = count * price_per_item
  total_price += total_price_for_stacks
  category_price += total_price_for_stacks
  print(f"x{count:<4}| {price_per_item:<4}c | -{int(total_price_for_stacks)}c | {item_key}")

print(f'all essences: {total_price}c')
print(f'div_price {div_price}')
for price_multiplier in [1.1,1,0.95,0.9,0.85,0.8,0.75]:
  multiplied_price = total_price * price_multiplier
  price_in_div = int(multiplied_price // div_price)
  left_in_chaos = int(multiplied_price - price_in_div * div_price)
  multiplied_category_price = f'{price_multiplier*100}%: {price_in_div}d + {left_in_chaos} | {int(multiplied_price)}c'
  print(multiplied_category_price)

