
DEFAULT_SESSION = '24h' # '12h', '16h', '20h', '24h'

FAST_MAPS = ["Beach Map", "Strand Map","Dunes Map","Cemetery Map","Plateau Map", "Castle Ruins Map", "Colonnade Map", "Pier Map", "Port Map"]
ANOTHER_MAPS_1 = ["Strand Map", "Cemetary Map", "Canyon Map", "Atoll Map", "Primordial Pool Map"]
FAST_MAPS = ["Dunes Map", "City Square Map","Strand Map","Toxic Sewer Map","Jungle Valley Map","Bog Map","Beach Map","Cemetery Map"]
FAST_WHITE_MAPS = ["Dunes Map","Siege Map","Lava Lake Map","Strand Map","Bog Map"]
FAST_YELLOW_MAPS = ["Cemetary Map", "Canyon Map", "Volcano Map", "Strand Map",  "Atoll Map", "Primordial Pool Map"]
BESTIARY_SCARABS = ["Bestiary Scarab of the Herd", "Bestiary Scarab of the Herd", "Bestiary Scarab of Duplicating"]

all_settings = '''
atlas_explorer = False # prefer to run higher tier maps over lower tier

keep_consumables = []

alch_chisel = False # will use alch + chisel if it's possible
growing_hordes = False # can place whatever different scarabs in atlas map device

prefered_tier = None
keep_maps_in_inventory = 10

prefered_map_device_modifiers = [] # prefered items to place in addition to map in map device, will place them if have them in inventory or pick them from stash if possible
musthave_map_device_modifiers = [] # items to place in addition to map in map device, will throw an error if wont have them in inventory before running map

do_essences = False
essences_do_all = False
essences_can_corrupt = False
essences_min_to_corrupt = 6

party_ultimatum = False

do_harvest = False

force_kill_rogue_exiles = False

invitation_rush = False
invitation_type = 'blue' # 'red' 'blue'
wildwood_jewel_farm = False

clear_around_shrines = False

do_alva = False
alva_clear_room = False
alva_ignore_temple_mechanics = False
alva_skip_map_if_finished_incursion = False
alva_skip_map_if_finished_incursion_and_have_priority_map_in_inventory = False
alva_also_keep_temples_with = ["Locus of Corruption (Tier 3)", "Doryani's Institute (Tier 3)"]
incursion_valuable_rooms =  ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ]
use_timeless_scarab_if_connected_or_presented = []

low_priority_maps = []

do_beasts = False
release_beasts = True # will also release beasts if beast farmer is True
collect_beasts_every_x_maps:int = 30
beast_search_string = "cic c|id w|id v|le m|ld h|Black M"

max_map_run_time = 600

'''



