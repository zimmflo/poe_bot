import copy

# https://poe.ninja/api/data/currencyoverview?league=Sanctum&type=Currency&language=en \

'''
https://poe.ninja/api/data/itemoverview?league=Crucible&type=Fossil&language=en

cheap = []
expensive = []

data.lines.map(el=>{ 
	if (el.chaosValue > 2){
		expensive.push(el)
	}else{
		cheap.push(el)
	}})

String(cheap.map(el=>`"`+el.name+`" `)).replaceAll(',','')

String(expensive.map(el=>`"`+el.name+`" `)).replaceAll(',','')

out:
"Fractured Fossil" "Faceted Fossil" "Glyphic Fossil" "Hollow Fossil" "Shuddering Fossil" "Corroded Fossil" "Sanctified Fossil" "Serrated Fossil" "Prismatic Fossil" "Bloodstained Fossil" "Bound Fossil" "Tangled Fossil" "Deft Fossil"

// decks

expensive = []
data.lines.map(el=>{
	let stack_price = el.chaosValue * el.stackSize;
	if (stack_price > 100){
		expensive.push(el);
	};
});

String(expensive.map(el=>`"`+el.name+`" `)).replaceAll(',','')
"The Apothecary" "House of Mirrors" "The Price of Devotion" "The Doctor" "Unrequited Love" "The Insane Cat" "The Demon" "The Fiend" "The Immortal" "The Shieldbearer" "The Nurse" "Love Through Ice" "The Price of Loyalty" "The Cheater" "The Chosen" "Choking Guilt" "Seven Years Bad Luck" "The Sephirot" "Wealth and Power" "The Rabbit's Foot" "The Soul" "The Endless Darkness" "Divine Beauty" "The Garish Power" "The Dragon's Heart" "The Samurai's Eye" "Desecrated Virtue" "Doryani's Epiphany" "The Enlightened" "Beauty Through Death" "Matryoshka" "A Fate Worse Than Death" "Succor of the Sinless" "The Artist" "Home" "The Patient" "Gemcutter's Mercy" "The Last One Standing" "The Eye of Terror" "Luminous Trove" "The Destination" "The Strategist" "Tranquillity" "The Greatest Intentions" "The Eye of the Dragon" "The Hunger" "Rebirth"
;
'''


cheap_scarabs = """

Show # cheap_scarabs
	Class "Map Fragments"
	BaseType "Scarab"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""
expensive_scarabs_list = [
	"Divination Scarab of Pilfering"
]

expensive_scarabs = f"""

Show # expensive_scarabs
	Class "Map Fragments"
	BaseType {' '.join(list(map(lambda l: f'"{l}"', expensive_scarabs_list)))}
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

inscribed_ultimatum = """

Show # $type->miscmapitemsextra $tier->itemizedleagues
	BaseType == "Inscribed Ultimatum" "Chronicle of Atzoatl"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

"""

expensive_allflames = """

## allflames
# always valuable
Show # $type->necropolis $tier->t2
	Class == "Embers of the Allflame"
	BaseType == "Allflame Ember of Manifested Wealth"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

# syndicate 
Show # $type->necropolis $tier->t2
	Class == "Embers of the Allflame"
	AreaLevel >= 82
	BaseType == "Allflame Ember of Syndicate Assassins" "Allflame Ember of Syndicate Escorts" "Allflame Ember of Syndicate Guards" "Allflame Ember of Syndicate Researchers"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

# 
Show # $type->necropolis $tier->t2
	Class == "Embers of the Allflame"
	AreaLevel >= 82
	BaseType == "Flaring Allflame Ember of Kalguurans"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

#
Show # $type->necropolis $tier->t2
	Class == "Embers of the Allflame"
	AreaLevel >= 84
	BaseType == "Flaring Allflame Ember of Wildwood Cultists"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

essence_scarabs = """

Show # cheap_scarabs
	Class "Map Fragments"
	BaseType == "Essence Scarab"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

beast_scarabs = """

Show # cheap_scarabs
	Class "Map Fragments"
	BaseType == "Bestiary Scarab of The Herd" "Bestiary Scarab of Duplicating"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

chaos_shards = """

Show # chaos_shards
	Class "Currency"
	BaseType "Chaos Shard"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

alch_chisel = """
#alch_chisel
Show 
	Class "Currency"
	BaseType "Orb of Alchemy" "Cartographer's Chisel"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

alch_orb = """
#alch_chisel
Show 
	Class "Currency"
	BaseType "Orb of Alchemy"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

