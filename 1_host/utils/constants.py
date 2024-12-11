""" constants """
# shitty uniques
unidentified_keywords = [
  'Unidentified'
]
# if item matches any of this, itll remove it
shitty_uniques_keywords = [
  # ["", ""],
  ["Carnage Heart", "Onyx Amulet"],
  ["Sidhebreath", "Paua Amulet"],
  ["Warped Timepiece", "Turquoise Amulet"],
  ["Sibyl's Lament", "Coral Ring"],
  ["The Anvil", "Amber Amulet"],
  ["The Consuming Dark", "Fiend Dagger"],
  ["Taproot", "Ambusher"],
  ["Vis Mortis", "Necromancer Silks"],
  ["Soul Mantle", "Spidersilk Robe"],
  ["Wreath of Phrecia", "Iron Circlet"],
  ["Blunderbore", "Astral Plate"],
  ["Skirmish", "Two-Point Arrow Quiver"],
  ["Axiom Perpetuum", "Bronze Sceptre"],
  ["Voices", "Large Cluster Jewel", "Adds 7 Small Passive Skills which grant nothing"],
  ["Voices", "Large Cluster Jewel", "Adds 5 Small Passive Skills which grant nothing"],
  ["Split Personality", "+40 to Evasion Rating"],
  ["Split Personality", "+5 to maximum Mana"],
  ["Split Personality", "+40 to Accuracy Rating"],
  ["Split Personality", "+40 to Armour"],
  ["Wurm's Molt", "Leather Belt"],
  ["Belt of the Deceiver", "Heavy Belt"],
  ["Leather Belt", "Immortal Flesh"],
  ["Gluttony", "Leather Belt"],
  ["Death's Oath", "Astral Plate"],
  ["Perfidy", "Glorious Plate"],
  ["Chin Sol", "Assassin Bow"],
  ["Snakebite", "Assassin's Mitts"],
  ["The Ivory Tower", "The Ivory Tower"],
  ["Lioneye's Vision", "Crusader Plate"],
  ["Siegebreaker", "Heavy Belt"],
  ["Umbilicus Immortalis", "Leather Belt"],
  ["Victario's Acuity", "Turquoise Amulet"],
]




shitty_uniques_metadatas = [
  # qarmours
  'Metadata/Items/Armours/BodyArmours/BodyStr14',
  'Metadata/Items/Armours/BodyArmours/BodyDexInt16', 

  'Metadata/Items/Armours/BodyArmours/BodyInt8',
  'Metadata/Items/Armours/BodyArmours/BodyInt11',
  'Metadata/Items/Armours/BodyArmours/BodyInt15', # shav wrappings
  # weapons
  'Metadata/Items/Weapons/OneHandWeapons/OneHandMaces/OneHandMace18',
  'Metadata/Items/Weapons/TwoHandWeapons/Bows/Bow19', # chin sol
  'Metadata/Items/Weapons/OneHandWeapons/OneHandMaces/Sceptre3', #Axiom Perpetuum
  'Metadata/Items/Weapons/OneHandWeapons/Daggers/Dagger18', # Taproot
  'Metadata/Items/Weapons/OneHandWeapons/OneHandThrustingSwords/Rapier21', # Cospri's Malice

  'Metadata/Items/Rings/Ring2',

  'Metadata/Items/Amulets/Amulet3', # The Anvil
  'Metadata/Items/Amulets/Amulet8',

  'Metadata/Items/Belts/Belt3',
  'Metadata/Items/Belts/Belt4',
  'Metadata/Items/Armours/Gloves/GlovesStr9',
  'Metadata/Items/Armours/BodyArmours/BodyInt14',
  'Metadata/Items/Armours/BodyArmours/BodyInt8',
  'Metadata/Items/Weapons/OneHandWeapons/Claws/Claw20',
  'Metadata/Items/Rings/Ring4',
  'Metadata/Items/Rings/Ring15',
  'Metadata/Items/Armours/Boots/BootsDex8',
  'Metadata/Items/Armours/Boots/BootsDex8',

  'Metadata/Items/Rings/Ring15','Metadata/Items/Armours/Boots/BootsDex8','Metadata/Items/Weapons/OneHandWeapons/Daggers/Dagger15',
  'Metadata/Items/Weapons/OneHandWeapons/Wands/Wand3','Metadata/Items/Weapons/OneHandWeapons/Daggers/Dagger21','Metadata/Items/Flasks/FlaskUtility12'
  ,'Metadata/Items/Weapons/OneHandWeapons/Daggers/Dagger15',
  'Metadata/Items/Amulets/Amulet7','Metadata/Items/Amulets/Amulet7','Metadata/Items/Rings/Ring4','Metadata/Items/Rings/Ring9','Metadata/Items/Rings/Ring9','Metadata/Items/Rings/Ring9',
  'Metadata/Items/Armours/Shields/ShieldStr14','Metadata/Items/Amulet/AmuletAtlas1','Metadata/Items/Armours/BodyArmours/BodyDexInt11','Metadata/Items/Armours/Helmets/HelmetInt2','Metadata/Items/Armours/Shields/ShieldStrInt10','Metadata/Items/Armours/Gloves/GlovesStrDex6','Metadata/Items/Armours/BodyArmours/BodyStr17','Metadata/Items/Weapons/OneHandWeapons/Wands/Wand6','Metadata/Items/Weapons/OneHandWeapons/Wands/Wand6','Metadata/Items/Weapons/TwoHandWeapons/Staves/Staff12'
  'Metadata/Items/Armours/BodyArmours/BodyStrInt16','Metadata/Items/Armours/Gloves/GlovesDexInt8','Metadata/Items/Rings/Ring6','Metadata/Items/Rings/Ring6',
]

