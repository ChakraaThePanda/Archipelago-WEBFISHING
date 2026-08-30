from BaseClasses import Location
import typing

class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    # region: str


class WebfishingAdvancement(Location):
    game: str = "WEBFISHING"


def populate_advancement_tables():
    counter = 0

    # 3 lots of easy generic catch quests
    no = 3
    for i, name in enumerate(gcq_easy):
        for x in range(no):
            title = f"{name} Quest ({x + 1}/{no})"
            item = AdvData(quest_offset + counter)
            standard_base[title] = item
            assign_rod(name, title, item)
            counter += 1

    # 2 lots of normal generic catch quests
    no = 2
    for i, name in enumerate(gcq_normal):
        for x in range(no):
            title = f"{name} Quest ({x + 1}/{no})"
            item = AdvData(quest_offset + counter)
            standard_base[title] = item
            assign_rod(name, title, item)
            counter += 1

    # 2 lots of hard generic catch quests
    no = 2
    for i, c in enumerate(gcq_hard):
        for x in range(no):
            hard[f"{c} Quest ({x + 1}/{no})"] = AdvData(quest_offset + counter)
            counter += 1

    # 2 lots of (all) normal specific catch quests (>1% chance according to wiki, no extra bait req.)
    no = 2
    for i, name in enumerate(scq_normal):
        for x in range(no):
            title = f"{name} Quest ({x + 1}/{no})"
            item = AdvData(quest_offset + counter)
            scqe[title] = item
            assign_rod(name, title, item)
            counter += 1

    # 1 of hard specific catch quests (so only need to catch 1, no second check for 5)
    for name in scq_hard:
        title = f"{name} Quest (1/1)"
        item = AdvData(quest_offset + counter)
        hard_specific[title] = item
        assign_rod(name, title, item)
        counter += 1

    # --- MISC --- #

    # reset counter
    counter = 0

    # one of each in misc
    for c in base_misc:
        standard_base[c] = AdvData(item_offset + counter)
        counter += 1

    # --- SHOPS --- #

    # another reset
    counter = 0

    # progression shop checks

    # t1 checks
    for i in range(8):
        standard_base[f"T1 Progression Shop Purchase ({i+1})"] = AdvData(shop_offset + counter)
        counter += 1

    # t2 checks
    for i in range(8):
        camp_2[f"T2 Progression Shop Purchase ({i+1})"] = AdvData(shop_offset + counter)
        counter += 1

    # t3 checks
    for i in range(8):
        camp_3[f"T3 Progression Shop Purchase ({i+1})"] = AdvData(shop_offset + counter)
        counter += 1

    # t4 checks
    for i in range(8):
        camp_4[f"T4 Progression Shop Purchase ({i+1})"] = AdvData(shop_offset + counter)
        counter += 1

    # spectral shop checks
    for i in range(4):
        spectral_shop[f"Spectral Shop Purchase ({i+1})"] = AdvData(shop_offset + counter)
        counter += 1

    # configuring harmonised base for gcq
    for key in standard_base:
        if key not in traveler:
            harmonised_base[key] = standard_base[key]

    # --- FISHSANITY --- #
    # one location per (species, quality) pair, kept fully separate from the quest-based
    # category_mapping dicts above - placed into regions directly in __init__.py, gated by
    # the fish_sanity option, so this never interacts with the harmonised_base filtering logic.
    counter = 0
    for tier, fish_list in FISH_ROSTER.items():
        for internal_id, display_name in fish_list:
            for quality in FISH_QUALITIES:
                title = f"{display_name} ({quality})"
                fish_sanity_categories[tier][title] = AdvData(fish_sanity_offset + counter)
                counter += 1


def assign_rod(name, title, item):
    for category, catches in rod_categories.items():
        if name in catches:
            category_mapping[category][title] = item
            break