valuable_fossils = """
# expensive only
Show # $type->currency->fossil $tier->restex
	Class "Currency"
	BaseType "Fractured Fossil" "Faceted Fossil" "Glyphic Fossil" "Hollow Fossil" "Shuddering Fossil" "Corroded Fossil" "Sanctified Fossil" "Serrated Fossil" "Prismatic Fossil" "Bloodstained Fossil" "Bound Fossil" "Tangled Fossil" "Deft Fossil"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
"""
cheap_fossils = """

Show # $type->currency->fossil $tier->restex
	Class "Currency"
	BaseType "Fossil"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
"""

always_valuable_items = """
## always_valuable_items

Show # VALUABLE CURRENCY
	Class "Currency"
	BaseType "Mirror of Kalandra" "Hinekora's Lock" "Mirror Shard" "Fracturing Orb" "Tempering Orb" "Tailoring Orb" "Blessing of Chayula" "Tainted Divine Teardrop" "Secondary Regrading Lens" "Orb of Dominance" "Blessing of Xoph" "Blessing of Tul" "Blessing of Esh" "Hunter's Exalted Orb" "Blessing of Uul-Netol" "Divine Orb" "Sacred Crystallised Lifeforce" "Prime Regrading Lens" "Fracturing Shard" "Orb of Conflict" "Sacred Orb" "Elevated Sextant" "Valdo's Puzzle Box"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # VALUABLE CURRENCY fragments
	Class "Currency"
	BaseType  "Tainted Blessing" "Exceptional Eldritch Ember" "Exceptional Eldritch Ichor" "Eldritch Chaos Orb" "Redeemer's Exalted Orb" "Crusader's Exalted Orb" "Eldritch Orb of Annulment" "Awakener's Orb" "Comprehensive Scouting Report" "Warlord's Exalted Orb"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # VALUABLE CURRENCY fragments
	Class "Currency"
	BaseType "Stacked Deck" "Tainted Orb of Fusing" "Tainted Exalted Orb" "Exalted Orb" "Unstable Catalyst" "Prismatic Catalyst" "Orb of Annulment" "Otherworldly Scouting Report" "Veiled Orb" "Grand Eldritch Ember" "Eldritch Exalted Orb" "Ancient Orb" "Oil Extractor" "Ritual Vessel" "Tainted Mythic Orb"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # VALUABLE CURRENCY fragments
	Class "Currency"
	BaseType "Ancient Shard" "Exalted Shard" "Annulment Shard"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255



Show # harvest currency
	Class "Currency"
	BaseType == "Primal Crystallised Lifeforce" "Vivid Crystallised Lifeforce" "Wild Crystallised Lifeforce" "Sacred Crystallised Lifeforce"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

"""

delirium_orbs = """

Show # deli orb
	Class "Currency"
	BaseType "Delirium Orb"
	SetBorderColor 255 0 0 255
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

"""