# TO GET LIST OF ITEMS IN INVENTORY AND PARSE THEIR RENDER ART
# items_in_inventory = []
# for item in poe_bot.getOpenedInventoryInfo()['items']:
#   items_in_inventory.append(item['RenderArt'])

# new_str = ''
# for item in items_in_inventory:
#   new_str += "'"
#   new_str += item
#   new_str += "',"
# print(new_str)

KEYWORDSTOSEARCH = ["Rusted", "Polished", "Screaming", "Shrieking", "Catalyst", "Oil"]
IGNOREKEYWORDSTOSEARCH = ["Golden", "Prismatic", "Unstable"]


# zone where we will drop the loot from inventory to the ground
DROP_ITEMS_ZONE = [488, 545, 413, 615] # x1, x2, y1, y2

INVENTORY_SLOT_CELL_SIZE = 38 # only for 1024x768

# 1024x768
CURRENCY_TAB_ITEMS_POSITIONS = {
  'divine' : {'X': 433, 'Y': 233},
  'fusing' : {'X': 122, 'Y': 283},
  'jewellers' : {'X': 81, 'Y': 281},
  'chaos' : {'X': 391, 'Y': 191},
  'vaal' : {'X': 431, 'Y': 361},
  'additional_slot_0_0' : {'X': 115, 'Y': 430},
  'additional_slot_0_1' : {'X': 155, 'Y': 430},
  'additional_slot_0_2' : {'X': 195, 'Y': 430},
  'additional_slot_0_3' : {'X': 235, 'Y': 430},
  'additional_slot_0_4' : {'X': 275, 'Y': 430},
  'additional_slot_0_5' : {'X': 315, 'Y': 430},
  'additional_slot_0_6' : {'X': 355, 'Y': 430},
  'additional_slot_1_0' : {'X': 115, 'Y': 475},
  'additional_slot_1_1' : {'X': 155, 'Y': 475},
  'additional_slot_1_2' : {'X': 195, 'Y': 475},
  'additional_slot_1_3' : {'X': 235, 'Y': 475},
  'additional_slot_1_4' : {'X': 275, 'Y': 475},
  'additional_slot_1_5' : {'X': 315, 'Y': 475},
  'additional_slot_1_6' : {'X': 355, 'Y': 475},
}


MAP_DEVICE_SLOTS ={ # [ [x,y], [x,y]]
  "5slot":[ [228, 456], [318, 456], [228, 556], [318, 556], [275, 500] ], 
  "4slot":[ [255,455], [255,495], [295,455], [295,495] ],
  
  # 0 2
  # 1 3


}

MAP_DEVICE_ACTIVATE_BUTTON = {
  "5slot":(272,633),
  "4slot":(280,590),
}

