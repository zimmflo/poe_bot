#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import random
import sys
from ast import literal_eval

from utils.gamehelper import PoeBot


# In[2]:


notebook_dev = False
# readability
poe_bot: PoeBot


# In[3]:


from utils.constants import SKILLS_INTERNAL_NAMES
from utils.combat import Build, AutoFlasks, SkillWithDelay, AreaSkill, MovementSkill, MinionSkillWithDelay, Skill
from utils.mover import Mover
from utils.gamehelper import Entity
from utils.utils import getAngle

from math import dist

class DodgeRoll(SkillWithDelay):
  def __init__(self, poe_bot, skill_index=3, skill_name='', display_name="DodgeRoll", min_delay=random.uniform(0.4,0.5), delay_random=0.1, min_mana_to_use=0, can_use_earlier=True):
    super().__init__(poe_bot, skill_index, skill_name, display_name, min_delay, delay_random, min_mana_to_use, can_use_earlier)
    self.skill_key = "DIK_SPACE"
    self.tap_func = poe_bot.bot_controls.keyboard.pressAndRelease
    self.press_func = poe_bot.bot_controls.keyboard_pressKey
    self.release_func = poe_bot.bot_controls.keyboard_releaseKey


class InfernalistZoomancer(Build):
  '''
  '''
  poe_bot: PoeBot
  def __init__(self,poe_bot: PoeBot) -> None:
    self.poe_bot = poe_bot
    
    self.max_srs_count = 10

    flame_wall_index = 3
    unearth_index = 4
    detonate_dead_index = 5
    offerening_index = 6
    flammability_index = 7

    self.fire_skills = []

    Skill.checkIfCanUse = lambda *args, **kwargs: True
    Skill.getCastTime = lambda *args, **kwargs: 0.7


    if flame_wall_index != None:
      self.flame_wall = SkillWithDelay(poe_bot=poe_bot, skill_index=flame_wall_index, min_delay=random.randint(20,30)/10, display_name="flame_wall", min_mana_to_use=0, can_use_earlier=False)
      self.fire_skills.append(self.flame_wall)

    if unearth_index != None:
      self.unearth = SkillWithDelay(poe_bot=poe_bot, skill_index=unearth_index, min_delay=random.randint(20,30)/10, display_name="unearth", min_mana_to_use=0, can_use_earlier=False)

    if detonate_dead_index != None:
      self.detonate_dead = SkillWithDelay(poe_bot=poe_bot, skill_index=detonate_dead_index, min_delay=random.uniform(3.1, 4.5), display_name="detonate_dead", min_mana_to_use=0, can_use_earlier=False)
      self.fire_skills.append(self.detonate_dead)
    
    if offerening_index != None:
      self.offering = SkillWithDelay(poe_bot=poe_bot, skill_index=offerening_index, min_delay=random.randint(20,30)/10, display_name="offering", min_mana_to_use=0, can_use_earlier=False)

    if flammability_index != None:
      self.flammability = SkillWithDelay(poe_bot=poe_bot, skill_index=flammability_index, min_delay=random.randint(20,30)/10, display_name="flammability", min_mana_to_use=0, can_use_earlier=False)

    self.dodge_roll = DodgeRoll(poe_bot=poe_bot)

    super().__init__(poe_bot)
    self.auto_flasks = AutoFlasks(poe_bot=poe_bot)
  def useBuffs(self):
    return False
  def usualRoutine(self, mover:Mover = None):
    print(f'calling usual routine')
    poe_bot = self.poe_bot
    self.auto_flasks.useFlasks()

    # if we are moving
    if mover is not None:
      self.useBuffs()
      attacking_skill_delay = 2

      nearby_enemies = list(filter(lambda e: e.isInRoi(), poe_bot.game_data.entities.attackable_entities))
      print(f'nearby_enemies: {nearby_enemies}')
      really_close_enemies = list(filter(lambda e: e.distance_to_player < 20,nearby_enemies))
      





      min_delay = 3
      if len(really_close_enemies) != 0:
        min_delay = 2
        attacking_skill_delay = 0.7

      enemy_to_attack = None
      if len(really_close_enemies) != 0:
        enemy_to_attack = really_close_enemies[0]
      elif len(nearby_enemies):
        nearby_enemies = sorted(nearby_enemies, key=lambda e: e.distance_to_player)
        nearby_enemies = list(filter(lambda e: e.isInLineOfSight() is True, nearby_enemies))
        if len(nearby_enemies) != 0:
          enemy_to_attack = nearby_enemies[0]
      
      if enemy_to_attack is not None:
        if self.flame_wall and self.flame_wall.last_use_time + attacking_skill_delay < time.time():
          alive_srs_nearby = list(filter(lambda e: not e.is_hostile and e.life.health.current != 0 and e.distance_to_player < 150 and "Metadata/Monsters/RagingSpirit/RagingSpiritPlayerSummoned" in e.path , self.poe_bot.game_data.entities.all_entities))
          if len(alive_srs_nearby) < self.max_srs_count:
            print(f'[Generic summoner] need to raise srs')
            if self.flame_wall.use(updated_entity=enemy_to_attack) == True:
              return True
        if self.detonate_dead and self.detonate_dead.canUse():
          corpses_around = poe_bot.game_data.entities.getCorpsesArountPoint(poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y, 40)
          corpses_around = list(filter(lambda e: e.isInLineOfSight() != False, corpses_around))
          if len(corpses_around) != 0:
            corpses_around.sort(key=lambda e: e.calculateValueForAttack())
            if corpses_around[0].attack_value != 0:
              if self.detonate_dead.use(updated_entity=corpses_around[0]) != False:
                return True
        if self.unearth and self.unearth.canUse():
          corpses_around = poe_bot.game_data.entities.getCorpsesArountPoint(poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y, 20)
          corpses_around = list(filter(lambda e: e.isInLineOfSight() != False, corpses_around))
          if len(corpses_around) != 0:
            corpses_around.sort(key=lambda e: e.calculateValueForAttack())
            if corpses_around[0].attack_value != 0:
              if self.unearth.use(updated_entity=corpses_around[0]) != False:
                return True
            
      p0 = (mover.grid_pos_to_step_x, mover.grid_pos_to_step_y)
      p1 = (poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y)
      
      extremley_close_entities = list(filter(lambda e: e.distance_to_player < 5, really_close_enemies))
      enemies_on_way = list(filter(lambda e: e.distance_to_player < 10 and getAngle(p0, p1, (e.grid_position.x, e.grid_position.y), abs_180=True) < 25, really_close_enemies))
      if extremley_close_entities or enemies_on_way:
        if self.dodge_roll.use() == True:
          return True
      # # use movement skill
      # if self.movement_skill and mover.distance_to_target > 50:
      #   if self.movement_skill.use(mover.grid_pos_to_step_x, mover.grid_pos_to_step_y, wait_for_execution=False) is True:
      #     return True
    
    # if we are staying and waiting for smth
    else:
      self.staticDefence()

    return False
  def prepareToFight(self, entity: Entity):
    print(f'[InfernalistZoomancer.prepareToFight] call {time.time()}')
    for i in range(random.randint(2,3)):
      self.poe_bot.refreshInstanceData()
      self.auto_flasks.useFlasks()
      updated_entity = next( (e for e in self.poe_bot.game_data.entities.all_entities if e.id == entity.id), None)
      if updated_entity is None:
        break

      self.flame_wall.use(updated_entity=updated_entity)
    return True
  def killUsual(self, entity:Entity, is_strong = False, max_kill_time_sec = random.randint(200,300)/10, *args, **kwargs):
    print(f'#build.killUsual {entity}')
    poe_bot = self.poe_bot
    mover = self.mover

    entity_to_kill_id = entity.id
    debuff_use_time = 0

    self.auto_flasks.useFlasks()
    
    min_distance = 40 # distance which is ok to start attacking
    keep_distance = 15 # if our distance is smth like this, kite

    entity_to_kill = next((e for e in poe_bot.game_data.entities.attackable_entities if e.id == entity_to_kill_id), None)
    if not entity_to_kill:
      print('cannot find desired entity to kill')
      return True

    print(f'entity_to_kill {entity_to_kill}')
    
    if entity_to_kill.life.health.current < 0:
      print('entity is dead')
      return True

    distance_to_entity = dist( (entity_to_kill.grid_position.x, entity_to_kill.grid_position.y), (poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y) ) 
    print(f'distance_to_entity {distance_to_entity} in killUsual')
    if distance_to_entity > min_distance:
      print('getting closer in killUsual ')
      return False
    
    if entity_to_kill.isInLineOfSight() is False:
      print('entity_to_kill.isInLineOfSight() is False')
      return False


    start_time = time.time()
    entity_to_kill.hover(wait_till_executed=False)
    poe_bot.last_action_time = 0
    kite_distance = random.randint(18,22)
    res = True
    reversed_run = random.choice([True, False])



    while True:
      skill_used = False
      poe_bot.refreshInstanceData()
      self.auto_flasks.useFlasks()
      if self.poe_bot.game_data.player.life.health.getPercentage() < self.auto_flasks.hp_thresh:
        pass #TODO kite?

      entity_to_kill = next((e for e in poe_bot.game_data.entities.attackable_entities if e.id == entity_to_kill_id), None)
      if not entity_to_kill:
        print('cannot find desired entity to kill')
        break
      print(f'entity_to_kill {entity_to_kill}')
      if entity_to_kill.life.health.current < 1:
        print('entity is dead')
        break

      distance_to_entity = dist( (entity_to_kill.grid_position.x, entity_to_kill.grid_position.y), (poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y) ) 
      print(f'distance_to_entity {distance_to_entity} in killUsual')
      if distance_to_entity > min_distance:
        print('getting closer in killUsual ')
        break
      current_time = time.time()
      skill_used = self.useBuffs()
      skill_use_delay = random.randint(20,30)/10
      print(f'skill_use_delay {skill_use_delay}')




      if skill_used is False and self.flame_wall and self.flame_wall.last_use_time + skill_use_delay < time.time():
        alive_srs_nearby = list(filter(lambda e: not e.is_hostile and e.life.health.current != 0 and e.distance_to_player < 150 and "Metadata/Monsters/RagingSpirit/RagingSpiritPlayerSummoned" in e.path , self.poe_bot.game_data.entities.all_entities))
        if len(alive_srs_nearby) < self.max_srs_count:
          print(f'[Generic summoner] need to raise srs')
          if self.flame_wall.use(updated_entity=entity_to_kill) == True:
            skill_used = True
      if skill_used is False and self.detonate_dead and self.detonate_dead.canUse():
        corpses_around = poe_bot.game_data.entities.getCorpsesArountPoint(poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y, 40)
        corpses_around = list(filter(lambda e: e.isInLineOfSight() != False, corpses_around))
        if len(corpses_around) != 0:
          corpses_around.sort(key=lambda e: e.calculateValueForAttack())
          if corpses_around[0].attack_value != 0:
            if self.detonate_dead.use(updated_entity=corpses_around[0]) != False:
              skill_used = True
      if skill_used is False and self.unearth and self.unearth.canUse():
        corpses_around = poe_bot.game_data.entities.getCorpsesArountPoint(poe_bot.game_data.player.grid_pos.x, poe_bot.game_data.player.grid_pos.y, 20)
        corpses_around = list(filter(lambda e: e.isInLineOfSight() != False, corpses_around))
        if len(corpses_around) != 0:
          corpses_around.sort(key=lambda e: e.calculateValueForAttack())
          if corpses_around[0].attack_value != 0:
            if self.unearth.use(updated_entity=corpses_around[0]) != False:
              skill_used = True


      if skill_used != True:
        print('kiting')
        point = self.poe_bot.game_data.terrain.pointToRunAround(entity_to_kill.grid_position.x, entity_to_kill.grid_position.y, kite_distance+random.randint(-1,1), check_if_passable=True, reversed=reversed_run)
        mover.move(grid_pos_x = point[0], grid_pos_y = point[1])




      if current_time  > start_time + max_kill_time_sec:
        print('exceed time')
        break
    return res