cluster_jewels = """
#### cluster jewels
Hide # Megalomaniac
	Rarity Unique
	BaseType "Medium Cluster Jewel"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->jewels->clustereco $tier->n3_i84_t1
	Rarity Normal Magic Rare
	ItemLevel >= 84
	EnchantmentPassiveNum 3
	BaseType "Small Cluster Jewel"
	EnchantmentPassiveNode "Reservation Efficiency"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # 12slot  expensive
	ItemLevel >= 84
	Rarity Normal Magic Rare
	EnchantmentPassiveNum 12
	BaseType "Large Cluster Jewel"
	EnchantmentPassiveNode "Bow Damage" "Minion Damage" "Spell Damage"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # 8 slot expensive
	ItemLevel == 50
	Rarity Normal Magic Rare
	EnchantmentPassiveNum 8
	BaseType "Large Cluster Jewel" 
	EnchantmentPassiveNode "Fire Damage" "Bow Damage" "Attack Damage" "Attack Damage while holding a Shield"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # 6 slot expensive
	Rarity Normal Magic Rare
	ItemLevel >= 84
	EnchantmentPassiveNum 6
	BaseType "Medium Cluster Jewel"
	EnchantmentPassiveNode "Flask Duration"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

# valuable fragments
Show 
	Class "Currency"
	BaseType "Splinter of Uul-Netol" "Splinter of Chayula" "Timeless Maraketh Splinter" "Timeless Templar Splinter"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->fragments $tier->t1
	Class "Map Fragments"
	SetFontSize 18
	SetBorderColor 255 0 0 255
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
	BaseType == "Chayula's Breachstone" "Chayula's Charged Breachstone" "Chayula's Enriched Breachstone" "Chayula's Flawless Breachstone" "Esh's Flawless Breachstone" "Gift to the Goddess" "The Maven's Writ" "Uul-Netol's Flawless Breachstone"
Show # $type->fragments $tier->t1
	Class "Map Fragments"
	SetFontSize 18
	SetBorderColor 255 0 0 255
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
	BaseType == "Baran's Crest" "Dedication to the Goddess" "Esh's Charged Breachstone" "Esh's Enriched Breachstone" "Esh's Pure Breachstone" "Fragment of Constriction" "Fragment of Emptiness" "Fragment of Enslavement" "Fragment of Eradication" "Fragment of Knowledge" "Fragment of Purification" "Fragment of Shape" "Fragment of Terror" "Fragment of the Chimera" "Mortal Ignorance" "Sacred Blossom" "Simulacrum" "Timeless Maraketh Emblem" "Timeless Templar Emblem" "Tribute to the Goddess" "Tul's Charged Breachstone" "Tul's Enriched Breachstone" "Tul's Flawless Breachstone" "Tul's Pure Breachstone" "Unrelenting Timeless Eternal Emblem" "Unrelenting Timeless Maraketh Emblem" "Unrelenting Timeless Templar Emblem" "Uul-Netol's Breachstone" "Uul-Netol's Charged Breachstone" "Uul-Netol's Enriched Breachstone" "Uul-Netol's Pure Breachstone" "Xoph's Charged Breachstone" "Xoph's Enriched Breachstone" "Xoph's Flawless Breachstone" "Xoph's Pure Breachstone"
Show # $type->fragments $tier->t1
	Class "Map Fragments"
	SetFontSize 18
	SetBorderColor 255 0 0 255
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
	BaseType == "Al-Hezmin's Crest" "Blood-filled Vessel" "Chayula's Pure Breachstone" "Drox's Crest" "Esh's Breachstone" "Fragment of the Hydra" "Fragment of the Minotaur" "Fragment of the Phoenix" "Mortal Grief" "Mortal Hope" "Mortal Rage" "Timeless Eternal Emblem" "Timeless Karui Emblem" "Timeless Vaal Emblem" "Tul's Breachstone" "Unrelenting Timeless Karui Emblem" "Unrelenting Timeless Vaal Emblem" "Veritania's Crest" "Xoph's Breachstone"


"""