FRIENDLY_ENTITIES_PATH_KEYWORDS = [
  "/NPCAllies/", # heist npc helpers
  'Metadata/Monsters/RockGolem/RockGolemSummoned', # stone golem
  'Metadata/Monsters/Mirage/RangerMirage', # mirage archer
  'Metadata/Monsters/Totems/ShotgunTotem', # ballista totem,
  'Metadata/Monsters/BoneGolem/BoneGolem@72', # carrion golem
  'Metadata/Monsters/SummonedSkull/SummonedSkull@72', # srs minion
  'Metadata/Monsters/Masters/Einhar'
]

DELIRIUM_TRASH_ON_MAPS = [
  "Metadata/Monsters/LeagueAffliction/DoodadDaemons/DoodadDaemonEyes", # some delirium mob on map
  "Metadata/Monsters/LeagueAffliction/DoodadDaemons/DoodadDaemonPimple",
  "Metadata/Monsters/LeagueAffliction/DoodadDaemons/DoodadDaemonSpikes", # some delirium mob on map
]

UNKNOWN_ENTITIES = [
  "Metadata/Monsters/LeagueAffliction/DoodadDaemons/DoodadDaemonEyes", # some delirium mob on map
  "Metadata/Monsters/LeagueAffliction/DoodadDaemons/DoodadDaemonPimple",
  "Metadata/Monsters/LeagueAffliction/DoodadDaemons/DoodadDaemonSpikes", # some delirium mob on map
]

SKILL_KEYS = [
  'left',
  'middle',
  'right',
  'DIK_Q',
  'DIK_W',
  'DIK_E',
  'DIK_R',
  'DIK_T',
  'CTRL+DIK_Q',
  'CTRL+DIK_W',
  'CTRL+DIK_E',
  'CTRL+DIK_R',
  'CTRL+DIK_T',
]

FLASK_NAME_TO_BUFF = {
  # https://github.com/TehCheat/PoEHelper/blob/master/Plugins/Compiled/BasicFlaskRoutine/config/languages/Russian/FlaskBuffDetails.json
  "Small Life Flask": "flask_effect_life",
  "Medium Life Flask": "flask_effect_life",
  "Large Life Flask": "flask_effect_life",
  "Greater Life Flask": "flask_effect_life",
  "Grand Life Flask": "flask_effect_life",
  "Giant Life Flask": "flask_effect_life",
  "Colossal Life Flask": "flask_effect_life",
  "Sacred Life Flask": "flask_effect_life",
  "Hallowed Life Flask": "flask_effect_life",
  "Sanctified Life Flask": "flask_effect_life",
  "Divine Life Flask": "flask_effect_life",
  "Eternal Life Flask": "flask_effect_life",
  "Small Mana Flask": "flask_effect_mana",
  "Medium Mana Flask": "flask_effect_mana",
  "Large Mana Flask": "flask_effect_mana",
  "Greater Mana Flask": "flask_effect_mana",
  "Grand Mana Flask": "flask_effect_mana",
  "Giant Mana Flask": "flask_effect_mana",
  "Colossal Mana Flask": "flask_effect_mana",
  "Sacred Mana Flask": "flask_effect_mana",
  "Hallowed Mana Flask": "flask_effect_mana",
  "Sanctified Mana Flask": "flask_effect_mana",
  "Divine Mana Flask": "flask_effect_mana",
  "Eternal Mana Flask": "flask_effect_mana",
  "Small Hybrid Flask": "flask_effect_life",
  "Medium Hybrid Flask": "flask_effect_life",
  "Large Hybrid Flask": "flask_effect_life",
  "Colossal Hybrid Flask": "flask_effect_life",
  "Sacred Hybrid Flask": "flask_effect_life",
  "Hallowed Hybrid Flask": "flask_effect_life",
  "Diamond Flask": "flask_utility_critical_strike_chance",
  "Ruby Flask": "flask_utility_resist_fire",
  "Sapphire Flask": "flask_utility_resist_cold",
  "Topaz Flask": "flask_utility_resist_lightning",
  "Granite Flask": "flask_utility_ironskin",
  "Quicksilver Flask": "flask_utility_sprint",
  "Amethyst Flask": "flask_utility_resist_chaos",
  "Quartz Flask": "flask_utility_phase",
  "Jade Flask": "flask_utility_evasion",
  "Basalt Flask": "flask_utility_stone",
  "Aquamarine Flask": "flask_utility_aquamarine",
  "Stibnite Flask": "flask_utility_smoke",
  "Sulphur Flask": "flask_utility_consecrate",
  "Silver Flask": "flask_utility_haste",
  "Bismuth Flask": "flask_utility_prismatic",
}

