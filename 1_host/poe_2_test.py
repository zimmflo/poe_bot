#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import sys
from ast import literal_eval

from utils.gamehelper import Poe2Bot


# In[2]:





# In[2]:


notebook_dev = False
# readability
poe_bot_class = Poe2Bot
poe_bot: poe_bot_class


# In[3]:


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


# In[4]:


REMOTE_IP = config['REMOTE_IP'] # REMOTE_IP
UNIQUE_ID = config['unique_id'] # unique id
MAX_LVL = config.get('max_lvl')
CHROMATICS_RECIPE = config['chromatics_recipe']
BUILD_NAME = config['build'] # build_name
password = config['password']
force_reset_temp = config['force_reset_temp']
print(f'running aqueduct using: REMOTE_IP: {REMOTE_IP} unique_id: {UNIQUE_ID} max_lvl: {MAX_LVL} chromatics_recipe: {CHROMATICS_RECIPE} force_reset_temp: {force_reset_temp}')


# In[5]:


poe_bot = Poe2Bot(unique_id = UNIQUE_ID, remote_ip = REMOTE_IP, password=password)
poe_bot.refreshAll()
# poe_bot.game_data.terrain.getCurrentlyPassableArea()



# In[6]:


from utils.loot_filter import PickableItemLabel

ARTS_TO_PICK = [
  "Art/2DItems/Currency/CurrencyModValues.dds", # divine
  "Art/2DItems/Currency/CurrencyGemQuality.dds", # gemcutter
  "Art/2DItems/Currency/CurrencyRerollRare.dds", # chaos
  "Art/2DItems/Currency/CurrencyAddModToRare.dds", # exalt
  "Art/2DItems/Currency/CurrencyUpgradeToUnique.dds", # chance
]

# big piles of gold
for tier in range(2,17):
  ARTS_TO_PICK.append(f"Art/2DItems/Currency/Ruthless/CoinPileTier{tier}.dds")
# waystones
for tier in range(1,17):
  ARTS_TO_PICK.append(f"Art/2DItems/Maps/EndgameMaps/EndgameMap{tier}.dds")

# "Art/2DItems/Currency/Essence/GreaterFireEssence.dds"

def isItemHasPickableKey(item_label:PickableItemLabel):
  if item_label.icon_render in ARTS_TO_PICK:
    return True
  elif "Art/2DItems/Currency/Essence/" in item_label.icon_render:
    return True
  return False
poe_bot.loot_picker.loot_filter.special_rules = [isItemHasPickableKey]


# In[7]:


poe_bot.mover.setMoveType('wasd')


# In[8]:


from utils.combat import PathfinderPoisonConc2
from utils.combat import InfernalistZoomancer

# poe_bot.combat_module.build = InfernalistZoomancer(poe_bot=poe_bot)
poe_bot.combat_module.build = PathfinderPoisonConc2(poe_bot=poe_bot)
poe_bot.combat_module.build.auto_flasks.life_flask_recovers_es = True
poe_bot.combat_module.build.auto_flasks.hp_thresh = 0.25

def activateSwitchesNearby():
  switch_nearby = next( (e for e in poe_bot.game_data.entities.all_entities if e.is_targetable and e.path == "Metadata/Terrain/Maps/Crypt/Objects/CryptSecretDoorSwitch" and e.distance_to_player < 30), None)
  if switch_nearby:
    poe_bot.mover.goToEntitysPoint(switch_nearby)
    poe_bot.combat_module.clearAreaAroundPoint(switch_nearby.grid_position.toList())
    switch_nearby.clickTillNotTargetable()
    return True
  return False

def custom_default_continue_function(*args, **kwargs):
  pass

poe_bot.mover.default_continue_function = poe_bot.combat_module.build.usualRoutine


# In[9]:


# raise 404


# In[10]:


# Ы


# In[11]:


# poe_bot.backend.getVisibleLabels()


# In[12]:


# raise 404


# In[13]:


from utils.encounters import EssenceEncounter
from utils.constants import ESSENCES_KEYWORD

rares_detection_radius = 999



def seekForEssences(search_loc = None):
  '''
  search_loc: [gridx,gridy]
  '''
  essences = list(filter(lambda e: e.is_targetable is True and ESSENCES_KEYWORD in e.path and poe_bot.game_data.terrain.checkIfPointPassable(e.grid_position.x, e.grid_position.y), poe_bot.game_data.entities.all_entities))
  return essences