uniques = """
#### UNIQUES SECTION
# Split personality
Show # $type->uniques $tier->exforgesword
	Rarity Unique
	BaseType == "Crimson Jewel"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # hh mb
	Rarity Unique
	BaseType == "Leather Belt" "Heavy Belt"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

#------------------------------------
#   [4201] Exceptions #1
#------------------------------------

Show # $type->uniques $tier->exuberimpresence
	HasInfluence "Shaper"
	HasInfluence "Elder"
	Rarity Unique
	BaseType "Onyx Amulet"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->exsquire
	Sockets >= 3WWW
	Rarity Unique
	BaseType == "Elegant Round Shield"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->extabula
	Rarity Unique
	SocketGroup "WWWWWW"
	BaseType == "Simple Robe"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->exforgesword
	HasInfluence "Elder" "Shaper"
	Rarity Unique
	BaseType == "Infernal Sword"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->exrationaljewel
	SynthesisedItem True
	Rarity Unique
	Class "Jewel"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->exsynth
	SynthesisedItem True
	Rarity Unique
	Class "Rings"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->ex6link
	LinkedSockets 6
	Rarity Unique
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

#------------------------------------
#   [4202] Tier 1 and 2 uniques
#------------------------------------

Show # $type->uniques $tier->t1
	Rarity Unique
	BaseType == "Champion Kite Shield" "Crusader Boots" "Ezomyte Tower Shield" "Fluted Bascinet" "Ghastly Eye Jewel" "Gladiator Plate" "Golden Buckler" "Greatwolf Talisman" "Karui Maul" "Painted Tower Shield" "Prismatic Jewel" "Prophecy Wand" "Rawhide Boots" "Ring" "Riveted Boots" "Sapphire Flask" "Siege Axe" "Unset Amulet" "Vaal Rapier" "Wyrmscale Doublet"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->t2
	Rarity Unique
	BaseType == "Blood Raiment" "Blue Pearl Amulet" "Branded Kite Shield" "Butcher Axe" "Carnal Boots" "Crimson Round Shield" "Cutlass" "Embroidered Gloves" "Ezomyte Burgonet" "Ezomyte Spiked Shield" "Foul Staff" "Imperial Maul" "Jewelled Foil" "Jingling Spirit Shield" "Large Cluster Jewel" "Leather Hood" "Medium Cluster Jewel" "Occultist's Vestment" "Ornate Quiver" "Raven Mask" "Reinforced Greaves" "Ruby Flask" "Runic Helm" "Runic Sabatons" "Runic Sollerets" "Savant's Robe" "Searching Eye Jewel" "Silk Gloves" "Slaughter Knife" "Sovereign Spiked Shield" "Steel Kite Shield" "Steelwood Bow" "Studded Belt" "Timeless Jewel" "Void Axe" "Wyrmscale Boots"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

#------------------------------------
#   [4203] Exceptions #2
#------------------------------------

Show # $type->uniques $tier->2xcorrupteduniques
	Corrupted True
	CorruptedMods >= 2
	Rarity Unique
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->2xabyss
	Sockets >= AA
	Rarity Unique
	Class == "Boots" "Gloves" "Helmets"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->uniques $tier->excrucibleunique
	HasCruciblePassiveTree True
	Rarity Unique
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

#------------------------------------
#   [4204] Multi-Unique bases.
#------------------------------------
# These bases have multiple uniques. One of the uniques, is a high value one
# While others are cheap. We give them a high quality display, while making a normal unique
# Sound to prevent false excitement.

Hide # %D4 $type->uniques $tier->5link
	LinkedSockets 5
	Rarity Unique
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Hide # $type->uniques $tier->multispecial
	Rarity Unique
	BaseType == "Amber Amulet" "Amethyst Ring" "Archon Kite Shield" "Assassin Bow" "Carved Wand" "Crusader Plate" "Crystal Sceptre" "Ebony Tower Shield" "Fencer Helm" "Fiend Dagger" "Gavel" "Glorious Plate" "Gold Ring" "Heavy Belt" "Hellion's Paw" "Highborn Staff" "Hydrascale Gauntlets" "Hypnotic Eye Jewel" "Imperial Bow" "Imperial Skean" "Iron Circlet" "Lacquered Garb" "Leather Belt" "Moonstone Ring" "Murder Mitts" "Murderous Eye Jewel" "Necromancer Circlet" "Necromancer Silks" "Onyx Amulet" "Paua Amulet" "Prophet Crown" "Sadist Garb" "Sage Wand" "Sage's Robe" "Saint's Hauberk" "Saintly Chainmail" "Sapphire Ring" "Small Cluster Jewel" "Solaris Circlet" "Sorcerer Boots" "Spidersilk Robe" "Spine Bow" "Stealth Boots" "Stibnite Flask" "Titan Gauntlets" "Titanium Spirit Shield" "Turquoise Amulet" "Unset Ring" "Vaal Claw" "Wyrmscale Gauntlets" "Zodiac Leather"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

# For those 6 sockets	

Hide # %D5 $type->uniques $tier->6s
	Sockets >= 6
	Rarity Unique
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255


"""

valuable_gems = '''
# gems
Show # $type->gems-exceptional $tier->awat1
	Class "Gems"
	BaseType "Awakened Chain Support" "Awakened Elemental Damage with Attacks Support" "Awakened Elemental Focus Support" "Awakened Empower Support" "Awakened Enhance Support" "Awakened Enlighten Support" "Awakened Fork Support" "Awakened Greater Multiple Projectiles Support" "Awakened Increased Area of Effect Support" "Awakened Multistrike Support" "Awakened Spell Echo Support"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->gems-exceptional $tier->altany
	AlternateQuality True
	Class "Gems"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Show # $type->gems-special $tier->exspecial
	Class "Gems"
	BaseType "Empower" "Enhance" "Enlighten" "Item Quantity" "Vaal Breach"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
'''

all_essences = """
Show # all essences
	Class "Currency"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
	BaseType "Essence of" "Remnant of Corruption"

"""

essences_wailing = """

Show # shit essences
	Class "Currency"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
	BaseType "Wailing Essence of"
"""