SHITTY_UNIQUES_ARTS = set([
  "Art/2DItems/Belts/PyroshockClasp.dds",
  "Art/2DItems/Belts/Gluttony.dds",
  "Art/2DItems/Belts/BeltOfTheDeciever.dds",
  "Art/2DItems/Belts/ImmortalFlesh.dds",
  "Art/2DItems/Belts/BiscosLeash.dds",
  "Art/2DItems/Belts/PyroshockClasp.dds",
  "Art/2DItems/Belts/UmbilicusImmortalis.dds"
  "Art/2DItems/Belts/Belt6Unique.dds", # "Wurm's Molt"
  "Art/2DItems/Belts/85482.dds", # Siegebreaker
  "Art/2DItems/Belts/Belt7Unique.dds", # "Meginord's Girdle"
  "Art/2DItems/Belts/KaomBelt.dds",
  "Art/2DItems/Belts/MotherDyadus.dds",
  "Art/2DItems/Belts/MothersEmbrace.dds",
  "Art/2DItems/Belts/LeashOfOblation.dds",
  "Art/2DItems/Belts/PyroshockClasp.dds",
])

HARVEST_SEED_COLOR_WEIGHTS = {
  'Vivid': 1/4000, # yellow 3000/1d
  'Wild': 1/6500, # purple 6500/1d
  "Primal": 1/5900 # blue 5900/1d
}

DANGER_ZONE_KEYS = [
  "LightningClone",
  "Metadata/Monsters/LeagueArchnemesis/LivingCrystal", # friendly? enemy?
  "Metadata/Monsters/VolatileCore/VolatileCoreArchnemesis", # 
  "/LeagueArchnemesis/ToxicVolatile",
]

