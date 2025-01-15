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



# In[7]:


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


# In[8]:


poe_bot.mover.setMoveType('wasd')


# In[9]:


from utils.combat import PathfinderPoisonConc2
from utils.combat import InfernalistZoomancer
from utils.combat import GenericBuild2
from utils.combat import GenericBuild2Cautious

# poe_bot.combat_module.build = InfernalistZoomancer(poe_bot=poe_bot)
# poe_bot.combat_module.build = PathfinderPoisonConc2(poe_bot=poe_bot)
poe_bot.combat_module.build = GenericBuild2(poe_bot=poe_bot)
# poe_bot.combat_module.build = GenericBuild2Cautious(poe_bot=poe_bot)
poe_bot.combat_module.build.auto_flasks.life_flask_recovers_es = True
poe_bot.combat_module.build.auto_flasks.hp_thresh = 0.70

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


# In[10]:


# raise 404


# In[11]:


# Ы


# In[12]:


# poe_bot.backend.getVisibleLabels()


# In[13]:


# raise 404


# In[14]:


from utils.encounters import EssenceEncounter, BreachEncounter, RitualEncounter
from utils.constants import ESSENCES_KEYWORD

class MapperSettings:
  pass

# class Mapper:
#   def run():
#     current_map_area = getMapArea(poe_bot.game_data.area_raw_name)
#     current_map_area.complete()
class MapArea:
  boss_render_names:List[str] = []

class MapBackwash(MapArea):
  boss_render_names = ["Yaota, the Loathsome"]

# settings
rares_detection_radius = 999
prefer_high_tier = True
alch_map_if_possible = True

maps_to_ignore = [
  "MapCrypt_NoBoss", # activators
  "MapAugury_NoBoss", # activators
  "MapLostTowers"
]


# cache
ritual_ignore_ids = []


def isMapCompleted():
  poe_bot.game_data.map_info.update()
  if poe_bot.game_data.map_info.map_completed == True:
    print(f'poe_bot.game_data.map_info.map_completed == True')
    return True
  return False

def seekForEssences(search_loc = None):
  '''
  search_loc: [gridx,gridy]
  '''
  essences = list(filter(lambda e: e.is_targetable is True and ESSENCES_KEYWORD in e.path and poe_bot.game_data.terrain.checkIfPointPassable(e.grid_position.x, e.grid_position.y), poe_bot.game_data.entities.all_entities))
  return essences

def seekForBreaches():
  return next( (e for e in poe_bot.game_data.entities.all_entities if e.path == "Metadata/MiscellaneousObjects/Breach/BreachObject"), None)

def seekForRituals():
  return next( (e for e in poe_bot.game_data.entities.all_entities if e.path == "Metadata/Terrain/Leagues/Ritual/RitualRuneInteractable" and not e.id in ritual_ignore_ids), None)


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

  breach_entity = seekForBreaches()
  if breach_entity:
    BreachEncounter(poe_bot, breach_entity).doEncounter()
    return True

  ritual_entity = seekForRituals()
  if ritual_entity:
    poe_bot.mover.goToEntitysPoint(ritual_entity, min_distance=100)
    poe_bot.game_data.minimap_icons.update()
    corresponding_icon = next( (i for i in poe_bot.game_data.minimap_icons.icons if i.id == ritual_entity.id), None)
    if not corresponding_icon:
      poe_bot.mover.goToEntitysPoint(ritual_entity, min_distance=50)
    poe_bot.game_data.minimap_icons.update()
    corresponding_icon = next( (i for i in poe_bot.game_data.minimap_icons.icons if i.id == ritual_entity.id), None)
    if not corresponding_icon:
      print('ritual minimap icon is not in hud, ignoring')
      ritual_ignore_ids.append(ritual_entity.id)
      return True
    if corresponding_icon.name == "RitualRuneFinished":
      print('according to minimap icon data, ritual is finished')
      ritual_ignore_ids.append(ritual_entity.id)
      return True
    RitualEncounter(poe_bot, ritual_entity).doEncounter()
    # check if we did 3 of 3 or 4of4 rituals, if true, defer\whatever items
    ritual_ignore_ids.append(ritual_entity.id)
    return True

    

  loot_collected = poe_bot.loot_picker.collectLoot()
  if loot_collected is True:
    return loot_collected
  return False
  


# In[15]:


# raise 404
poe_bot.refreshAll()


# In[ ]:


# free inventory if needed
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


# In[ ]:


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










# In[ ]:


poe_bot.ui.map_device.update()
for m in poe_bot.ui.map_device.avaliable_maps:
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


# In[ ]:


if len(poe_bot.ui.map_device.place_map_window_items) > 1:
  poe_bot.raiseLongSleepException('placed more than 1 map already')
elif len(poe_bot.ui.map_device.place_map_window_items) == 0:
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


# In[ ]:


poe_bot.ui.map_device.update()
#TODO sometimes activate button is outside roi
poe_bot.ui.map_device.checkIfActivateButtonIsActive()


# In[ ]:


poe_bot.ui.map_device.activate()

time.sleep(random.uniform(0.8, 1.6))
poe_bot.helper_functions.waitForNewPortals()


# In[ ]:


poe_bot.refreshInstanceData()
original_area_raw_name = poe_bot.game_data.area_raw_name
poe_bot.helper_functions.getToPortal(check_for_map_device=False, refresh_area=True)
area_changed = False
while area_changed != True:
  poe_bot.refreshAll()
  area_changed = poe_bot.game_data.area_raw_name != original_area_raw_name


# In[25]:


# raise 404


# In[ ]:


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
    if isMapCompleted() == True:
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


# In[ ]:


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


map_finish_time = time.time() 
time_now = time.time()
rev = bool(random.randint(0,1))
while time_now < map_finish_time + 1 :
  poe_bot.refreshInstanceData()
  killed_someone = poe_bot.combat_module.clearLocationAroundPoint({"X":poe_bot.game_data.player.grid_pos.x, "Y":poe_bot.game_data.player.grid_pos.y},detection_radius=50)
  res = poe_bot.loot_picker.collectLoot()
  if killed_someone is False and res is False:
    point = poe_bot.game_data.terrain.pointToRunAround(
      point_to_run_around_x=poe_bot.game_data.player.grid_pos.x,
      point_to_run_around_y=poe_bot.game_data.player.grid_pos.y,
      distance_to_point=15,
      reversed=rev
    )
    poe_bot.mover.move(grid_pos_x = point[0], grid_pos_y = point[1])
    poe_bot.refreshInstanceData()
  time_now = time.time()

i = 0
random_click_iter = 0
can_click_portal_after = time.time()
while True:
  while True:
    poe_bot.refreshInstanceData()
    res = poe_bot.loot_picker.collectLoot()
    if res is False:
      break
  
  if poe_bot.game_data.invites_panel_visible != False:
    print(f'[onmapfinishfunction] already loading')
  else:
    i+= 1
    random_click_iter += 1
    if random_click_iter > 15:
      print('[Mapper] cannot get to portal, clicking random point around the player')
      poe_bot.ui.closeAll()
      # point = poe_bot.game_data.terrain.pointToRunAround(poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y, distance_to_point=random.randint(15,25), check_if_passable=True)
      random_click_iter = random.randint(0,3)
    if i > 200:
      poe_bot.raiseLongSleepException('portal bug')
    nearby_portals = list(filter(lambda e: e.distance_to_player < 50, poe_bot.game_data.entities.town_portals))
    if len(nearby_portals) == 0:
      openPortal()
    nearby_portals = list(filter(lambda e: e.distance_to_player < 50, poe_bot.game_data.entities.town_portals))
    if len(nearby_portals) != 0:
      poe_bot.helper_functions.getToPortal(check_for_map_device=False, refresh_area=False)
  poe_bot.combat_module.clearLocationAroundPoint({"X": poe_bot.game_data.player.grid_pos.x, "Y": poe_bot.game_data.player.grid_pos.y},detection_radius=50)
  poe_bot.loot_picker.collectLoot()


# In[ ]:


# while True:
#   poe_bot.refreshInstanceData()
#   loot_collected = poe_bot.loot_picker.collectLoot()
#   if loot_collected == True:
#     continue
#   killed_smth = poe_bot.combat_module.clearAreaAroundPoint(poe_bot.game_data.player.grid_pos.toList())
  
#   if poe_bot.game_data.invites_panel_visible == False and killed_smth == False:
#     openPortal()
#     poe_bot.helper_functions.waitForPortalNearby()
#     poe_bot.helper_functions.getToPortal(check_for_map_device=False, refresh_area=False)
#     poe_bot.refreshInstanceData()
#     killed_smth = poe_bot.combat_module.clearAreaAroundPoint(poe_bot.game_data.player.grid_pos.toList())

    


# In[ ]:


raise Exception('Script ended, restart')


# In[24]:


prefer_high_tier = True


# In[ ]:


poe_bot.refreshAll()
poe_bot.game_data.terrain.getCurrentlyPassableArea()


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


# In[ ]:


poe_bot.refreshAll()


# In[ ]:


poe_bot.ui.stash.update()


# In[ ]:


max_tier_to_recycle = 11

stash = poe_bot.ui.stash
stash.update()
waystone_items = list(filter(lambda i: i.map_tier != 0, stash.current_tab_items))
waystones_by_tier = {

}
for item in waystone_items:
  waystone_tier = item.map_tier
  if waystone_tier > max_tier_to_recycle:
    continue
  if waystones_by_tier.get(waystone_tier, 0) == 0:
    waystones_by_tier[waystone_tier] = []
  waystones_by_tier[waystone_tier].append(item)

waystone_tiers_sorted = list(waystones_by_tier.keys())
waystone_tiers_sorted.sort()

collected_items_count = 0
max_items_can_get = 60
for k in waystone_tiers_sorted:
  waystones_amount = len(waystones_by_tier[k])
  if waystones_amount // 3 == 0:
    continue

  collected_items_count += waystones_amount
  if collected_items_count > max_items_can_get:
    break
  poe_bot.ui.clickMultipleItems(waystones_by_tier[k])


# In[ ]:


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
  item.hover()
  item_info = poe_bot.backend.getHoveredItemInfo()
  cost = int(item_info['tt'][-2][:-1])
  # do something with them, defer, reroll, buyout, whatever