essences_expensive = """
# essences
Show # $type->currency->essence $tier->t1
	Class "Currency"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
	BaseType "Deafening Essence of" "Essence of Delirium" "Essence of Horror" "Essence of Hysteria" "Essence of Insanity"
Show # $type->currency->essence $tier->t1
	Class "Currency"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
	BaseType "Remnant of Corruption" "Shrieking Essence of"
Show # $type->currency->essence $tier->t1
	Class "Currency"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
	BaseType "Screaming Essence of"

"""

incubators = """
# incubators
Show # $type->currency->incubators $tier->t1
	Class "Incubator"
	BaseType "Fine Incubator" "Ornate Incubator" "Diviner's Incubator" "Skittering Incubator"
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

"""

expensive_maps = """

Show # $type->maps->influenced $tier->infshaper
	Class "Maps"
	BaseType "Vaal Temple Map"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

Show # $type->maps->influenced $tier->infshaper
	HasInfluence Shaper Elder Crusader Hunter Redeemer Warlord
	Rarity Normal Magic Rare
	Class "Maps"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

"""

exclude_expensive_maps = """

Hide # $type->maps->influenced $tier->infshaper
	Class "Maps"
	BaseType "Vaal Temple Map"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

Hide # $type->maps->influenced $tier->infshaper
	HasInfluence Shaper Elder Crusader Hunter Redeemer Warlord
	Rarity Normal Magic Rare
	Class "Maps"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

"""

all_maps = """
Show
	Class "Maps"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

"""

exclude_unique_maps = """
Hide
	Class "Maps"
	Rarity Unique
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

"""

low_eldritch_currency = [ "Lesser Eldritch Ember", "Lesser Eldritch Ichor", "Greater Eldritch Ember", "Greater Eldritch Ichor"]
high_eldritch_currency = [ "Grand Eldritch Ember", "Exceptional Eldritch Ember", "Grand Eldritch Ichor", "Exceptional Eldritch Ichor"]
# map-tier currency which is needed to do atlas rush 
map_currencies = ["Orb of Chance", "Orb of Alchemy", "Vaal Orb", "Orb of Regret", "Orb of Fusing", "Orb of Scouring", "Orb of Horizons", "Orb of Unmaking", "Orb of Binding"]
# needed for initial leveling, rolling on items\sockets, also ok to sell
need_for_gear_currencies = ["Vaal Orb", "Orb of Regret", "Gemcutter's Prism", "Glassblower's Bauble", "Instilling Orb", "Orb of Fusing", "Orb of Scouring", "Orb of Unmaking"]
# ok to sell
tier_ok_currencies = ["Blessed Orb", "Jeweller's Orb", "Orb of Binding", "Glassblower's Bauble", "Instilling Orb", "Orb of Fusing", "Chromatic Orb"]
# not ok to sell
tier_soso_currencies = ["Orb of Alteration", "Jeweller's Orb", "Orb of Binding", "Orb of Augmentation", "Chromatic Orb", "Regal Orb"]
# just shit
tier_shit_currencies = ["Engineer's Orb", "Armourer's Scrap", "Blacksmith's Whetstone", "Portal Scroll", "Orb of Transmutation" ]

unsorted = """
Show # catalysts
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
	BaseType "Noxious Catalyst" "Intrinsic Catalyst" "Tempering Catalyst" "Accelerating Catalyst" "Abrasive Catalyst" "Imbued Catalyst" "Turbulent Catalyst" "Prismatic Catalyst" "Unstable Catalyst" "Fertile Catalyst"
	Class "Currency"

# valuable oils
Show
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
	BaseType "Crimson Oil" "Black Oil" "Opalescent Oil" "Silver Oil" "Golden Oil"
	Class "Currency"
# other oils
Hide
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255
	BaseType "Oil"
	Class "Currency"


Show # resonators
	Class "Resonator"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255




Hide # $type->currency->incubators $tier->t2
	Class "Incubator"
	BaseType == "Gemcutter's Incubator" 
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255

Hide # %H5 $type->currency->incubators $tier->t3
	Class "Incubator"
	BaseType ==   "Fossilised Incubator"  "Singular Incubator" 
	SetBorderColor 255 0 0 255
	SetFontSize 18
	SetTextColor 255 0 0 255
	SetBackgroundColor 255 0 0 255




#### MAPS

Show # $type->exotic->invitation $tier->t1
	Rarity Normal Magic Rare
	BaseType == "Incandescent Invitation" "Screaming Invitation" "Maven's Invitation: The Elderslayers" "Maven's Invitation: The Formed"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

Show # $type->exotic->invitation $tier->t2
	Rarity Normal Magic Rare
	BaseType == "Maven's Invitation: The Feared" "Maven's Invitation: The Forgotten" "Maven's Invitation: The Hidden" "Maven's Invitation: The Twisted"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255

Show # $type->exoticmap->memory $tier->handpicked
	BaseType == "Einhar's Memory"
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255



"""