BOSS_RENDER_NAMES = ["Drought-Maddened Rhoa","Khor, Sister of Shadows","Enticer of Rot","Merveil, the Reflection","Merveil, the Returned","Headmistress Braeta","The Goddess","Captain Clayborne, The Accursed","Skullbeak","Titan of the Grove","Penitentiary Incarcerator","Rama, The Kinslayer","Kalria, The Fallen","Invari, The Bloodshaper","Lokan, The Deceiver","Marchak, The Betrayer","Berrots, The Breaker","Vessider, The Unrivaled","Morgrants, The Deafening","He of Many Pieces","Liantra","Bazur","Helial, the Day Unending","Selenia, the Endless Night","Forest of Flames","Gorulis, Will-Thief","The Reaver","Nassar, Lion of the Seas","Burtok, Conjurer of Bones","Amalgam of Nightmares","Konley, the Unrepentant","Sebbert, Crescent's Point","Maker of Mires","Rose","Thorn","Mistress Hyseria","The Steel Soul","Lord of the Ashen Arrow","Ancient Sculptor","Erebix, Light's Bane","Warmonger","Jorus, Sky's Edge","Maligaro the Mutilator","The Sanguine Siren","Fairgraves, Never Dying","The Apex Assembly","Gazuul, Droughtspawn","Herald of Ashes","Herald of Thunder","Tunneltrap","Blood Progenitor","Belcer, the Pirate Lord","Shadow of the Vaal","Avatar of the Huntress","Avatar of the Skies","Avatar of the Forge","Arachnoxia","Nightmare's Omen","Melur Thornmaul","Elida Blisterclaw","Orvi Acidbeak","Kadaris, Crimson Mayor","Vision of Justice","Lycius, Midnight's Howl","Puruna, the Challenger","Mephod, the Earth Scorcher","Olmec, the All Stone","Avatar of Thunder","The Grey Plague","Carius, the Unnatural","Pileah, Corpse Burner","Pileah, Burning Corpse","Oriath's Virtue","Oriath's Vengeance","Oriath's Vigil","Sanctum Enforcer","Sanctum Guardian","Xixic, High Necromancer","Doedre the Defiler","Sallazzang","Preethi, Eye-Pecker","Oak the Mighty","Terror of the Infinite Drifts","Tyrant","Varhesh, Shimmering Aberration","Eater of Souls","Rek'tar, the Breaker","Blackguard Avenger","Blackguard Tempest","Visceris","Fire and Fury","Void Anomaly","Lord of the Hollows","Messenger of the Hollows","Champion of the Hollows","Talin, Faithbreaker","Tore, Towering Ancient","The Blacksmith","Gnar, Eater of Carrion","Stonebeak, Battle Fowl","Queen of the Great Tangle","Tolman, the Exhumer","Portentia, the Foul","The Restless Shade","Orra Greengate","Torr Olgosso","Damoi Tui","Wilorin Demontamer","Augustina Solaria","Igna Phoenix","The Cursed King","Stone of the Currents","Executioner Bloodwing","The High Templar","Winterfang","Storm Eye","Solus, Pack Alpha","Olof, Son of the Headsman","Shock and Horror","Unravelling Horror","It That Fell","The Broken Prince","The Fallen Queen","The Hollow Lady","The Shifting Ire","Ciergan, Shadow Alchemist","The Brittle Emperor","Captain Tanner Lightfoot","Pesquin, the Mad Baron","Riftwalker","Tormented Temptress","Glace","Calderus","Drek, Apex Hunter","Master of the Blade","Massier","Aulen Greychain","Infector of Dreams","Suncaller Asha","Beast of the Pits","Pagan Bishop of Agony","Shavronne the Sickening","God's Chosen","Guardian of the Chimera","The Infernal King","Kitava, The Destroyer","Guardian of the Hydra","Guardian of the Minotaur","K'aj Q'ura","K'aj Y'ara'az","K'aj A'alai","Witch of the Cauldron","Guardian of the Phoenix","Excellis Aurafix","Absence of Patience and Wisdom","The Searing Exarch","Absence of Symmetry and Harmony","The Eater of Worlds","Polaric Void","The Black Star","Seething Chyme","The Infinite Hunger","Thunderskull","Champion of Frost","Steelpoint the Avenger","Arwyn, the Houndmaster","The Eroding One","Yorishi, Aurora-sage","Jeinei Yuushu","Otesha, the Giantslayer","Shrieker Eihal","Breaker Toruul","Mirage of Bones","Litanius, the Black Prayer","Bolt Brownfur, Earth Churner","Thena Moga, the Crimson Storm","Ion Darkshroud, the Hungering Blade","Hephaeus, The Hammer","Uruk Baleh","El'Abin, Bloodeater","Leli Goya, Daughter of Ash","Bin'aia, Crimson Rain","The Forgotten Soldier","The Gorgon","Barthol, the Pure","Barthol, the Corruptor","The Winged Death","Legius Garhall","Thraxia","Erythrophagia","The Arbiter of Knowledge","Megaera","Spinner of False Hope","Avatar of Undoing","Poporo, the Highest Spire","Sumter the Twisted","Guardian of the Vault","Gisale, Thought Thief","Tahsin, Warmaker","Musky "," Grenn","Susara, Siren of Pondium","Lussi "," Roth","Lord of the Grey","Hybrid Widow","Ancient Architect","Telvar, the Inebriated","Pirate Treasure","Fragment of Winter","Woad, Mockery of Man","Leif, the Swift-Handed","Shredder of Gladiators","Crusher of Gladiators","Bringer of Blood","Lady Stormflay","Nightmare Manifest","Piety the Empyrean","Ambrius, Legion Slayer","Stalker of the Endless Dunes","Ormud, Fiend of the Flood","Renkarr, The Kiln Keeper","Murgeth Bogsong","Skictis, Frostkeeper","Takatax Brittlethorn","Corruptor Eedaiak"]

# "The Hallowed Husk" - Palace Map



ATLAS_COMPLETED_MAPS_LONG = [
  "Haunted Mansion",
]