# --- QUESTS --- #
gcq_easy = [
    "Catch Lake Fish", "Catch Ocean Fish"
]
gcq_normal = [
    "Catch Tiny/Microscopic Fish", "Catch Massive/Gigantic/Colossal Fish", "Catch Treasure Chests",
    "Catch Fish in the Rain"
]
gcq_hard = [
    "Catch High Tier Fish"
]
scq_normal = [
    "Sturgeon", "Catfish", "Koi", "Frog", "Turtle", "Toad", "Leech", "Eel", "Swordfish",
    "Hammerhead Shark", "Octopus", "Seahorse", "CREATURE"
]
scq_hard = [
    "Golden Ray", "Unidentified Fish Object", "Helicoprion", "Leedsichthys", "Golden Bass", "Bull Shark",
    "Manta Ray", "Gar", "Sawfish", "Muskellunge", "Axolotl", "Pupfish", "Mooneye", "Great White Shark", "Whale",
    "Coelacanth", "Alligator", "King Salmon", "Man O' War", "Sea Turtle", "Squid"
]
base_misc = [
    "Spectral Rib", "Spectral Skull", "Spectral Spine", "Spectral Humerus", "Spectral Femur"
]

# -- ROD CATEGORIES -- #
rod_categories = {
    "traveler": ["Catch Lake Fish", "Catch Ocean Fish", "Catch Tiny/Microscopic Fish",
                 "Catch Massive/Gigantic/Colossal Fish", "Catch Fish in the Rain"],
    "collector": ["Frog", "Seahorse", "Swordfish"],
    "shining": ["Catfish", "Koi", "Sturgeon", "Eel", "Octopus"],
    "glistening": ["Leech", "Turtle", "Toad", "Hammerhead Shark", "Sawfish"],
    "opulent": ["Gar", "King Salmon", "Muskellunge", "Man O' War", "Manta Ray", "Sea Turtle", "Squid"],
    "radiant": ["Axolotl", "Pupfish", "Mooneye", "Great White Shark"],
    "alpha": ["Whale", "Coelacanth", "Alligator", "Bull Shark"],
    "prosperous": ["Leedsichthys", "Golden Bass", "Golden Ray"],
    "spectral": ["Unidentified Fish Object", "Helicoprion", "CREATURE"]
}

# quests requiring respective rods
traveler = {}
collector = {}
shining = {}
glistening = {}
opulent = {}
radiant = {}
alpha = {}
prosperous = {}
spectral = {}

category_mapping = {
    "traveler": traveler,
    "collector": collector,
    "shining": shining,
    "glistening": glistening,
    "opulent": opulent,
    "radiant": radiant,
    "alpha": alpha,
    "prosperous": prosperous,
    "spectral": spectral
}

# sphere 1
standard_base = {}
harmonised_base = {}

scqe = {}  # specific catch quest easy - position depends on game mode
hard = {}  # soft requirement for lots of resources
hard_specific = {}  # same as hard, but toggleable
camp_2 = {}  # require 1 camp upgrade
camp_3 = {}  # require 2 camp upgrades
camp_4 = {}  # require all camp upgrades
spectral_shop = {}   # require at least one spectral bone

quest_offset: int = 94200
item_offset: int = 94700
shop_offset: int = 95200

# --- FISHSANITY --- #
# Internal ids match the "fish_*"/"wtrash_*" ids used by the client mod's harmonized loot
# tables (client/ArchipelagoClient/mods/mwmw.Archipelago/main.gd, _generate_alt_loot_tables)
# and the display names/tiers match loottables.md. "simple" is the junk pool caught on the
# starter Simple Rod (never gated behind an item, unlike every other tier) - Diamond lives
# in "prosperous" since it only shows up in that rod's loot table.
FISH_QUALITIES = ["Normal", "Shining", "Glistening", "Opulent", "Radiant", "Alpha"]

