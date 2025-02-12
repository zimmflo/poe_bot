from .constants import BOSS_RENDER_NAMES

# multi phased and unusual bosses, description of their kill process
# https://github.com/vlaskinarita/Papashagodx-Seusheque-ExPlugins-source/blob/master/ExPlugins.MapBotEx.Tasks/KillBossTask.cs

# description of maps
# https://github.com/vlaskinarita/Papashagodx-Seusheque-ExPlugins-source/blob/master/ExPlugins.MapBotEx/MapSettings.cs

# map boss render names
# https://github.com/shaliuno/Papashagodx-Seusheque-ExPlugins-source/blob/master/ExPlugins.MapBotEx.Helpers/MapData.cs

# unusual map walkthrough, vault is not supported
# https://github.com/vlaskinarita/Papashagodx-Seusheque-ExPlugins-source/blob/master/ExPlugins.MapBotEx.Tasks/MapExplorationTask.cs
# https://github.com/vlaskinarita/Papashagodx-Seusheque-ExPlugins-source/blob/master/ExPlugins.MapBotEx.Tasks/SpecialObjectTask.cs


# https://github.com/vlaskinarita/Papashagodx-Seusheque-ExPlugins-source/blob/master/ExPlugins.MapBotEx.Tasks/TransitionTriggerTask.cs


class MapArea:
  arena_render_name = "Arena"
  ignore_bossroom = False
  boss_render_names = BOSS_RENDER_NAMES
  entities_to_ignore_in_bossroom_path_keys = []
  transitions_to_ignore_render_names = []
  need_to_leave_bossroom_through_transition = True
  possible_transition_on_a_way_to_boss = False
  bossroom_activator = None
  activator_inside_bossroom = None
  activators_on_map = None
  kill_entities_to_spawn_boss = False
  refresh_terrain_data_in_bossroom = False


class Carcass(MapArea):
  arena_render_name = "The Black Heart"
  boss_render_names = ["Amalgam of Nightmares"]


class Cage(MapArea):
  arena_render_name = "Ladder"
  boss_render_names = ["Executioner Bloodwing"]


class Dungeon(MapArea):
  arena_render_name = "Opening"
  boss_render_names = ["Penitentiary Incarcerator"]


class JungleValley(MapArea):
  arena_render_name = "The Loom Chamber"
  boss_render_names = ["Queen of the Great Tangle"]


class ArachnidNest(MapArea):
  arena_render_name = "The Loom Chamber"
  boss_render_names = ["Spinner of False Hope"]


class Barrows(MapArea):
  transitions_to_ignore_render_names = ["Tomb"]
  boss_render_names = ["Beast of the Pits"]


class AcidCaverns(MapArea):
  boss_render_names = [
    "Rama, The Kinslayer",
    "Kalria, The Fallen",
    "Kalria, The Risen",
    "Invari, The Bloodshaper",
    "Lokan, The Deceiver",
    "Marchak, The Betrayer",
    "Berrots, The Breaker",
    "Vessider, The Unrivaled",
    "Morgrants, The Deafening",
  ]


class ColdRiver(MapArea):
  boss_render_names = ["Ara, Sister of Light", "Khor, Sister of Shadows"]
  need_to_leave_bossroom_through_transition = False
  possible_transition_on_a_way_to_boss = True


class Malformation(MapArea):
  need_to_leave_bossroom_through_transition = False
  possible_transition_on_a_way_to_boss = True


class Factory(MapArea):
  boss_render_names = ["Pesquin, the Mad Baron"]
  transitions_to_ignore_render_names = ["Voltaic Workshop"]
  need_to_leave_bossroom_through_transition = False
  possible_transition_on_a_way_to_boss = True


class Sepulchre(MapArea):
  need_to_leave_bossroom_through_transition = False


class OvergrownShrine(MapArea):
  boss_render_names = ["Maligaro the Mutilator"]
  need_to_leave_bossroom_through_transition = False
  possible_transition_on_a_way_to_boss = True


class InfestedValley(MapArea):
  boss_render_names = ["Gorulis' Nest", "Gorulis, Will-Thief"]


class Basilica(MapArea):
  boss_render_names = ["Konley, the Unrepentant", "The Cleansing Light"]


class Palace(MapArea):
  boss_render_names = ["God's Chosen", "The Hallowed Husk"]


class Arcade(MapArea):
  boss_render_names = ["Herald of Ashes", "Herald of Thunder"]


class Tower(MapArea):
  boss_render_names = ["Bazur", "Liantra"]


class Academy(MapArea):
  bossroom_activator = "Metadata/QuestObjects/Library/HiddenDoorTrigger"


class Museum(MapArea):
  bossroom_activator = "Metadata/QuestObjects/Library/HiddenDoorTrigger"


class GraveTrough(MapArea):
  ignore_bossroom = True
  bossroom_activator = "Metadata/Terrain/EndGame/MapBurn/Objects/BossEventSarcophagus"


class FrozenCabins(MapArea):
  activators_on_map = "Metadata/Terrain/Labyrinth/Objects/Puzzle_Parts/Switch_Once"