UNSORTED_FROM_SIMULACRUM = [
  "Metadata/Monsters/VolatileCore/VolatileCoreArchnemesis",
  "Metadata/Monsters/DropBear/DropBear2SpawnParasite",
  "Goatman/GoatmanLightningLeapSlamMaps",
  "Metadata/Monsters/InvisibleCurse/Invisible",
  "Metadata/Monsters/LeagueAffliction/AfflictionSkillDaemonMonsterFrostOrbs",
  "Metadata/Monsters/LeagueAffliction/AfflictionSkillDaemonMonsterSlamma_",
  "Metadata/Monsters/Daemon/DoNothingDaemon",
  "Metadata/Monsters/LeagueArchnemesis/ToxicVolatile_",
  "Metadata/Monsters/Daemon/AfflictionAnomalyOnDeathDaemon_",
  "Metadata/Monsters/LeagueAffliction/AfflictionDemonLightningGigaBall",
  "Metadata/Monsters/Daemon/AfflictionFirestormOnDeathDaemon_",
  "Metadata/Monsters/Totems/MonsterTotemArchnemesisObelisk" ,
  "Metadata/Monsters/Skeletons/DockSkeletonBow",
  "Metadata/Monsters/InvisibleAura/InvisibleHatredStationary",
  "Metadata/Monsters/InvisibleFire/InvisibleFireAfflictionFireTornado",
  'Metadata/Monsters/InvisibleFire/InvisibleFireAfflictionDemonColdDegen',
  "Metadata/Monsters/AnimatedItem/AnimatedWeaponSolarisChampion",
  "Metadata/Monsters/InvisibleFire/AfflictionBossFinalDeathZone",
  "Metadata/Monsters/Daemon/SkeletonSoldierBloodProjectileDaemon",
  "Metadata/Monsters/Frog/FrogGod/SilverOrbFromMonsters",
  "Metadata/Monsters/LeagueAffliction/Volatile/AfflictionVomitile",
  "Metadata/Monsters/InvisibleCurse/InvisibleFrostbiteStationary",

]

WAYPOINTS = [
  "1_1_town",
  "1_1_2",
  "1_1_4_1",
  "1_1_5",
  "1_1_6",
  "1_1_7_1",
  "1_1_8",
  "1_1_9",
  "1_1_11_1",
  "Unknown",
  "Unknown",
  "1_2_3",
  "1_2_5_1",
  "1_2_6_1",
  "1_2_4",
  "1_2_7",
  "1_2_8",
  "1_2_9",
  "1_2_12",
  "1_2_14_2",
  "Unknown",
  "Unknown",
  "1_3_3_1",
  "1_3_5",
  "1_3_7",
  "1_3_8_1",
  "1_3_8_2",
  "1_3_9",
  "1_3_10_1",
  "1_3_13",
  "1_3_14_1",
  "1_3_15",
  "Unknown",
  "1_3_18_1",
  "Unknown",
  "Unknown",
  "1_4_3_3",
  "1_4_4_3",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "1_5_3",
  "1_5_3b",
  "1_5_4",
  "1_5_5",
  "1_5_7",
  "Unknown",
  "Unknown",
  "2_6_2",
  "2_6_6",
  "2_6_7_1",
  "Unknown",
  "2_6_9",
  "2_6_10",
  "2_6_12",
  "2_6_14",
  "2_6_15",
  "Unknown",
  "2_7_2",
  "2_7_4",
  "2_7_5_1",
  "2_7_6",
  "2_7_7",
  "Unknown",
  "2_7_10",
  "2_7_11",
  "Unknown",
  "Unknown",
  "Unknown",
  "2_8_5",
  "2_8_6",
  "2_8_7_1_",
  "2_8_9",
  "2_8_10",
  "Unknown",
  "2_8_12_1",
  "Unknown",
  "Unknown",
  "2_9_3",
  "2_9_5",
  "Unknown",
  "Unknown",
  "Unknown",
  "2_10_2",
  "2_10_4",
  "2_10_7",
  "Unknown",
  "Unknown",
  "Labyrinth_Airlock", # 89
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
  "Unknown",
]

