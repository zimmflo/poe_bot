#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import sys
from ast import literal_eval

from utils.gamehelper import PoeBot
from utils.controller import VMHostPuppeteer
from utils.mover import Mover
from utils.loot_filter import CustomLootFilter


# In[2]:


time_now = 0
notebook_dev = False
# readability
poe_bot: PoeBot
bot_controls:VMHostPuppeteer
mover: Mover


# In[3]:


default_config = {
  "REMOTE_IP": '172.28.180.101', # z2
  "unique_id": "incorrect",
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
  parsed_config['unique_id'] = PoeBot.getDevKey()

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


poe_bot = PoeBot(unique_id = UNIQUE_ID, remote_ip = REMOTE_IP, password=password)
bot_controls = poe_bot.bot_controls
mover = poe_bot.mover
poe_bot.refreshAll()
poe_bot.combat_module.assignBuild(BUILD_NAME)


# In[ ]:


class AqueductSettings:
  rares_detection_radius = 50
  blues_detection_radius = 50
class Aqueduct:
  look_for_objects_orig = ["Waypoint", "Highgate"]
  look_for_objects = ["Waypoint", "Highgate"]
  def __init__(self, poe_bot:PoeBot) -> None:
    self.poe_bot = poe_bot
  def run(self):
    self.poe_bot.on_death_function = self.onDeathFunction
    if poe_bot.game_data.area_raw_name == "2_9_town":
      inventory = poe_bot.ui.inventory
      stashed = False
      inventory.update()
      filled_slots_count = len(inventory.getFilledSlots())
      if filled_slots_count > 30:
        stash_box = next((e for e in poe_bot.game_data.entities.all_entities if "Stash" in e.path), None)
        if stash_box is None:
          poe_bot.raiseLongSleepException('stashbox is not found in highgate')
        mover.goToEntitysPoint(stash_box, release_mouse_on_end=True)
        stash = poe_bot.ui.stash
        stash.open()
        inventory.update()
        stash.placeItemsAcrossStash(inventory.items)
      poe_bot.ui.closeAll()

      aqueduct_transition = next((e for e in poe_bot.game_data.entities.all_entities if e.render_name == "The Blood Aqueduct"), None)



      if aqueduct_transition.distance_to_player > 40:
        mover.goToEntitysPoint(aqueduct_transition, release_mouse_on_end=True)

      for i in range(random.randint(5,10)):
        poe_bot.helper_functions.lvlUpGem()

      time.sleep(random.randint(20,40)/10)
      poe_bot.refreshInstanceData()
      aqueduct_transition = next((e for e in poe_bot.game_data.entities.all_entities if e.render_name == "The Blood Aqueduct"), None)

      # ctrl + click 196 365
      bot_controls.keyboard_pressKey('DIK_LCONTROL')
      pos_x,pos_y = poe_bot.convertPosXY(aqueduct_transition.location_on_screen.x,aqueduct_transition.location_on_screen.y)
      print(pos_x,pos_y)
      poe_bot.bot_controls.mouse.setPosSmooth(int(pos_x),int(pos_y))
      time.sleep(0.2)
      poe_bot.bot_controls.mouseClick(int(pos_x),int(pos_y))
      time.sleep(0.8)
      # release ctrl
      bot_controls.keyboard_releaseKey('DIK_LCONTROL')
      time.sleep(3) # till window is loaded

      # click new instance 165 240
      pos_x,pos_y = poe_bot.convertPosXY(165,240)
      print(pos_x,pos_y)
      poe_bot.bot_controls.mouse.setPosSmooth(int(pos_x),int(pos_y))
      time.sleep(0.2)
      poe_bot.bot_controls.mouseClick(int(pos_x),int(pos_y))
      time.sleep(0.8)
      time.sleep(5)
      raise 404
    elif poe_bot.game_data.area_raw_name == "2_9_1":
      poe_bot.combat_module.build.doPreparations()
    else:
      poe_bot.raiseLongSleepException('bring me to aqueduct or highgate')
  def aqueductFinishFunction(self):
    target = list(filter(lambda e: e.render_name in self.look_for_objects, poe_bot.game_data.entities.all_entities))
    if target:
      return True
  def resetInstance(self):
    targets = list(filter(lambda e: e.render_name in self.look_for_objects_orig, poe_bot.game_data.entities.all_entities))
    target = targets[0]
    if target.render_name == "Highgate":
      mover.goToEntitysPoint(target)
      target.clickTillNotTargetable()
    if target.render_name == "Waypoint":
      mover.goToEntitysPoint(target, release_mouse_on_end=True)
      for i in range(random.randint(5,10)):
        poe_bot.helper_functions.lvlUpGem()
      target.openWaypoint()
      # part 2 280 82
      pos_x,pos_y = poe_bot.convertPosXY(240,82)
      print(f"clicking part2 {pos_x,pos_y}")
      poe_bot.bot_controls.mouse.setPosSmooth(int(pos_x),int(pos_y))
      time.sleep(0.2)
      poe_bot.bot_controls.mouseClick(int(pos_x),int(pos_y))
      time.sleep(0.8)


      quest_flags = poe_bot.backend.getQuestFlags()
      a9_boss_killed = quest_flags.get("A9Q1KilledBoss", False)
      print(f"a9_boss_killed {a9_boss_killed}")
      if a9_boss_killed is True:
        # act 9 285 105 if act10 town is opened
        pos_x,pos_y = poe_bot.convertPosXY(285,105)
      else:
        # act 9 319 105 if act10 town is closed
        pos_x,pos_y = poe_bot.convertPosXY(319,105)

      print(f"clicking a9 {pos_x,pos_y}")
      poe_bot.bot_controls.mouse.setPosSmooth(int(pos_x),int(pos_y))
      time.sleep(0.2)
      poe_bot.bot_controls.mouseClick(int(pos_x),int(pos_y))
      time.sleep(0.8)

      # ctrl + click 196 365
      bot_controls.keyboard_pressKey('DIK_LCONTROL')
      pos_x,pos_y = poe_bot.convertPosXY(196,365)
      print(pos_x,pos_y)
      poe_bot.bot_controls.mouse.setPosSmooth(int(pos_x),int(pos_y))
      time.sleep(0.2)
      poe_bot.bot_controls.mouseClick(int(pos_x),int(pos_y))
      time.sleep(0.8)
      # release ctrl
      bot_controls.keyboard_releaseKey('DIK_LCONTROL')
      time.sleep(3) # till window is loaded

      # click new instance 165 240
      pos_x,pos_y = poe_bot.convertPosXY(165,240)
      print(pos_x,pos_y)
      poe_bot.bot_controls.mouse.setPosSmooth(int(pos_x),int(pos_y))
      time.sleep(0.2)
      poe_bot.bot_controls.mouseClick(int(pos_x),int(pos_y))
      time.sleep(0.8)

      waypoint_grid_pos_sum = target.grid_position.x + target.grid_position.y
      time.sleep(5)
      poe_bot.refreshInstanceData()
      # supposed to throw error that loc has changed
      targets = list(filter(lambda e: e.render_name in self.look_for_objects, poe_bot.game_data.entities.all_entities))
      target = targets[0]
      new_waypoint_grid_pos_sum = target.grid_position.x + target.grid_position.y
      # if waypoint_grid_pos_sum == new_waypoint_grid_pos_sum:
      #   poe_bot.raiseLongSleepException('couldnt create new area')
  def onDeathFunction(self):
    poe_bot.resurrectAtCheckpoint()
    poe_bot.refreshInstanceData()
    self.resetInstance()
    raise Exception('died resetting')


# In[ ]:


aqueduct_module = Aqueduct(poe_bot=poe_bot)
aqueduct_module.run()


# In[ ]:


poe_bot.mover.default_continue_function = poe_bot.combat_module.build.usualRoutine
aqueduct_loot_filter = CustomLootFilter(collect_links=None,collect_small_rgb=CHROMATICS_RECIPE)
poe_bot.loot_picker.loot_filter.special_rules = [aqueduct_loot_filter.isItemPickable]


# In[ ]:


rares_detection_radius = 50
blues_detection_radius = 50
look_for_objects_orig = ["Waypoint", "Highgate"]
look_for_objects = ["Waypoint", "Highgate"]

waypoints_or_transitions = list(filter(lambda e: e.render_name == "Waypoint" or e.render_name == "Highgate", poe_bot.game_data.entities.all_entities))
for entity in waypoints_or_transitions:
  entity_index = look_for_objects.index(entity.render_name)
  look_for_objects.pop(entity_index)

if len(look_for_objects) == 0:
  poe_bot.raiseLongSleepException("len(look_for_objects) == 0")


# In[ ]:


def aqueductFinishFunction():
  target = list(filter(lambda e: e.render_name in look_for_objects, poe_bot.game_data.entities.all_entities))
  if target:
    return True
def aqueductRunRoutine(self, mover=None):
  '''
  if function returns something other than bool:False, itll regenerate it's path
  '''
  if rares_detection_radius != 0:
    rares_nearby = list(filter(lambda e: e.distance_to_player < rares_detection_radius, poe_bot.game_data.entities.attackable_entities_rares))
    for rare_mob in rares_nearby:
      updated_entity = list(filter(lambda e: e.id == rare_mob.id, poe_bot.game_data.entities.attackable_entities_rares))
      if len(updated_entity) != 0:
        updated_entity = updated_entity[0]
        poe_bot.combat_module.killUsualEntity(updated_entity)
        return True

  if blues_detection_radius != 0:
    rares_nearby = list(filter(lambda e: e.distance_to_player < blues_detection_radius, poe_bot.game_data.entities.attackable_entities_blue))
    for blue_mob in rares_nearby:
      updated_entity = list(filter(lambda e: e.id == blue_mob.id, poe_bot.game_data.entities.attackable_entities_blue))
      if len(updated_entity) != 0:
        updated_entity = updated_entity[0]
        poe_bot.combat_module.killUsualEntity(updated_entity)
        return True
      
  loot_collected = poe_bot.loot_picker.collectLoot()
  if loot_collected is True:
    return loot_collected
  #   if len(inventory.getFilledSlots()) > 51:
  #     self.can_pick_drop = False
  #   else:
  #     self.can_pick_drop = True
  if aqueductFinishFunction() is True:
    return True
  return False


# In[ ]:


from utils.pathing import TSP

mover_custom_break_function = aqueductRunRoutine
explorer_break_function = aqueductFinishFunction

tsp = TSP(poe_bot=poe_bot)
# tsp.generatePointsForDiscovery()
mover = poe_bot.mover
map_complete = False
while map_complete is False:
  poe_bot.refreshInstanceData()
  print(f'generating pathing points')
  discovery_points = tsp.generateSortedPointsForBossRush()
  print(f'len(discovery_points) {len(discovery_points)}')
  discovery_points = list(filter(lambda p: poe_bot.helper_functions.checkIfEntityOnCurrenctlyPassableArea(p[0], p[1]), discovery_points))
  print(f'len(discovery_points) {len(discovery_points)} after sorting')
  if len(discovery_points) == 0:
    print(f'len(discovery_points) == 0 after points generation')
    map_complete = True
    break
  point_to_go = discovery_points.pop(0)
  while point_to_go is not None:
    need_to_explore = True
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
      custom_break_function=mover_custom_break_function,
      step_size=random.randint(30,35)
    )
    # then, it result is True, False or None
    print(f"mover.goToPoint result {result}")


    # if we arrived to discovery point and nothing happened
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
    
    if explorer_break_function() is True:
      map_complete = True
      break

    poe_bot.refreshInstanceData()
    poe_bot.last_action_time = 0
  # if possible_transition to explore, go to it, run discovery again



# In[ ]:


aqueduct_module.resetInstance()


# In[ ]:


raise Exception('finished, all good')


# In[ ]:


poe_bot.refreshAll()

list(filter(lambda e: e.life.health.current != 0 and not e.is_hostile and e.distance_to_player < 50 and "Metadata/Monsters/Totems/ShotgunTotem" in e.path, poe_bot.game_data.entities.all_entities))


# In[ ]:


list(filter(lambda e: e.life.health.current != 0 and not e.is_hostile and e.distance_to_player < 50 and "Metadata/Monsters/Totems/ShotgunTotem" in e.path, poe_bot.game_data.entities.all_entities))


# In[ ]:


nearby_totems = list(filter(lambda e: "Metadata/Monsters/Totems/ShotgunTotem" in e.path, poe_bot.game_data.entities.all_entities))


# In[ ]:


nearby_totems[0].raw

