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
  "REMOTE_IP": '172.20.89.14', # z2
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


bot_controls.restartScript()
poe_bot.refreshAll()


# In[8]:


while True:
  input('gonna pick essences from current stash tab, lowest amount to highest amount')
  poe_bot.ui.stash.update()
  current_stash_items = poe_bot.ui.stash.current_tab_items
  ess_keys = ["Deafening", "Shrieking", "Essence of Horror", "Essence of Delirium", "Essence of Hysteria","Essence of Insanity"]
  filtered_items = list(filter(lambda i: any(list(map(lambda k: k in i.name, ess_keys))), current_stash_items))
  filtered_items = sorted(filtered_items, key=lambda i: i.items_in_stack)
  stack_size = 9
  items_to_pick = []
  while True:
    if len(filtered_items) == 0:
      if len(items_to_pick) == 0:
        raise Exception('dont have items in stash tab')
      print(f'last trade')
      break
    item_count = int(filtered_items[0].items_in_stack / stack_size) + int(filtered_items[0].items_in_stack % stack_size != 0)  
    for i in range(item_count):
      items_to_pick.append(filtered_items[0])
    filtered_items.pop(0)
    if len(items_to_pick) >= 60:
      break

  items_to_pick = items_to_pick[:60]
  time.sleep(random.randint(3,7)/100)
  bot_controls.keyboard_pressKey('DIK_LCONTROL')

  for item in items_to_pick:
    item.click()
  bot_controls.keyboard_releaseKey('DIK_LCONTROL')

  input('going to ctrl click essences to put them in trade')
  poe_bot.ui.inventory.update()
  items_in_inventory = poe_bot.ui.inventory.items
  single_stack_items_in_inventory = []
  multiple_stack_item_names_in_inventory = []

  
  shift_pressed = False
  time.sleep(random.randint(3,7)/100)
  bot_controls.keyboard_pressKey('DIK_LCONTROL')

  for item in items_in_inventory:
    item_name = item.name
    if item_name in multiple_stack_item_names_in_inventory:
      continue
    item_stack_count = len(list(filter(lambda i: i.name == item_name, items_in_inventory)))
    if item_stack_count > 1:
      if not shift_pressed:
        time.sleep(random.randint(3,7)/100)
        poe_bot.bot_controls.keyboard_pressKey('DIK_LSHIFT')
        shift_pressed = True
      item.click()
      multiple_stack_item_names_in_inventory.append(item.name)
    else:
      single_stack_items_in_inventory.append(item)
  if shift_pressed:
    poe_bot.bot_controls.keyboard_releaseKey('DIK_LSHIFT')

  for item in single_stack_items_in_inventory:
    item.click()
    if random.randint(1,10) == 1:
      time.sleep(random.randint(3,7)/10)

  bot_controls.keyboard_releaseKey('DIK_LCONTROL')

  input('going to stash items, divines in current tab, others just ctrl click')
  poe_bot.refreshInstanceData()
  poe_bot.ui.stash.open()
  time.sleep(random.randint(20,30)/100)
  poe_bot.ui.inventory.update()
  items_in_inventory = poe_bot.ui.inventory.items
  divines = list(filter(lambda i: i.name == "Divine Orb", items_in_inventory))
  if divines:
    poe_bot.bot_controls.keyboard_pressKey('DIK_LSHIFT')
    time.sleep(random.randint(7,13)/100)
    poe_bot.ui.clickMultipleItems(divines, add_delay_before_last_clicks=False)
    time.sleep(random.randint(7,13)/100)
    poe_bot.bot_controls.keyboard_releaseKey("DIK_LSHIFT")
  poe_bot.ui.inventory.update()
  items_in_inventory = poe_bot.ui.inventory.items
  poe_bot.ui.clickMultipleItems(items_in_inventory, add_delay_before_last_clicks=False)