AURAS_SKILLS_TO_BUFFS = {

  "herald_of_ice":"herald_of_ice",
  "herald_of_thunder":"herald_of_thunder",
  "herald_of_light":"herald_of_light",
  "herald_of_ash": "herald_of_ash",
  "herald_of_agony":"herald_of_agony",

  "haste":"player_aura_speed",


  "anger":"player_aura_fire_damage",
  "spell_damage_aura":"player_aura_spell_damage",
  "damage_over_time_aura": "player_aura_damage_over_time",
  "wrath": "player_aura_lightning_damage",
  "hatred":"player_aura_cold_damage",
  "physical_damage_aura":"player_physical_damage_aura",

  "aura_accuracy_and_crits": "player_aura_accuracy_and_crits",
  "clarity":"player_aura_mana_regen",
  "vitality":"player_aura_life_regen",

  "purity":"player_aura_resists",
  "grace": "player_aura_evasion",
  "determination":"player_aura_armour",

  "discipline":"player_aura_energy_shield",
  "new_arctic_armour":"new_arctic_armour",
  "skitterbots": "skitterbots_buff",

  "banner_armour_evasion": "armour_evasion_banner_buff_aura",
  "banner_war":"bloodstained_banner_buff_aura",

  "call_to_arms": "call_to_arms",
  "automation": "automation",


}

ROGUE_EXILES_RENDER_NAMES_ENG = ["Orra Greengate","Thena Moga, the Crimson Storm","Ailentia Rac","Torr Olgosso","Torr Olgosso","Oyra Ona","Ainsley Varrich","Igna Phoenix","Kirmes Olli","Jonah Unchained","Damoi Tui","Bolt Brownfur, Earth Churner","Ohne Trix","Eoin Greyfur","Baracus Phraxisanct","Ion Darkshroud, the Hungering Blade","Wilorin Demontamer","Thom Imperial","Augustina Solaria","Torr Olgosso","Jonah Unchained","Orra Greengate","Ion Darkshroud","Eoin Greyfur","Minara Anemina","Hector Titucius, Eternal Servant","The Forgotten Soldier","Orra Greengate","Orra Greengate","Thena Moga","Thena Moga","Antalie Napora","Antalie Napora","Silva Fearsting","Ailentia Rac","Ailentia Rac","Torr Olgosso","Armios Bell","Armios Bell","Antonio Bravadi","Zacharie Desmarais","Zacharie Desmarais","Oyra Ona","Oyra Ona","Ainsley Varrich","Minara Anemina","Minara Anemina","Igna Phoenix","Igna Phoenix","Aria Vindicia","Dena Lorenni","Dena Lorenni","Ultima Thule","Ultima Thule","Kirmes Olli","Jonah Unchained","Damoi Tui","Damoi Tui","Xandro Blooddrinker","Xandro Blooddrinker","Haki Karukaru","Vickas Giantbone","Vickas Giantbone","Bolt Brownfur","Bolt Brownfur","Ohne Trix","Sevet Tetherein","Sevet Tetherein","Eoin Greyfur","Eoin Greyfur","Tinevin Highdove","Tinevin Highdove","Doven Falsetongue","Magnus Stonethorn","Magnus Stonethorn","Aurelio Voidsinger","Aurelio Voidsinger","Baracus Phraxisanct","Ion Darkshroud","Ion Darkshroud","Ash Lessard","Ash Lessard","Jarek Irontrap","Wilorin Demontamer","Wilorin Demontamer","Ulysses Morvant","Ulysses Morvant","Thom Imperial","Jade","Augustina Solaria","Augustina Solaria","Lael Furia","Lael Furia","Vanth Agiel","Vanth Agiel","Shade of a Scion","Shade of a Templar","Shade of a Duelist","Shade of a Marauder","Shade of a Shadow","Shade of a Witch","Shade of a Ranger","Dimachaeri Cassius","Mevia","Rudiarius Felix"]

ULTIMATUM_MODS_SAFE_KEYS = [
  # safe
  "Limited Arena",
  "Raging Dead I",
  "Raging Dead II",
  "Stormcaller Runes I",
  "Stormcaller Runes II",
  "Razor Dance I",
  "Razor Dance II",
  "Precise Monsters",
  "Hindering Flasks",
  "Unstoppable Monsters",
  "Overwhelming Monsters",
  "Random Projectiles",
  "Buffs Expire Faster",
  "Escalating Monster Speed",

  "Stormcaller Runes III",
  "Raging Dead III",
  "Stormcaller Runes IV",
  "Raging Dead IV",
  "Blistering Cold I",
  "Blistering Cold II",
  "Blistering Cold III",
  "Blistering Cold IV",
  "Razor Dance III",
  "Choking Miasma",
  "Resistant Monsters",
  "Unlucky Criticals",
  "Razor Dance IV",

  # chaos dot
  # ele dot 
  "Totem of Costly Potency",

  # phys dot
  "Totem of Costly Might",
  # bloody altar


  # totems
  # mob res
  "Dexterous Monsters",
  "Ailment and Curse Reflection",
  "Deadly Monsters",
  "Treacherous Auras",
  # extra mob damage
  "Prismatic Monsters",
  # reduced cd recovery
  "Less Cooldown Recovery",
  
]