PREDEFINED_STRATEGIES = {
  "all_settings": {
    "alch_chisel": False, # if True, will use chisel + alch if possible
    "prefer_high_tier": True, # True 16-1 False 1-16
    "prefered_tier": None, # None - no change, "yellow" will try to prefer the yellow maps 6/7/8/9/10 tier or 10/9/8/7/6 if prefer_high_tier is True
    "atlas_explorer": False, # will explore atlas
    # will pick these consumables and keep them in inventory
    "keep_consumables": ['Orb of Alchemy', 'Orb of Scouring', 'Scroll of Wisdom', 'Vaal Orb'],

    # ["Bestiary Scarab", "Bestiary Scarab", "Bestiary Scarab Of The Herd", "Bestiary Scarab"]
    # will try to place "Bestiary Scarab" and "Bestiary Scarab" and "Bestiary Scarab Of the Herd"
    # if the 5th slot is opened, will place one more "Bestiary Scarab" in addition
    # also pick them from stash if possible also will try to keep 3 * "Bestiary Scarab" and 1 * "Bestiary Scarab Of The Herd"

    # [] - will mean no prefered
    "prefered_map_device_modifiers": ["Bestiary Scarab", "Bestiary Scarab", "Bestiary Scarab Of The Herd", "Bestiary Scarab"], 

    "do_alva": False,
    "use_timeless_scarab_if_connected_or_presented": [],
    "alva_also_keep_temples_with":["Locus of Corruption (Tier 3)", "Doryani's Institute (Tier 3)"],

    # will clear around shrines and activate it if its immortal shrine
    "clear_around_shrines": False,

    # amount of maps its allowed to keep in inventory if stashing something
    "keep_maps_in_inventory": 10, 

    "one_portal": False,
    "force_kill_boss": True,
    "force_kill_blue": True,
    "force_kill_rares": False,
  },

  "atlas_explorer": {
    "atlas_explorer": True,
    "one_portal": False,
    "prefer_high_tier": True,
    "force_kill_boss": True,
    "force_kill_blue": True,
    "force_kill_rares": False,
  },
  "atlas_explorer_and_harbringers": {
    "atlas_explorer": True,
    "one_portal": False,
    "prefer_high_tier": True,
    "do_harbringers": True,
    "force_kill_boss": True,
    "force_kill_blue": True,
    "force_kill_rares": False,
  },
  
  "low_tier_incursion_locus_clear_room": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "use_timeless_scarab_if_connected_or_presented": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber"],
    "alva_clear_room": True,
  },

  "low_tier_incursion_locus_and_dory_clear_room": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "use_timeless_scarab_if_connected_or_presented": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "alva_clear_room": True,
  },

  "low_tier_incursion_locus_and_dory_no_scarab": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "alva_clear_room_if_need_to_connect": True,
    "map_priorities": FAST_WHITE_MAPS,
  },

  "low_tier_incursion": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "map_priorities": FAST_WHITE_MAPS,
  },

  "low_tier_incursion_weak": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "map_priorities": FAST_WHITE_MAPS,
    "alva_clear_room_if_need_to_connect": True,
  },
  
  "low_tier_incursion_rush_weak": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "map_priorities": FAST_WHITE_MAPS,
    "alva_clear_room_if_need_to_connect": True,
    "alva_skip_map_if_finished_incursion_and_have_priority_map_in_inventory": True,
  },

  "low_tier_incursion_rush": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "alva_skip_map_if_finished_incursion_and_have_priority_map_in_inventory": True,
    "alva_also_keep_temples_with":[],
    "map_priorities": FAST_WHITE_MAPS,
  },
  
  "low_tier_beast_no_scarabs": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "beast_search_string": "cic c",
    "map_priorities": FAST_WHITE_MAPS,
    "release_beasts": True,
  },

  "high_tier_beast_no_scarabs": {
    "force_kill_boss": False, 
    "prefer_high_tier": True,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "release_beasts": True,
  },

  "high_tier_beast_force_scarabs": {
    "force_kill_boss": False, 
    "prefer_high_tier": True,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "release_beasts": True,
    "musthave_map_device_modifiers": BESTIARY_SCARABS,
    "map_priorities": FAST_MAPS,
  },

  "high_tier_beast_locus_force_scarabs": {
    "force_kill_boss": False, 
    "prefer_high_tier": True,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "release_beasts": True,
    "musthave_map_device_modifiers": BESTIARY_SCARABS,
    "map_priorities": FAST_MAPS,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute" ],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "alva_clear_room_if_need_to_connect": True,
    "alva_skip_map_if_finished_incursion_and_have_priority_map_in_inventory": True,
    "alva_also_keep_temples_with":[],
  },

  "low_tier_beast_force_scarabs": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    # "beast_search_string": "cic c",
    "release_beasts": True,
    "musthave_map_device_modifiers": BESTIARY_SCARABS,
    "map_priorities": FAST_WHITE_MAPS,
    "beast_search_string": "cic c|id w|id v|le m|ld h|Black M",
    
  },

  "low_tier_locus_deli":{
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute"],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "alva_clear_room": True,
    "force_deli": True,
    "wait_for_deli_drops": True,
  },

  "low_tier_deli_incursion_collect_temples":{
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute"],
    "alva_clear_room": True,
    "force_deli": True,
    "wait_for_deli_drops": True,
  },

  "yellow_tier_deli_incursion":{
    "alch_chisel": True,
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "prefered_tier": "yellow",
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute"],
    "alva_ignore_temple_mechanics": True,
    "alva_clear_room": True,
    "force_deli": True,
    "wait_for_deli_drops": True,
  },

  "yellow_tier_deli_incursion_collect_temples":{
    "alch_chisel": True,
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "prefered_tier": "yellow",
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute"],
    "alva_clear_room": True,
    "force_deli": True,
    "wait_for_deli_drops": True,
  },

  
  "low_tier_deli_incursion_with_scarab":{
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute"],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "alva_clear_room": True,
    "map_priorities": FAST_MAPS,
    "force_deli": True,
    "wait_for_deli_drops": True,
  },

  "high_tier_deli_incursion":{
    "force_kill_boss": False, 
    "prefer_high_tier": True,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute"],
    "alva_ignore_temple_mechanics": True,
    "alva_clear_room": True,
    "map_priorities": FAST_MAPS,
    "force_deli": True,
    "wait_for_deli_drops": True,
  },

  "high_tier_deli_incursion_with_scarab":{
    "force_kill_boss": False, 
    "prefer_high_tier": True,
    "do_alva": True,
    "incursion_valuable_rooms": ["Locus of Corruption", "Catalyst of Corruption", "Corruption Chamber", "Gemcutter's Workshop", "Department of Thaumaturgy", "Doryani's Institute"],
    "use_timeless_scarab_if_connected_or_presented": ["Corruption Chamber", "Catalyst of Corruption", "Locus of Corruption"],
    "alva_clear_room": True,
    "map_priorities": FAST_MAPS,
    "force_deli": True,
    "wait_for_deli_drops": True,
  },

  # white tier essences
  "essence_early": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "map_priorities": FAST_MAPS,
    "essences_can_corrupt": False,
  },
  # yellow tier essences
  "essence_early_yellow": {
    "force_kill_boss": False,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "map_priorities": FAST_MAPS,
    "essences_can_corrupt": False,
  },
  # yellow tier essences with scarabs
  "lowtier_ess_expensive_ascent_force": {
    "force_kill_boss": False,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "musthave_map_device_modifiers": ["Essence Scarab", "Essence Scarab", "Essence Scarab of Ascent", "Essence Scarab",], 
    "essences_can_corrupt": True,
    "essences_min_to_corrupt": 8,
    "map_priorities": FAST_YELLOW_MAPS,
  },
  # yellow tier essences with scarabs and map device mod
  "lowtier_ess_expensive_ascent_force_no_wailing": {
    "force_kill_boss": False,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": False,
    "prefered_map_device_modifiers": ["Essence Scarab", "Essence Scarab", "Essence Scarab", "Essence Scarab",], 
    "essences_can_corrupt": True,
    "essences_min_to_corrupt": 8,
    "map_priorities": FAST_YELLOW_MAPS,
  },
  "lowtier_ess_expensive_ascent_force_no_wailing_map_device": {
    "force_kill_boss": False,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": False,
    "musthave_map_device_modifiers": ["Essence Scarab", "Essence Scarab", "Essence Scarab of Ascent", "Essence Scarab",], 
    "map_device_option": 'Essence',
    "essences_can_corrupt": True,
    "essences_min_to_corrupt": 8,
    "map_priorities": FAST_YELLOW_MAPS,
  },
  "lowtier_ess_expensive_ascent": {
    "force_kill_boss": False,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "prefered_map_device_modifiers": ["Essence Scarab", "Essence Scarab", "Essence Scarab of Ascent", "Essence Scarab",], 
    "map_device_option": 'Essence',
    "essences_can_corrupt": True,
    "essences_min_to_corrupt": 8,
    "map_priorities": FAST_YELLOW_MAPS,
  },

  "yellowtier_ess_expensive": {
    "force_kill_boss": False,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "prefered_map_device_modifiers": ["Essence Scarab", "Essence Scarab", "Essence Scarab", "Essence Scarab",], 
    "map_device_option": 'Essence',
    "essences_can_corrupt": True,
    "essences_min_to_corrupt": 8,
    "map_priorities": FAST_YELLOW_MAPS,
  },


  "ultimatum_leader": {
    "prefer_high_tier": True,
    "party_ultimatum": True,
    "prefered_map_device_modifiers": [], 
  },




  "lowtier_rogue": {
    "alch_chisel": True,
    "force_kill_boss": False,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "force_kill_rogue_exiles": True,
    "map_priorities": FAST_YELLOW_MAPS,
  },
  "lowtier_rogue_ess": {
    "alch_chisel": True,
    "force_kill_boss": True,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "force_kill_rogue_exiles": True,
    "map_device_option": 'Essence',
    "map_priorities": FAST_YELLOW_MAPS,
  },
  "lowtier_rogue_ess_early": {
    "force_kill_boss": True,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "force_kill_rogue_exiles": True,
    # "map_priorities": ANOTHER_MAPS,
  },
  "lowtier_rogue_ess_no_alch": {
    "alch_chisel": False,
    "force_kill_boss": True,
    "prefered_tier": "yellow",
    "prefer_high_tier": False,
    "do_essences": True,
    "essences_do_all": True,
    "force_kill_rogue_exiles": True,
    "map_device_option": 'Essence',
    "map_priorities": FAST_YELLOW_MAPS,
  },

  "lowtier_delirium_harbringers": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "do_harbringers": True,
    "force_deli": True,
    "wait_for_deli_drops": True,
    "map_priorities": FAST_YELLOW_MAPS,
  },

  "high_tier_rogue_harbringers_scarabs_farm": {
    "force_kill_boss": False,
    "prefer_high_tier": True,
    "do_harbringers": True,
    "alch_chisel": True,
    # "force_kill_rogue_exiles": True
  },

  "harvest_harbringers_high_tier": {
    "prefer_high_tier": True,
    "do_harvest": True,
    "do_harbringers": True,
    "alch_chisel": True,
    "force_kill_boss": False, 
    "force_kill_blue": True,
    "force_kill_rares": False,
  },

  "boss_rush": {
    "boss_rush": True,
    "force_kill_boss": True,
    # "force_kill_mobs": True, #TODO blue + rare mobs
    "do_essences": False,
    "do_legion": False,
    "do_blight": False,
    "force_deli": False,
  },
  

  "low_tier_essence": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "do_essences": True,
    "map_device_option": 'Essence'
  },
  "low_tier_essence_deli_lowcost": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "prefered_tier": "yellow",
    "force_deli": True,
    "wait_for_deli_drops": True,
    "keep_consumables": ['Remnant of Corruption'],
    "do_essences": True,
    "can_corrupt_essenecs": True,
    "essences_do_all": True,
    # "map_priorities": FAST_MAPS,
  },
  "low_tier_essence_deli_lowcost_no_corruption": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "prefered_tier": "yellow",
    "force_deli": True,
    "wait_for_deli_drops": True,
    "do_essences": True,
    "can_corrupt_essenecs": False,
    "essences_do_all": True,
    # "map_priorities": FAST_MAPS,
  },
  "low_tier_essence_deli": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "prefered_tier": "yellow",
    "force_deli": True,
    "wait_for_deli_drops": True,
    "keep_consumables": ['Remnant of Corruption'],
    "prefered_map_device_modifiers": ["Essence Scarab"],
    "do_essences": True,
    "can_corrupt_essenecs": True,
    "essences_do_all": True,
    # "map_priorities": FAST_MAPS,
    "map_device_option": 'Essence'
  },

  "lowtier_harbringer_delirium": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "prefered_tier": "yellow",
    "do_harbringers": True,
    "force_deli": True,
    "wait_for_deli_drops": True,
    "force_kill_rogue_exiles": True,

  },

  "low_tier_essence_deli_old": {
    "force_kill_boss": False,
    "prefer_high_tier": False,
    "force_deli": True,
    "wait_for_deli_drops": True,
    "keep_consumables": ['Remnant of Corruption'],
    "do_essences": True,
    "can_corrupt_essenecs": True,
    "essences_do_all": False,
    "map_priorities": FAST_MAPS,
    "map_device_option": 'Essence'
  },

  "low_tier_beast_fast": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "beast_search_string": "cic c",
    "release_beasts": True,
    "map_priorities": FAST_WHITE_MAPS,
    "prefered_map_device_modifiers": ["Bestiary Scarab of the Herd", "Bestiary Scarab of the Herd", "Bestiary Scarab of Duplicating"],
  },

  
  "low_tier_beast_deli": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "beast_search_string": "cic c",
    "release_beasts": True,
    "force_deli": True,
    "wait_for_deli_drops": True,
    "map_priorities": FAST_WHITE_MAPS,
    "prefered_map_device_modifiers": ["Bestiary Scarab of the Herd", "Bestiary Scarab of the Herd", "Bestiary Scarab of Duplicating"],
  },
  "low_tier_beast_deli_essence": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "beast_search_string": "cic c",
    "release_beasts": True,
    "keep_consumables": ['Remnant of Corruption'],
    "force_deli": True,
    "wait_for_deli_drops": True,
    "do_essences": True,
    "map_priorities": FAST_WHITE_MAPS,
    "prefered_map_device_modifiers": BESTIARY_SCARABS,
    "map_device_option": 'Essence'
  },
  "low_tier_beast_deli_essence_no_fenumals": {
    "force_kill_boss": False, 
    "prefer_high_tier": False,
    "beast_farmer": True,
    "collect_beasts_every_x_maps": 80,
    "release_beasts": True,
    "keep_consumables": ['Remnant of Corruption'],
    "force_deli": True,
    "wait_for_deli_drops": True,
    "do_essences": True,
    "beast_search_string": "cic c",
    "map_priorities": FAST_MAPS,
    "prefered_map_device_modifiers": ["Bestiary Scarab"],
    "map_device_option": 'Essence'
  },

  "t16_deli_legion_harbringers": {
    "force_kill_boss": False, 
    "prefered_map_device_modifiers": ["Legion Scarab", "Harbringer Scarab"],
    # "map_device_modifiers": ["Bestiary Scarab"],
    "map_priorities": ["Dunes Map", "Fields Map", "Colonnade Map"],
    "do_essences": False,
    "force_deli": True,
    "do_legion": True,
    "do_harbringers": True,
    "do_blight": False,
    "wait_for_deli_drops": True,
  },
  "t16_deli_harbringers_altar": {
    "boss_rush": True,
    "invitation_rush": True,
    "alch_chisel": True,
    "prefer_high_tier": True,
    "prefered_map_device_modifiers": ["Abyss Scarab", "Harbringer Scarab"],
    "map_priorities": FAST_MAPS,
    "force_deli": True,
    "wait_for_deli_drops": True,
    "do_harbringers": True,
    "do_abysses": True,
  },

  "deli_harbringer_lowtier": {
    "force_kill_boss": False, 
    "map_priorities": ["Beach Map", "Strand Map","Dunes Map","Cemetery Map","Plateau Map"],
    "force_deli": True,
    "do_harbringers": True,
    "force_kill_blue": True,
    "force_kill_rares": True,
    "wait_for_deli_drops": True,
  },

  "invintation_high_tier_wildwood_jewels": {
    "alch_chisel": True,
    "invitation_rush": True,
    "wildwood_jewel_farm": True,
    "prefer_high_tier": True,
    "force_kill_boss": False, 
    "force_kill_blue": True,
    "force_kill_rares": False,
  },

  "high_tier_harvest_growing_hordes_no_deli": {
    "prefer_high_tier": True,
    "do_harvest": True,
    "alch_chisel": True,
    "force_kill_boss": False, 
    "force_kill_blue": True,
    "force_kill_rares": False,
    "growing_hordes": True,
    "map_priorities": FAST_MAPS,
  },
  "high_tier_harvest_wandering_path_growing_hordes": {
    "prefer_high_tier": True,
    "force_kill_boss": False, 
    "do_harvest": True,
    "do_harbringers": True,
    "force_kill_blue": True,
    "force_kill_rares": False,
    "force_deli": True,
    "wait_for_deli_drops": True,
    "map_priorities": ["Crimson Temple Map", "Grotto Map", "Dunes Map" ,"Cemetery Map", "Arcade Map", "Strand Map"],
    "growing_hordes": True
  },

}