class PrimordialBlocks(MapArea):
  boss_render_names = ["High Lithomancer"]


class SunkenCity(MapArea):
  refresh_terrain_data_in_bossroom = True
  boss_render_names = ["Armala, the Widow"]


class MapWorldsNecropolis(MapArea):
  bossroom_activator = "Metadata/Chests/Sarcophagi/sarcophagus_door"
  arena_render_name = "Stairs"


class MapWorldsShipyard(MapArea):
  boss_render_names = [
    'Musky "Two-Eyes" Grenn',
    "Susara, Siren of Pondium",
    'Lussi "Rotmother" Roth',
  ]


class MapWorldsWastePool(MapArea):
  activator_inside_bossroom = "Metadata/Terrain/EndGame/MapGraveyard/Objects/GraveyardAltar"


class MapWorldsDesert(MapArea):
  activators_on_map = "Metadata/Terrain/EndGame/MapDesert/Objects/MummyEventChest"


class MapWorldsGraveyard(MapArea):
  ignore_bossroom = True
  activator_inside_bossroom = "Metadata/Terrain/EndGame/MapGraveyard/Objects/GraveyardAltar"


# MAPS WITH PROBLEMS ATM
class MapWorldsSummit(MapArea):
  ignore_bossroom = True


class MapWorldsIvoryTemple(MapArea):
  ignore_bossroom = True


class MapWorldsBelfry(MapArea):
  ignore_bossroom = True


class MapWorldsThicket(MapArea):
  boss_render_names = ["The Primal One"]


class MapWorldsFields(MapArea):
  entities_to_ignore_in_bossroom_path_keys = [
    "Metadata/Monsters/Bandits/BoarBanditSpectator",
    "Metadata/Monsters/Ralakesh/Greust/GreustArcher",
    "Metadata/Monsters/Bandits/BoarBanditSpectator",
  ]


class MapWorldsLavaLake(MapArea):
  boss_render_names = [
    "Kitava, The Destroyer",
  ]
  ignore_bossroom = True


# class MapWorldsThicket(MapArea):
#   boss_render_names = ["Stone of the Currents"]


class MapWorldsDesertSpring(MapArea):
  arena_render_name = "The Sand Pit"
  ignore_bossroom = True


class Pier(MapArea):
  arena_render_name = "Gauntlet"
  ignore_bossroom = True


class MapWorldsSiege(MapArea):
  ignore_bossroom = True


class Lookout(MapArea):
  ignore_bossroom = True
  kill_entities_to_spawn_boss = True


maps = {
  "MapWorldsCarcass": Carcass,
  "MapWorldsCage": Cage,
  "MapWorldsDungeon": Dungeon,
  "MapWorldsJungleValley": JungleValley,
  "MapWorldsArachnidNest": ArachnidNest,
  "MapWorldsBarrows": Barrows,
  "MapWorldsAcidLakes": AcidCaverns,
  "MapWorldsColdRiver_": ColdRiver,
  "MapWorldsFactory": Factory,
  "MapWorldsOvergrownShrine": OvergrownShrine,
  "MapWorldsInfestedValley": InfestedValley,
  "MapWorldsBasilica": Basilica,
  "MapWorldsTower": Tower,
  "MapWorldsAcademy": Academy,
  "MapWorldsFrozenCabins": FrozenCabins,
  "MapWorldsMalformation": Malformation,
  "MapWorldsPalace": Palace,
  "MapWorldsPier": Pier,
  "MapWorldsGraveTrough": GraveTrough,
  "MapWorldsTortureChamber": PrimordialBlocks,
  "MapWorldsGraveyard": MapWorldsGraveyard,
  "MapWorldsLookout": Lookout,
  "MapWorldsArcade": Arcade,
  "MapWorldsSunkenCity": SunkenCity,
  "MapWorldsMuseum": Museum,
  "MapWorldsSepulchre": Sepulchre,
  "MapWorldsNecropolis": MapWorldsNecropolis,
  "MapWorldsSummit": MapWorldsSummit,
  "MapWorldsIvoryTemple": MapWorldsIvoryTemple,
  "MapWorldsThicket": MapWorldsThicket,
  "MapWorldsDesert": MapWorldsDesert,
  "MapWorldsSiege": MapWorldsSiege,  # broken arena
  "MapWorldsShipyard": MapWorldsShipyard,
  "MapWorldsDesertSpring": MapWorldsDesertSpring,  # broken arena
  "MapWorldsBelfry": MapWorldsBelfry,  # broken arena
  "MapWorldsFields": MapWorldsFields,  # broken arena
  "MapWorldsLavaLake": MapWorldsLavaLake,
}


def getMapAreaObject(map_raw_name) -> MapArea:
  if map_raw_name in list(maps.keys()):
    map_object = maps[map_raw_name]
  else:
    map_object = MapArea
  return map_object