default_display = """
	SetFontSize 18
	SetTextColor 0 0 0 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 249 150 25 255
"""

def generateLootFilterCell(
	show=True,
	item_class = None,
	base_type = None,
	min_map_tier = None,
	max_map_tier = None,
	min_sockets = None,
	min_links = None,
	min_amount = None,


	):
	cell_string = ''
	
	cell_string+= "Show" if show is True else "Hide"
	# cell_string+= "\n"
	if item_class is not None:
		cell_string += f'\n\tClass == "{item_class}"'

	if base_type is not None and base_type != [] and base_type != "":
		cell_string += f"\n\tBaseType == {base_type}"

	if min_sockets is not None:
		cell_string += f"\n\tSockets >= {min_sockets}"

	if min_links is not None:
		cell_string += f"\n\tLinkedSockets >= {min_links}"

	if min_map_tier is not None:
		cell_string += f"\n\tMapTier >= {min_map_tier}"

	if max_map_tier is not None:
		cell_string += f"\n\tMapTier <= {max_map_tier}"

	if min_amount is not None:
		cell_string += f"\n\tStackSize >= {min_amount}"

	cell_string+= f"{default_display}\n"
	cell_string+= "\n"
	return cell_string

class LootFilterSettings:
	add_simulacrum_splinters = True
	add_eldritch_currency = True
	add_low_eldritch_currency = True
	collect_tabula_cards = True
	add_incubators = True

	all_essences = False 
	essences_wailing = True
	essences_expensive = True
	
	scarabs_cheap = True
	scarabs_expensive = True
	add_bestiary_scrabs = False
	add_essence_scarabs = False
	alch_chisel = True
	alch_orb = False
	add_portals = True
	
	add_cheap_fossils = True
	add_valuable_fossils = True
	
	
	all_maps = True
	expensive_maps = True
	exclude_maps = []
	only_maps = []
	exclude_unique_maps = False
	exclude_expensive_maps = True
	map_min_tier = None
	map_max_tier = None
	def __init__(
		self,
		add_map_currencies = True,
		add_need_for_gear_currencies = True,
		add_tier_ok_currencies = True,
		add_tier_soso_currencies = True,
		add_tier_shit_currencies = False,
		add_silver_coins = True,
		min_sockets_to_collect = None,
		min_links_to_collect = None,
		min_chaos_orbs = None,
		add_chaos_shards = True,
		show_expensive_allflames = True,
		show_inscribed_ultimatum = True,
		show_delirium_orbs = True,
		show_uniques = True,
		) -> None:


		self.add_map_currencies = add_map_currencies
		self.add_need_for_gear_currencies = add_need_for_gear_currencies
		self.add_tier_ok_currencies = add_tier_ok_currencies
		self.add_tier_soso_currencies = add_tier_soso_currencies
		self.add_tier_shit_currencies = add_tier_shit_currencies
		self.add_silver_coins = add_silver_coins

		self.show_expensive_allflames = show_expensive_allflames

		self.min_sockets_to_collect = min_sockets_to_collect
		self.min_links_to_collect = min_links_to_collect
		self.min_chaos_orbs = min_chaos_orbs
		self.add_chaos_shards = add_chaos_shards
		self.show_inscribed_ultimatum = show_inscribed_ultimatum
		self.show_delirium_orbs = show_delirium_orbs
		self.show_uniques = show_uniques

