import json
import os

from flask import Blueprint, jsonify, render_template, request

CONFIGS_PATH = "./configs/"
DEFAULTS_PATH = "./defaults/"

if not os.path.exists(CONFIGS_PATH):
  print(f'creating configs folder')
  os.makedirs(CONFIGS_PATH)

class MapperConfigsDB:
  config:dict
  def __init__(self) -> None:
    # attempt to load mapper configs, else use defaults
    self.file_path = f'{CONFIGS_PATH}mapper_configs.json'
    self.load()
  def load(self):
    try:
      file = open(self.file_path, encoding='utf-8')
      self.config = json.load(file)
      file.close()
      print(f'loaded from file')
    except FileNotFoundError:
      print("using defaults")
      file = open(f'{DEFAULTS_PATH}mapper_configs.json', encoding='utf-8')
      self.config = json.load(file)
      file.close()
      self.save()    
  
  def save(self):
    file = open(self.file_path, 'w', encoding='utf-8')
    json.dump(self.config, file, ensure_ascii=False, indent=4)
    file.close()
  
  def toJson(self) -> dict:
    return self.config
mapper_configs_db = MapperConfigsDB()


mapper_configs_bp = Blueprint('mapper_configs', __name__, url_prefix='/mapper_configs')
@mapper_configs_bp.route("/ping")
def ping():
  return jsonify({"result": 200})

@mapper_configs_bp.route("/")
def main():
  return render_template('mapper_configs_main.html', data=mapper_configs_db.toJson())

def formField(type = "text", disabled = True):
  return {
    "type": type,
    "disabled": disabled,
  }
def checkoutField():
  return formField(type = "checkbox", disabled = False)
def textField():
  return formField(type = "text", disabled = False)
def numberField():
  return formField(type = "text", disabled = False)

form_fields = {
  'alch_chisel':checkoutField(), 
  'alva_clear_room':checkoutField(), 
  'alva_ignore_temple_mechanics':checkoutField(), 
  'alva_skip_map_if_finished_incursion_and_have_priority_map_in_inventory':checkoutField(), 
  'atlas_explorer':checkoutField(), 
  'beast_farmer':checkoutField(), 
  'beast_search_string':textField(), 
  'boss_rush':checkoutField(), 
  'can_corrupt_essenecs':checkoutField(), 
  'clear_around_shrines':checkoutField(), 
  'collect_beasts_every_x_maps':numberField(), 
  'do_abysses':checkoutField(), 
  'do_alva':checkoutField(), 
  'do_blight':checkoutField(), 
  'do_essences':checkoutField(), 
  'do_harbringers':checkoutField(), 
  'do_harvest':checkoutField(), 
  'do_legion':checkoutField(), 
  'essences_can_corrupt':checkoutField(), 
  'essences_do_all':checkoutField(), 
  'essences_min_to_corrupt':checkoutField(), 
  'force_deli':checkoutField(), 
  'force_kill_blue':checkoutField(), 
  'force_kill_boss':checkoutField(), 
  'force_kill_rares':checkoutField(), 
  'force_kill_rogue_exiles':checkoutField(), 
  'growing_hordes':formField(), 
  'incursion_valuable_rooms':formField(), 
  'invitation_rush':checkoutField(), 
  'keep_consumables':formField(), 
  'keep_maps_in_inventory':formField(), 
  'map_device_option':formField(), 
  'map_priorities':formField(), 
  'musthave_map_device_modifiers':formField(), 
  'one_portal':checkoutField(), 
  'party_ultimatum':checkoutField(), 
  'prefer_high_tier':checkoutField(), 
  'prefered_map_device_modifiers':formField(), 
  'prefered_tier':formField(), 
  'release_beasts':checkoutField(), 
  'use_timeless_scarab_if_connected_or_presented':checkoutField(), 
  'wait_for_deli_drops':checkoutField(), 
  'wildwood_jewel_farm':formField()
}

@mapper_configs_bp.route("/edit")
def edit():
  config_index = request.args.get('index', None)
  config = None
  if config_index and config_index != "new":
    config_title = list(mapper_configs_db.config.keys())[int(config_index)]
    config = mapper_configs_db.config[config_title]
    config['title'] = config_title
  return render_template('mapper_configs_edit.html', data=config, form_fileds=form_fields)