MAPS_TO_IGNORE = [
  "Forge of the Phoenix Map",
  "Lair of the Hydra Map",
  "Maze of the Minotaur Map",
  "Pit of the Chimera Map",
  "Core Map",
  "Caldera Map",  # 3 waypoints, activate 2, and go for 3
  "Arena Map",  # multiple transitions with render name Arena
  "Colosseum Map",
  "Pit Map",
  "Laboratory Map",  # 4 activators,
  "Vault Map",  # activators for doors
  "Frozen Cabins Map",  # activators for doors
  # mostlikeley wont run at all
  "Forking River Map",  # pathing problem
]

IGNORE_BOSSROOM_MAPS = [
  # bossfight activator
  "Belfry Map",  # bossfight activator
  "Waste Pool Map",  # bossfight activator, bossroom activator?
  "Desert Spring Map",  # bossfight activator, bossroom activator?
  "Ivory Temple Map"  # bossfight activator
  "Lookout Map",  # Boss has some time before appearing,
  "Summit Map",  # nested bossroom
  "Pier Map",  # nested bossroom
  "Lava Lake Map",  # boss is oob
  "Siege Map",  # totem boss
  "Graveyard Map",  # totem boss
]

FAST_BOSS_MAPS = [
  "Park Map",
  "City Square Map",
  "Ashen Woods Map",
  "Dunes Map",
  "Coves Map",
  "Arcade Map",
  "Canyon Map",
  "Strand Map",
  "Grotto Map",
]


class MapperSettings:
  default_discovery_percent = 0.93  # % for which itll explore the area

  session_duration = "24h"
  atlas_explorer = False  # prefer to run higher tier maps over lower tier

  keep_consumables = []

  alch_chisel = False  # will use alch + chisel if it's possible
  alch_chisel_force = False  # TODO will use alch or scour alch chisel if possible
  growing_hordes = False  # can place whatever different scarabs in atlas map device

  prefered_tier = None
  keep_maps_in_inventory = 10

  prefered_map_device_modifiers = []  # prefered items to place in addition to map in map device, will place them if have them in inventory or pick them from stash if possible
  musthave_map_device_modifiers = []  # items to place in addition to map in map device, will throw an error if wont have them in inventory before running map

  do_essences = False
  essences_do_memory = False
  essences_do_all = False
  essences_can_corrupt = False
  essences_min_to_corrupt = 6

  party_ultimatum = False

  do_harbringers = False

  do_harvest = False
  harvest_crop_rotation = False
  harvest_rush = False

  force_kill_rogue_exiles = False

  invitation_rush = False
  invitation_type = "blue"  # 'red' 'blue'
  wildwood_jewel_farm = False

  reroll_scarabs = []

  clear_around_shrines = False

  do_alva = False
  alva_clear_room = False
  alva_ignore_temple_mechanics = False
  alva_skip_map_if_finished_incursion = False
  alva_skip_map_if_finished_incursion_and_have_priority_map_in_inventory = False
  alva_also_keep_temples_with = [
    "Locus of Corruption (Tier 3)",
    "Doryani's Institute (Tier 3)",
  ]
  incursion_valuable_rooms = [
    "Locus of Corruption",
    "Catalyst of Corruption",
    "Corruption Chamber",
    "Gemcutter's Workshop",
    "Department of Thaumaturgy",
    "Doryani's Institute",
  ]
  use_timeless_scarab_if_connected_or_presented = []
  alva_clear_room_if_need_to_connect = True

  low_priority_maps = []

  do_beasts = False
  release_beasts = True  # will also release beasts if beast farmer is True
  beasts_kill_keywords = [
    "Black Mórrigan",
    "Vivid Watcher",
    "Vivid Vulture",
    "Craicic Chimeral",
    "Wild Hellion Alpha",
    "Wild Bristle Matron",
  ]
  collect_beasts_every_x_maps: int = 30
  beast_search_string = "cic c|id w|id v|le m|ld h|Black M"

  max_map_run_time = 600
  discovery_percent = default_discovery_percent  # % for which itll explore the area

  force_kill_mobs = True  # TODO blue + rare mobs
  force_kill_blue = False
  force_kill_rares = False

  def __init__(self, config: dict) -> None:
    for key, value in config.items():
      setattr(self, key, value)

    if self.essences_can_corrupt is True:
      print("essences_can_corrupt is True, gonna keep remnant of corruption")
      self.keep_consumables.append("Remnant of Corruption")

    self.keep_consumables.append("Portal Scroll")
    self.low_priority_maps.extend(
      [
        "Overgrown Shrine Map",
        "Frozen Cabins Map",
        "Reef Map",
        "Lava Lake Map",
        "Cage Map",
        "Cells Map",
        "Crimson Township Map",
      ]
    )
    if self.use_timeless_scarab_if_connected_or_presented:
      self.keep_consumables.append("Incursion Scarab of Timelines")
      self.keep_consumables.append("Incursion Scarab of Timelines")
    if self.atlas_explorer is True:
      self.keep_consumables.extend(
        [
          "Orb of Alchemy",
          "Orb of Scouring",
          "Scroll of Wisdom",
          "Vaal Orb",
          "Orb of Binding",
          "Orb of Transmutation",
        ]
      )
    print(str(self))

  def __str__(self):
    return f"mapper_settings: {str(vars(self))}"