FISH_ROSTER = {
    "simple": [
        ("wtrash_bone", "Bone"), ("wtrash_boot", "Boot"), ("wtrash_branch", "Branch"),
        ("wtrash_drink_rings", "Drink Rings"), ("wtrash_plastic_bag", "Plastic Bag"),
        ("wtrash_sodacan", "Soda Can"), ("wtrash_weed", "Seaweed"),
    ],
    "traveler": [
        ("fish_lake_salmon", "Salmon"), ("fish_lake_bass", "Largemouth Bass"), ("fish_lake_carp", "Carp"),
        ("fish_lake_rainbowtrout", "Rainbow Trout"), ("fish_lake_bluegill", "Bluegill"), ("fish_lake_perch", "Perch"),
        ("fish_lake_walleye", "Walleye"), ("fish_lake_goldfish", "Goldfish"),
        ("fish_ocean_atlantic_salmon", "Atlantic Salmon"), ("fish_ocean_herring", "Herring"),
        ("fish_ocean_flounder", "Flounder"), ("fish_ocean_clownfish", "Clownfish"), ("fish_ocean_shrimp", "Shrimp"),
        ("fish_ocean_angelfish", "Angelfish"), ("fish_ocean_grouper", "Grouper"),
    ],
    "collector": [
        ("fish_lake_crayfish", "Crayfish"), ("fish_lake_drum", "Drum"), ("fish_lake_guppy", "Guppy"),
        ("fish_lake_snail", "Snail"), ("fish_lake_frog", "Frog"), ("fish_lake_crab", "Crab"),
        ("fish_ocean_krill", "Krill"), ("fish_ocean_oyster", "Oyster"), ("fish_ocean_bluefish", "Bluefish"),
        ("fish_ocean_lobster", "Lobster"), ("fish_ocean_tuna", "Tuna"), ("fish_ocean_seahorse", "Seahorse"),
        ("fish_ocean_sunfish", "Sunfish"), ("fish_ocean_swordfish", "Swordfish"),
    ],
    "shining": [
        ("fish_lake_catfish", "Catfish"), ("fish_lake_crappie", "Crappie"), ("fish_lake_pike", "Pike"),
        ("fish_lake_bowfin", "Bowfin"), ("fish_lake_koi", "Koi"), ("fish_lake_sturgeon", "Sturgeon"),
        ("fish_ocean_marlin", "Marlin"), ("fish_ocean_octopus", "Octopus"), ("fish_ocean_stingray", "Stingray"),
        ("fish_ocean_eel", "Eel"), ("fish_ocean_dogfish", "Dogfish"), ("fish_ocean_lionfish", "Lionfish"),
    ],
    "glistening": [
        ("fish_lake_leech", "Leech"), ("fish_lake_turtle", "Turtle"), ("fish_lake_toad", "Toad"),
        ("fish_ocean_sawfish", "Sawfish"), ("fish_ocean_wolffish", "Wolffish"),
        ("fish_ocean_hammerhead_shark", "Hammerhead Shark"),
    ],
    "opulent": [
        ("fish_lake_muskellunge", "Muskellunge"), ("fish_lake_kingsalmon", "King Salmon"), ("fish_lake_gar", "Gar"),
        ("fish_ocean_sea_turtle", "Sea Turtle"), ("fish_ocean_squid", "Squid"), ("fish_ocean_manowar", "Man O' War"),
        ("fish_ocean_manta_ray", "Manta Ray"),
    ],
    "radiant": [
        ("fish_lake_pupfish", "Pupfish"), ("fish_lake_axolotl", "Axolotl"), ("fish_lake_mooneye", "Mooneye"),
        ("fish_ocean_greatwhiteshark", "Great White Shark"),
    ],
    "alpha": [
        ("fish_lake_alligator", "Alligator"), ("fish_lake_bullshark", "Bullshark"),
        ("fish_ocean_whale", "Whale"), ("fish_ocean_coalacanth", "Coelacanth"),
    ],
    "prosperous": [
        ("fish_lake_golden_bass", "Golden Bass"), ("fish_ocean_golden_manta_ray", "Golden Manta Ray"),
        ("fish_rain_leedsichthys", "Leedsichthys"), ("wtrash_diamond", "Diamond"),
    ],
    "spectral": [
        ("fish_rain_anomalocaris", "Anomalocaris"), ("fish_rain_horseshoe_crab", "Horseshoe Crab"),
        ("fish_rain_heliocoprion", "Helicoprion"), ("fish_alien_dog", "UFO"), ("fish_void_voidfish", "CREATURE"),
    ],
}

fish_sanity_categories = {tier: {} for tier in FISH_ROSTER}
fish_sanity_offset: int = 96000

populate_advancement_tables()

fish_sanity_all = {}
for _tier_dict in fish_sanity_categories.values():
    fish_sanity_all |= _tier_dict

all_advancements = (standard_base | scqe | hard | hard_specific | camp_2 | camp_3 | camp_4 | spectral_shop |
                    fish_sanity_all)