def runnerBreakFunction(*args, **kwargs):

  '''crypt map'''
  if activateSwitchesNearby() == True:
    return True
  '''crypt map'''

  if rares_detection_radius != 0:
    rares_nearby = list(filter(lambda e: e.distance_to_player < rares_detection_radius, poe_bot.game_data.entities.attackable_entities_rares))
    print(f'found rares {list(map(lambda e: e.raw, rares_nearby))}')
    for rare_mob in rares_nearby:
      updated_entity = list(filter(lambda e: e.id == rare_mob.id, poe_bot.game_data.entities.attackable_entities_rares))
      if len(updated_entity) != 0:
        updated_entity = updated_entity[0]
        print(f'going to kill rare {updated_entity.raw}')
        def custom_continue_func(*args, **kwargs):
          if activateSwitchesNearby() == True:
            return True
          if poe_bot.loot_picker.collectLoot() == True:
            return True
          return False
        # while True:
        #   res = poe_bot.mover.goToEntitysPoint(updated_entity,custom_break_function=custom_continue_func, min_distance=50)
        #   if res is None:
        #     break
        poe_bot.combat_module.killUsualEntity(updated_entity)
        return True
  essences = seekForEssences()
  if len(essences) != 0:
    essence_encounter = EssenceEncounter(poe_bot, essences[0])
    essence_encounter.doEncounter()
    poe_bot.loot_picker.collectLoot()
    return True

  loot_collected = poe_bot.loot_picker.collectLoot()
  if loot_collected is True:
    return loot_collected
  return False
  


# In[14]:


# raise 404
poe_bot.refreshAll()


# In[15]:


prefer_high_tier = True
alch_map_if_possible = True

maps_to_ignore = [
  "MapCrypt_NoBoss", # activators
  "MapAugury_NoBoss", # activators
  "MapLostTowers"
]


# In[16]:


# free inventory if neededS
poe_bot.ui.inventory.update()
empty_slots = poe_bot.ui.inventory.getEmptySlots()
if len(empty_slots) < 40:
  poe_bot.ui.stash.open()
  items_to_keep = []
  poe_bot.ui.inventory.update()
  waystones_to_keep = list(filter(lambda i: i.map_tier, poe_bot.ui.inventory.items))
  waystones_to_keep.sort(key=lambda i: i.map_tier, reverse=prefer_high_tier)
  items_to_keep.extend(waystones_to_keep[:4])
  alchemy_orbs = list(filter(lambda i: i.name == "Orb of Alchemy", poe_bot.ui.inventory.items))
  items_to_keep.extend(alchemy_orbs[:1])
  items_can_stash = list(filter(lambda i: i not in items_to_keep, poe_bot.ui.inventory.items))
  poe_bot.ui.clickMultipleItems(items_can_stash)
  poe_bot.ui.closeAll()
  time.sleep(random.uniform(0.3, 1.4))


# In[17]:


# open map device
poe_bot.ui.map_device.open()
# move to map, open dropdown
poe_bot.ui.map_device.update()
possible_to_run_maps = list(filter(lambda m: 
  m.is_boss == False and # some bosses have unique logic?
  m.is_tower == False and# cant run tower maps yet
  m.is_hideout == False and# hideouts ignored
  m.is_trader == False and# manual trade
  m.is_ritual == False and# save rituals for tests
  (m.name_raw in maps_to_ignore) == False
, poe_bot.ui.map_device.avaliable_maps))
map_obj = random.choice(possible_to_run_maps)
print(map_obj.raw)
poe_bot.ui.map_device.moveScreenTo(map_obj)
time.sleep(random.uniform(0.15, 0.35))


poe_bot.ui.map_device.update()