class LootFilter():
	def __init__(self, settings = LootFilterSettings()) -> None:
		self.settings = settings
		self.valuable_decks = '''"The Fortunate" "Fire of Unknown Origin" "Darker Half" "The Apothecary" "House of Mirrors" "The Price of Devotion" "The Doctor" "Unrequited Love" "The Insane Cat" "The Demon" "The Fiend" "The Immortal" "The Shieldbearer" "The Nurse" "Love Through Ice" "The Price of Loyalty" "The Cheater" "The Chosen" "Choking Guilt" "Seven Years Bad Luck" "The Sephirot" "Wealth and Power" "The Rabbit's Foot" "The Soul" "The Endless Darkness" "Divine Beauty" "The Garish Power" "The Dragon's Heart" "The Samurai's Eye" "Desecrated Virtue" "Doryani's Epiphany" "The Enlightened" "Beauty Through Death" "Matryoshka" "A Fate Worse Than Death" "Succor of the Sinless" "The Artist" "Home" "The Patient" "Gemcutter's Mercy" "The Last One Standing" "The Eye of Terror" "Luminous Trove" "The Destination" "The Strategist" "Tranquillity" "The Greatest Intentions" "The Eye of the Dragon" "The Hunger" "Rebirth" '''
		self.valuable_fossils = []
		self.valuable_scarabs = []
		self.valuable_cluster = []
	def returnString(self,):
		loot_filter_str = ""
		loot_filter_str += "# generated loot filter\n"
		loot_filter_str += always_valuable_items
		loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type='"Chaos Orb"', min_amount=self.settings.min_chaos_orbs)

		loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type=' '.join(list(map(lambda s: f'"{s}"', high_eldritch_currency))))
		if self.settings.add_low_eldritch_currency: loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type=' '.join(list(map(lambda s: f'"{s}"', low_eldritch_currency))))

		if self.settings.exclude_unique_maps is True: loot_filter_str += exclude_unique_maps
		if self.settings.exclude_expensive_maps is True: loot_filter_str += exclude_expensive_maps

		loot_filter_str += cluster_jewels
		if self.settings.show_uniques: loot_filter_str += uniques
		loot_filter_str += valuable_gems
		
		div_cads = self.valuable_decks
		if self.settings.collect_tabula_cards is True:
			div_cads += ''' "Humility" "Vanity"'''
		loot_filter_str += generateLootFilterCell(show=True, item_class="Divination Card", base_type=div_cads)

		if self.settings.add_simulacrum_splinters: loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type='"Simulacrum Splinter"')
		if self.settings.add_portals: loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type='"Portal Scroll"')
		
		if self.settings.add_map_currencies: loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type=' '.join(list(map(lambda s: f'"{s}"', map_currencies))))
		if self.settings.add_need_for_gear_currencies: loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type=' '.join(list(map(lambda s: f'"{s}"', need_for_gear_currencies))))

		if self.settings.add_tier_ok_currencies: loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type=' '.join(list(map(lambda s: f'"{s}"', tier_ok_currencies))))
		if self.settings.add_tier_soso_currencies:loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type=' '.join(list(map(lambda s: f'"{s}"', tier_soso_currencies))))
		if self.settings.add_tier_shit_currencies: loot_filter_str += generateLootFilterCell(show=True, item_class="Currency", base_type=' '.join(list(map(lambda s: f'"{s}"', tier_shit_currencies))))

		if len(self.settings.exclude_maps) != 0: 
			loot_filter_str += generateLootFilterCell(show=False, item_class="Maps", base_type=' '.join(list(map(lambda s: f'"{s}"', self.settings.exclude_maps))))
		if self.settings.expensive_maps: loot_filter_str += expensive_maps
		if self.settings.map_min_tier or self.settings.map_max_tier or self.settings.only_maps:
			loot_filter_str += generateLootFilterCell(show=True, item_class="Maps", base_type = ' '.join(list(map(lambda s: f'"{s}"', self.settings.only_maps))), min_map_tier=self.settings.map_min_tier, max_map_tier=self.settings.map_max_tier)
		else:
			if self.settings.all_maps: loot_filter_str += all_maps

		if self.settings.add_chaos_shards: loot_filter_str += chaos_shards
		if self.settings.show_delirium_orbs: loot_filter_str += delirium_orbs

		if self.settings.show_expensive_allflames: loot_filter_str += expensive_allflames
		if self.settings.show_inscribed_ultimatum: loot_filter_str += inscribed_ultimatum

		if self.settings.add_cheap_fossils: loot_filter_str += cheap_fossils
		if self.settings.add_valuable_fossils: loot_filter_str += valuable_fossils
		
		if self.settings.all_essences: loot_filter_str += all_essences
		if self.settings.essences_wailing: loot_filter_str += essences_wailing
		if self.settings.essences_expensive: loot_filter_str += essences_expensive
		
		if self.settings.scarabs_cheap: loot_filter_str += cheap_scarabs
		if self.settings.add_essence_scarabs: loot_filter_str += essence_scarabs
		if self.settings.scarabs_expensive: loot_filter_str += expensive_scarabs

		if self.settings.alch_orb: loot_filter_str += alch_orb
		if self.settings.alch_chisel: loot_filter_str += alch_chisel
		if self.settings.add_bestiary_scrabs: loot_filter_str += beast_scarabs


		if self.settings.min_links_to_collect is not None: loot_filter_str += generateLootFilterCell(show=True, min_links=self.settings.min_links_to_collect)
		if self.settings.min_sockets_to_collect is not None: loot_filter_str += generateLootFilterCell(show=True, min_sockets=self.settings.min_sockets_to_collect)

		loot_filter_str += unsorted

		loot_filter_str += "\nHide"
		return loot_filter_str