# In[4]:


default_config = {
  "REMOTE_IP": '172.23.178.57', # z2
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
  parsed_config['unique_id'] = PoeBot.getDevKey()

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


ARTS_TO_PICK = [
  "Art/2DItems/Currency/CurrencyModValues.dds",
  "Art/2DItems/Currency/CurrencyGemQuality.dds",
  "Art/2DItems/Currency/CurrencyRerollRare.dds",
  "Art/2DItems/Currency/CurrencyAddModToRare.dds",
  "Art/2DItems/Currency/CurrencyUpgradeToUniqueShard.dds"
]


# In[7]:


poe_bot = PoeBot(unique_id = UNIQUE_ID, remote_ip = REMOTE_IP, password=password)

def clickResurrect_POE2(town = False):
  # poe_bot = self.poe_bot
  pos_x, pos_y = random.randint(430,580), random.randint(560,570)
  pos_x, pos_y = poe_bot.convertPosXY(pos_x, pos_y)
  time.sleep(random.randint(20,80)/100)
  poe_bot.bot_controls.mouse.setPosSmooth(pos_x, pos_y)
  time.sleep(random.randint(20,80)/100)
  poe_bot.bot_controls.mouse.click()
  time.sleep(random.randint(30,60)/100)
  return True


poe_bot.ui.resurrect_panel.clickResurrect = clickResurrect_POE2

poe_bot.refreshAll()
poe_bot.game_data.terrain.getCurrentlyPassableArea()



# In[8]:


from utils.loot_filter import PickableItemLabel
def isItemHasPickableKey(item_label:PickableItemLabel):
  if item_label.icon_render in ARTS_TO_PICK:
    return True
  return False
poe_bot.loot_picker.loot_filter.special_rules = [isItemHasPickableKey]


# In[9]:


# poe_bot.mover.setMoveType('wasd')


# In[10]:


poe_bot.combat_module.build = InfernalistZoomancer(poe_bot=poe_bot)
poe_bot.mover.default_continue_function = poe_bot.combat_module.build.usualRoutine


# In[11]:


beetle_entity = next( (e for e in poe_bot.game_data.entities.attackable_entities_rares if e.render_name == "The Ninth Treasure of Keth"), None)
if beetle_entity:
  poe_bot.combat_module.killTillCorpseOrDisappeared(beetle_entity)
else:
  print(f'no entity found')


# In[12]:


start_time = time.time()

def destroyCorpse(corpse_entity:Entity):
  while True:
    poe_bot.refreshInstanceData()
    updated_corpse_entity = next( (e for e in poe_bot.game_data.entities.all_entities if e.id == corpse_entity.id), None)
    if updated_corpse_entity:
      if updated_corpse_entity.distance_to_player > 25:
        poe_bot.mover.goToEntitysPoint(updated_corpse_entity)
      else:
        if poe_bot.combat_module.build.detonate_dead and poe_bot.combat_module.build.detonate_dead.canUse():
          if poe_bot.combat_module.build.detonate_dead.use(updated_entity=updated_corpse_entity) != False:
            continue
        if poe_bot.combat_module.build.unearth and poe_bot.combat_module.build.unearth.canUse():
          if poe_bot.combat_module.build.unearth.use(updated_entity=updated_corpse_entity) != False:
            continue
    else:
      break
beetle_corpse = next( (e for e in poe_bot.game_data.entities.all_entities if e.render_name == "The Ninth Treasure of Keth"), None)
if beetle_corpse:
  destroyCorpse(beetle_corpse)


# In[ ]:


entity_to_run_around = None
if beetle_corpse:
  print(f'running around corpse {beetle_corpse}')
  entity_to_run_around = beetle_corpse
elif beetle_entity:
  print(f'running around entity {beetle_entity}')

  entity_to_run_around = beetle_entity

if entity_to_run_around:
  start_time = time.time()
  run_duration_seconds = 5
  end_at = start_time + run_duration_seconds
  kite_distance = 10
  reversed_run = random.choice([True, False])
  while time.time() < end_at:
    poe_bot.refreshInstanceData()
    poe_bot.combat_module.build.auto_flasks.useFlasks()  
    print('kiting')
    point = poe_bot.game_data.terrain.pointToRunAround(entity_to_run_around.grid_position.x, entity_to_run_around.grid_position.y, kite_distance+random.randint(-1,1), check_if_passable=True, reversed=reversed_run)
    poe_bot.mover.move(grid_pos_x = point[0], grid_pos_y = point[1])
else:
  poe_bot.refreshInstanceData()


# In[14]:


poe_bot.loot_picker.collectLootWhilePresented()


# In[15]:


def respawnAtCheckPoint():
  poe_bot.bot_controls.keyboard.tap('DIK_ESCAPE')
  time.sleep(random.randint(40,80)/100)
  pos_x, pos_y = random.randint(450,550), random.randint(289,290)
  pos_x, pos_y = poe_bot.convertPosXY(pos_x, pos_y)
  poe_bot.bot_controls.mouse.setPosSmooth(pos_x, pos_y)
  time.sleep(random.randint(40,80)/100)
  poe_bot.bot_controls.mouse.click()
  time.sleep(random.randint(30,60)/100)

  pos_x, pos_y = random.randint(580,640), random.randint(408,409)
  pos_x, pos_y = poe_bot.convertPosXY(pos_x, pos_y)
  time.sleep(random.randint(20,80)/100)
  poe_bot.bot_controls.mouse.setPosSmooth(pos_x, pos_y)
  time.sleep(random.randint(20,80)/100)
  poe_bot.bot_controls.mouse.click()
  time.sleep(random.randint(30,60)/100)
  return True
poe_bot.bot_controls.releaseAll()
respawnAtCheckPoint()
while True:
  poe_bot.refreshInstanceData()
  beetle_entity = next( (e for e in poe_bot.game_data.entities.all_entities if e.render_name == "The Ninth Treasure of Keth"), None)
  if beetle_entity:
    break


# In[16]:


raise 404


# In[ ]:


poe_bot.refreshInstanceData()
poe_bot.loot_picker.collectLoot()


# In[10]:


from utils.pathing import TSP


tsp = TSP(poe_bot=poe_bot)
# tsp.generatePointsForDiscovery()
mover = poe_bot.mover
map_complete = False
while map_complete is False:
  poe_bot.refreshInstanceData()
  print(f'generating pathing points')
  tsp.generatePointsForDiscovery()
  discovery_points = tsp.sortedPointsForDiscovery()
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
      custom_continue_function=poe_bot.combat_module.build.usualRoutine,
      # custom_break_function=mover_custom_break_function,
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
    
    # if explorer_break_function() is True:
    #   map_complete = True
    #   break

    poe_bot.refreshInstanceData()
    poe_bot.last_action_time = 0
  # if possible_transition to explore, go to it, run discovery again


# In[ ]:


raise 404