updated_map_obj = next( (m for m in poe_bot.ui.map_device.avaliable_maps if m.id == map_obj.id))
updated_map_obj.click()
time.sleep(random.uniform(0.15, 0.35))
poe_bot.ui.map_device.update()
if poe_bot.ui.map_device.place_map_window_opened == False:
  print(f'dropdown didnt open')
  pos_x, pos_y = poe_bot.game_window.convertPosXY(100, 100)
  poe_bot.bot_controls.mouse.setPosSmooth(pos_x, pos_y)
  time.sleep(random.uniform(0.15, 0.35))
  poe_bot.ui.map_device.update()
  updated_map_obj = next( (m for m in poe_bot.ui.map_device.avaliable_maps if m.id == map_obj.id))
  updated_map_obj.click()
  time.sleep(random.uniform(0.15, 0.35))
  poe_bot.ui.map_device.update()
  if poe_bot.ui.map_device.place_map_window_opened == False:
    print(f'seems like map device bug')
    poe_bot.raiseLongSleepException("cant open dropdown for map device")










# In[18]:


for m in possible_to_run_maps:
  print(m.raw)


# In[19]:


if poe_bot.ui.map_device.place_map_window_opened != True:
  poe_bot.raiseLongSleepException("cant open dropdown for map device")


# In[20]:


# screen_pos_x, screen_pos_y = poe_bot.game_window.center_point
# pos_x, pos_y = poe_bot.game_window.convertPosXY(screen_pos_x, screen_pos_y)
# poe_bot.bot_controls.mouse.setPos(pos_x, pos_y)


# poe_bot.ui.map_device.update()
# updated_map_obj = next( (m for m in poe_bot.ui.map_device.avaliable_maps if m.id == map_obj.id))

# screen_pos_x, screen_pos_y = updated_map_obj.screen_pos.toList()
# pos_x, pos_y = poe_bot.game_window.convertPosXY(screen_pos_x, screen_pos_y)
# # poe_bot.bot_controls.mouse.setPosSmooth(pos_x, pos_y)
# poe_bot.bot_controls.mouse.setPos(pos_x, pos_y)


# In[21]:


poe_bot.ui.inventory.update()
maps_in_inventory = list(filter(lambda i: i.map_tier, poe_bot.ui.inventory.items))
maps_in_inventory.sort(key=lambda i: i.map_tier, reverse=prefer_high_tier)
map_to_run = maps_in_inventory[0]
print(f'placing map {map_to_run.raw}')

if alch_map_if_possible == True:
  ARTS_TO_PICK.append("Art/2DItems/Currency/CurrencyUpgradeToRare.dds")
  for _i in range(1):
    if map_to_run.rarity != "Normal":
      break
    alchemy_orbs = list(filter(lambda i: i.name == "Orb of Alchemy", poe_bot.ui.inventory.items))
    if len(alchemy_orbs) == 0:
      break
    alchemy_orb = alchemy_orbs[0]
    alchemy_orb.click(button="right")
    time.sleep(random.uniform(0.4, 1.2))
    map_to_run.click()
    time.sleep(random.uniform(0.8, 1.2))

map_to_run.click(hold_ctrl=True)
poe_bot.ui.map_device.update()
#TODO sometimes activate button is outside roi
poe_bot.ui.map_device.checkIfActivateButtonIsActive()


poe_bot.ui.map_device.activate()

time.sleep(random.uniform(0.8, 1.6))
poe_bot.helper_functions.waitForNewPortals()


# In[22]:


poe_bot.refreshInstanceData()
original_area_raw_name = poe_bot.game_data.area_raw_name
poe_bot.helper_functions.getToPortal(check_for_map_device=False, refresh_area=True)
area_changed = False
while area_changed != True:
  poe_bot.refreshAll()
  area_changed = poe_bot.game_data.area_raw_name != original_area_raw_name


# In[23]:


# raise 404


# In[24]:


from utils.pathing import TSP