def writeLootFilter(
		loot_filter_string: str,
		file_name = 'default',
	):
	f = open(f"./{file_name}.filter", "w", encoding="utf-8")
	f.close()

	f = open(f"./{file_name}.filter", "a", encoding="utf-8")
	f.write(loot_filter_string)
	f.close()

def main():
	loot_filter = LootFilter()

	default_settings = LootFilterSettings()
	# yellow\red stable mapper
	mid_settings = copy.copy(default_settings)
	mid_settings.collect_tabula_cards = False
	mid_settings.add_cheap_fossils = False
	mid_settings.add_valuable_fossils = False
	mid_settings.add_tier_soso_currencies = False
	mid_settings.add_tier_ok_currencies = False
	mid_settings.essences_wailing = False
	# ready to go farmer
	strict_settings = copy.copy(mid_settings)
	strict_settings.exclude_maps = ['Forking River Map', "Core Map", "Laboratory Map", "Vault Map", "Frozen Cabins Map", "Colosseum Map", "Arena Map", "Caldera Map", "Pit Map"]
	strict_settings.add_chaos_shards = False
	strict_settings.exclude_unique_maps = True
	strict_settings.add_valuable_fossils = False
	strict_settings.add_low_eldritch_currency = False
	strict_settings.add_map_currencies = False
	strict_settings.add_need_for_gear_currencies = False
	strict_settings.all_essences= False
	strict_settings.essences_expensive = False
	strict_settings.essences_wailing = False
	strict_settings.scarabs_cheap = False
	strict_settings.scarabs_expensive = True
	strict_settings.alch_chisel = False

	## Early
	# default
	loot_filter.settings = copy.copy(default_settings)
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="default")
	# atlas rush + aqueduct
	loot_filter.settings.min_links_to_collect=5
	loot_filter.settings.min_sockets_to_collect=6
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="early_atlas_rush")
	## MID
	# when got equip, and farming essences
	loot_filter.settings = copy.copy(mid_settings)
	loot_filter.settings.add_map_currencies = True
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="early_atlas_rush_strict")
	
	## LATE
	# essence
	loot_filter.settings = copy.copy(strict_settings)
	loot_filter.settings.show_uniques = False
	loot_filter.settings.add_valuable_fossils = False
	loot_filter.settings.show_expensive_allflames = False
	loot_filter.settings.add_simulacrum_splinters = False
	loot_filter.settings.show_delirium_orbs = False
	loot_filter.settings.scarabs_expensive = False
	loot_filter.settings.essences_expensive = True
	loot_filter.settings.add_essence_scarabs = True
	loot_filter.settings.map_min_tier = 6
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="yellow_essence")
	loot_filter.settings.essences_wailing = True
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="yellow_essence_plusWailing")
	loot_filter.settings.all_essences = True
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="yellow_essence_allEss")

	# alva or beasts
	loot_filter.settings = copy.copy(strict_settings)
	loot_filter.settings.show_uniques = False
	loot_filter.settings.add_valuable_fossils = False
	loot_filter.settings.show_expensive_allflames = False
	loot_filter.settings.scarabs_expensive = False
	loot_filter.settings.map_max_tier = 5
	loot_filter.settings.alch_chisel = True
	loot_filter.settings.show_delirium_orbs = False
	loot_filter.settings.add_simulacrum_splinters = False
	loot_filter.settings.alch_chisel = False
	loot_filter.settings.add_chaos_shards = False
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="white_alva_pick_chaos")
	loot_filter.settings.min_chaos_orbs = 2
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="white_alva")
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="white_beast")
	loot_filter.settings.map_min_tier = 14
	loot_filter.settings.map_max_tier = None
	writeLootFilter(loot_filter_string=loot_filter.returnString(),file_name="red_beast")


main()