ULTIMATUM_MODS_RUIN_KEYS = [
  "Lightning Damage from Mana Costs",
  "Drought",
  "Ruin",
  "Reduced Recovery",
]

DOOR_KEYWORDS = [
  "Metadata/MiscellaneousObjects/Door",
  "Heist/Objects/Level/Door_Basic",
  "/Lights/ScepterDoorLight",
  "/Lights/IncaDoorLight",
  "Level/Door_NPC",
  "Metadata/Terrain/Mountain/Belly/Objects/BellyArseDoor"
]


ULTIMATUM_ALTAR_PATH = "Metadata/Terrain/Leagues/Ultimatum/Objects/UltimatumChallengeInteractable"
HIDEOUT_ALVA_METADATA_KEY = "Metadata/NPC/League/Incursion/TreasureHunterHideout"
INCURSION_CLOSED_DOOR_PATH_KEY = "Metadata/Terrain/Leagues/Incursion/Objects/ClosedDoorPast"
INCURSION_EXIT_PORTAL_PATH_KEY = "Metadata/Terrain/Leagues/Incursion/Objects/IncursionPortal2"
SMALL_RGB_ITEM_KEYS = [
  "Art/2DItems/Weapons/OneHandWeapons/Daggers/Dagger",
  "Art/2DItems/Weapons/OneHandWeapons/Wands/Wand",
  'Art/2DItems/Weapons/OneHandWeapons/Claws/Claw',
  "Art/2DItems/Armours/Helmets/Helmet",
  "Art/2DItems/Armours/Shields/ShieldInt",
  "Art/2DItems/Armours/Boots/Boots",
]

ESSENCES_KEYWORD = "Metadata/MiscellaneousObjects/Monolith"

GOLD_COIN_ART = "Art/2DItems/Currency/Ruthless/CoinPileTier2.dds"

T17_MAP_NAMES = [
  "Fortress Map",
  "Ziggurat Map",
  "Sanctuary Map",
  "Citadel Map",
  "Abomination Map"
]
class MAPS:
  T17_MAP_NAMES = T17_MAP_NAMES 

class FLASK_TYPES:
  UTILITY = "utility"
  MANA = "mana"
  LIFE = "life"
class FLASKS:
  FLASK_TYPES = FLASK_TYPES

class SKILLS_INTERNAL_NAMES:
  ABSOLUTION = "absolution"
  
  BLOOD_RAGE = "blood_rage"

  FLAME_DASH = "flame_dash"
  FLICKER_STRIKE = "flicker_strike"
  FROST_BLADES = "frost_blades"
  FROSTBLINK = "frostblink"
  
  HOLY_FLAME_TOTEM = "holy_flame_totem"
  
  LIGHTNING_STRIKE = "lightning_strike"
  
  MOLTEN_STIKE = "molten_strike"

  PURIFYING_FLAME = "purifying_flame"
  
  RAISE_ZOMBIE = "raise_zombie"
  
  SHIELD_CHARGE = "shield_charge"
  SMITE = "smite"
  SPLITTING_STEEL = "splitting_steel"
  SUMMON_RAGING_SPIRIT = "summon_raging_spirit"
  SUMMON_SKELETONS = "summon_skeletons"
  
  VENOM_GYRE = "venom_gyre"
  VENOM_GYRE_VAAL = "vaal_venom_gyre"
  
  WHIRLING_BLADES = "whirling_blades"
  
class SKILLS:
  INTERNAL_NAMES_KEYS = SKILLS_INTERNAL_NAMES
  
class CONSTANTS:
  FLASKS = FLASKS
  MAPS = MAPS
  SKILLS = SKILLS