tsp = TSP(poe_bot=poe_bot)
# tsp.generatePointsForDiscovery()
mover = poe_bot.mover
map_complete = False
while map_complete is False:
  poe_bot.refreshInstanceData()
  print(f'generating pathing points')
  tsp.generatePointsForDiscovery()
  #TODO astar sorting
  discovery_points = tsp.sortedPointsForDiscovery(add_start_point_weight=True)
  print(f'len(discovery_points) {len(discovery_points)}')
  discovery_points = list(filter(lambda p: poe_bot.game_data.terrain.checkIfPointPassable(p[0], p[1]), discovery_points))
  print(f'len(discovery_points) {len(discovery_points)} after sorting')
  print(f'discovery_points {discovery_points}')
  if len(discovery_points) == 0:
    print(f'len(discovery_points) == 0 after points generation')
    map_complete = True
    break
  point_to_go = discovery_points.pop(0)
  while point_to_go is not None:
    need_to_explore = poe_bot.helper_functions.needToExplore(point_to_go=point_to_go)
    if need_to_explore is True:
      print(f'exploring point {point_to_go}')
    else:
      print(f'surrounding around {point_to_go} discovered, skipping')
      try:
        point_to_go = discovery_points.pop(0)
      except:
        point_to_go = None
      continue

    # go to point to make it explored
    result = mover.goToPoint(
      point=point_to_go,
      min_distance=50,
      release_mouse_on_end=False,
      custom_break_function=runnerBreakFunction,
      step_size=random.randint(30,35)
    )
    # then, it result is True, False or None
    print(f"mover.goToPoint result {result}")


    # if we arrived to discovery point and nothing happened
    poe_bot.game_data.map_info.update()
    if poe_bot.game_data.map_info.map_completed == True:
      print(f'poe_bot.game_data.map_info.map_completed == True')
      map_complete = True
      break
    if result is None:
      while True:
        if len(discovery_points) == 0:
          point_to_go = None
          map_complete = True
          print(f'len(discovery_points) == 0, breaking')
          break

        point_to_go = discovery_points.pop(0)
        print(f'willing to explore next point {point_to_go}')
        need_to_explore = poe_bot.helper_functions.needToExplore(point_to_go=point_to_go)

        if need_to_explore is True:
          print(f'exploring point {point_to_go}')
          break
        else:
          print(f'surrounding around {point_to_go} discovered, skipping')
          continue
    
    # if explorer_break_function() is True:
    #   map_complete = True
    #   break

    poe_bot.refreshInstanceData()
    poe_bot.last_action_time = 0
  # if possible_transition to explore, go to it, run discovery again


# In[25]:


# open portal and enter it
def openPortal():
  poe_bot.bot_controls.releaseAll()

  time.sleep(random.randint(40,80)/100)
  pos_x, pos_y = random.randint(709,711), random.randint(694,696)
  pos_x, pos_y = poe_bot.convertPosXY(pos_x, pos_y, safe=False)
  poe_bot.bot_controls.mouse.setPosSmooth(pos_x, pos_y)
  time.sleep(random.randint(40,80)/100)
  poe_bot.bot_controls.mouse.click()
  time.sleep(random.randint(30,60)/100)

while True:
  poe_bot.refreshInstanceData()
  loot_collected = poe_bot.loot_picker.collectLoot()
  if loot_collected == True:
    continue
  killed_smth = poe_bot.combat_module.clearAreaAroundPoint(poe_bot.game_data.player.grid_pos.toList())
  
  if poe_bot.game_data.invites_panel_visible == False and killed_smth == False:
    openPortal()
    poe_bot.helper_functions.waitForPortalNearby()
    poe_bot.helper_functions.getToPortal(check_for_map_device=False, refresh_area=False)
    poe_bot.refreshInstanceData()
    killed_smth = poe_bot.combat_module.clearAreaAroundPoint(poe_bot.game_data.player.grid_pos.toList())

    


# In[ ]:


raise 404


# In[24]:


prefer_high_tier = True


# In[ ]:


poe_bot.refreshAll()


# In[ ]:


tsp = TSP(poe_bot)

tsp.generatePointsForDiscovery()
#TODO astar sorting
discovery_points = tsp.sortedPointsForDiscovery()


# In[ ]:


poe_bot.game_data.player.grid_pos.toList()


# In[ ]:


discovery_points


# In[ ]:


poe_bot.backend.getMapInfo()


# In[ ]:


poe_bot.backend.getMapInfo()


# In[18]:


poe_bot.game_data.map_info.update()


# In[ ]:


poe_bot.game_data.map_info.map_completed


# In[ ]:


poe_bot.refreshAll()


# In[ ]:


poe_bot.game_data.player.grid_pos.toList()


# In[ ]:


poe_bot.mover.move(*poe_bot.game_data.player.grid_pos.toList())


# In[ ]:


# poe_bot.mo


# In[ ]:


import matplotlib.pyplot as plt

plt.imshow(poe_bot.game_data.terrain.passable)


# In[ ]:


poe_bot.refreshAll()
for e in poe_bot.game_data.labels_on_ground_entities:
  print(e.raw)

