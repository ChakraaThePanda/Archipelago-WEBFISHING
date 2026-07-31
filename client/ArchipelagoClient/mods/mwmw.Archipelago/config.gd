extends Node

const LOCKED_ITEMS = {
	"Crickets License": null,
	"Leeches License": null,
	"Minnows License": null,
	"Squid License": null,
	"Nautiluses License": null,
	"Gilded Worm License": null,
	"Rod Power 1": null,
	"Rod Power 2": null,
	"Rod Power 3": null,
	"Rod Power 4": null,
	"Rod Power 5": null,
	"Rod Power 6": null,
	"Rod Power 7": null,
	"Rod Power 8": null,
	"Rod Speed 1": null,
	"Rod Speed 2": null,
	"Rod Speed 3": null,
	"Rod Speed 4": null,
	"Rod Speed 5": null,
	"Rod Chance 1": null,
	"Rod Chance 2": null,
	"Rod Chance 3": null,
	"Rod Chance 4": null,
	"Rod Chance 5": null,
	"Tacklebox Upgrade 1": null,
	"Tacklebox Upgrade 2": null,
	"Tacklebox Upgrade 3": null,
	"Tacklebox Upgrade 4": null,
	"Tacklebox Upgrade 5": null,
	"Tacklebox Upgrade 6": null,
	"Tacklebox Upgrade 7": null,
	"Tacklebox Upgrade 8": null,
	"Tacklebox Upgrade 9": null,
	"Buddy Quality Upgrade 1": null,
	"Buddy Quality Upgrade 2": null,
	"Buddy Quality Upgrade 3": null,
	"Buddy Quality Upgrade 4": null,
	"Buddy Quality Upgrade 5": null,
	"Buddy Speed Upgrade 1": null,
	"Buddy Speed Upgrade 2": null,
	"Buddy Speed Upgrade 3": null,
	"Buddy Speed Upgrade 4": null,
	"Buddy Speed Upgrade 5": null,
	"Rod Luck 1": null,
	"Rod Luck 2": null,
	"Rod Luck 3": null,
	"Rod Luck 4": null,
	"Rod Luck 5": null,
	"Fly Hook": null,
	"Lucky Hook": null,
	"Patient Lure": null,
	"Quick Jig": null,
	"Salty Lure": null,
	"Fresh Lure": null,
	"Efficient Lure": null,
	"Magnet Lure": null,
	"Large Lure": null,
	"Attractive Angler": null,
	"Sparkling Lure": null,
	"Double Hook": null,
	"Golden Hook": null,
	"Challenge Lure": null,
	"Shower Lure": null,
	"Collector's Fishing Rod": null,
	"Shining Collector's Fishing Rod": null,
	"Glistening Collector's Fishing Rod": null,
	"Opulent Collector's Fishing Rod": null,
	"Radiant Collector's Fishing Rod": null,
	"Alpha Collector's Fishing Rod": null,
	"Prosperous Fishing Rod": null,
	"Traveler's Fishing Rod": null
}

const SHOP_ID = {
	"t1_1": 95200,
	"t1_2": 95201,
	"t1_3": 95202,
	"t1_4": 95203,
	"t1_5": 95204,
	"t1_6": 95205,
	"t1_7": 95206,
	"t1_8": 95207,
	"t2_9": 95208,
	"t2_10": 95209,
	"t2_11": 95210,
	"t2_12": 95211,
	"t2_13": 95212,
	"t2_14": 95213,
	"t2_15": 95214,
	"t2_16": 95215,
	"t3_17": 95216,
	"t3_18": 95217,
	"t3_19": 95218,
	"t3_20": 95219,
	"t3_21": 95220,
	"t3_22": 95221,
	"t3_23": 95222,
	"t3_24": 95223,
	"t4_25": 95224,
	"t4_26": 95225,
	"t4_27": 95226,
	"t4_28": 95227,
	"t4_29": 95228,
	"t4_30": 95229,
	"t4_31": 95230,
	"t4_32": 95231,
	"s_1": 95232,
	"s_2": 95233,
	"s_3": 95234,
	"s_4": 95235
}


const ALT_FREE_ITEMS = {
	"fishing_rod_simple": null,
}

# Fishsanity: one location per (species, quality) pair. Quality index order must match
# PlayerData.ITEM_QUALITIES (Normal, Shining, Glistening, Opulent, Radiant, Alpha).
# This table is generated from worlds/webfishing/locations.py's FISH_ROSTER/FISH_QUALITIES -
# keep both in sync if either changes.
const FISH_QUALITIES = ["Normal", "Shining", "Glistening", "Opulent", "Radiant", "Alpha"]

const FISH_SANITY_ID = {
	"wtrash_bone": [96000, 96001, 96002, 96003, 96004, 96005],
	"wtrash_boot": [96006, 96007, 96008, 96009, 96010, 96011],
	"wtrash_branch": [96012, 96013, 96014, 96015, 96016, 96017],
	"wtrash_drink_rings": [96018, 96019, 96020, 96021, 96022, 96023],
	"wtrash_plastic_bag": [96024, 96025, 96026, 96027, 96028, 96029],
	"wtrash_sodacan": [96030, 96031, 96032, 96033, 96034, 96035],
	"wtrash_weed": [96036, 96037, 96038, 96039, 96040, 96041],
	"fish_lake_salmon": [96042, 96043, 96044, 96045, 96046, 96047],
	"fish_lake_bass": [96048, 96049, 96050, 96051, 96052, 96053],
	"fish_lake_carp": [96054, 96055, 96056, 96057, 96058, 96059],
	"fish_lake_rainbowtrout": [96060, 96061, 96062, 96063, 96064, 96065],
	"fish_lake_bluegill": [96066, 96067, 96068, 96069, 96070, 96071],
	"fish_lake_perch": [96072, 96073, 96074, 96075, 96076, 96077],
	"fish_lake_walleye": [96078, 96079, 96080, 96081, 96082, 96083],
	"fish_lake_goldfish": [96084, 96085, 96086, 96087, 96088, 96089],
	"fish_ocean_atlantic_salmon": [96090, 96091, 96092, 96093, 96094, 96095],
	"fish_ocean_herring": [96096, 96097, 96098, 96099, 96100, 96101],
	"fish_ocean_flounder": [96102, 96103, 96104, 96105, 96106, 96107],
	"fish_ocean_clownfish": [96108, 96109, 96110, 96111, 96112, 96113],
	"fish_ocean_shrimp": [96114, 96115, 96116, 96117, 96118, 96119],
	"fish_ocean_angelfish": [96120, 96121, 96122, 96123, 96124, 96125],
	"fish_ocean_grouper": [96126, 96127, 96128, 96129, 96130, 96131],
	"fish_lake_crayfish": [96132, 96133, 96134, 96135, 96136, 96137],
	"fish_lake_drum": [96138, 96139, 96140, 96141, 96142, 96143],
	"fish_lake_guppy": [96144, 96145, 96146, 96147, 96148, 96149],
	"fish_lake_snail": [96150, 96151, 96152, 96153, 96154, 96155],
	"fish_lake_frog": [96156, 96157, 96158, 96159, 96160, 96161],
	"fish_lake_crab": [96162, 96163, 96164, 96165, 96166, 96167],
	"fish_ocean_krill": [96168, 96169, 96170, 96171, 96172, 96173],
	"fish_ocean_oyster": [96174, 96175, 96176, 96177, 96178, 96179],
	"fish_ocean_bluefish": [96180, 96181, 96182, 96183, 96184, 96185],
	"fish_ocean_lobster": [96186, 96187, 96188, 96189, 96190, 96191],
	"fish_ocean_tuna": [96192, 96193, 96194, 96195, 96196, 96197],
	"fish_ocean_seahorse": [96198, 96199, 96200, 96201, 96202, 96203],
	"fish_ocean_sunfish": [96204, 96205, 96206, 96207, 96208, 96209],
	"fish_ocean_swordfish": [96210, 96211, 96212, 96213, 96214, 96215],
	"fish_lake_catfish": [96216, 96217, 96218, 96219, 96220, 96221],
	"fish_lake_crappie": [96222, 96223, 96224, 96225, 96226, 96227],
	"fish_lake_pike": [96228, 96229, 96230, 96231, 96232, 96233],
	"fish_lake_bowfin": [96234, 96235, 96236, 96237, 96238, 96239],
	"fish_lake_koi": [96240, 96241, 96242, 96243, 96244, 96245],
	"fish_lake_sturgeon": [96246, 96247, 96248, 96249, 96250, 96251],
	"fish_ocean_marlin": [96252, 96253, 96254, 96255, 96256, 96257],
	"fish_ocean_octopus": [96258, 96259, 96260, 96261, 96262, 96263],
	"fish_ocean_stingray": [96264, 96265, 96266, 96267, 96268, 96269],
	"fish_ocean_eel": [96270, 96271, 96272, 96273, 96274, 96275],
	"fish_ocean_dogfish": [96276, 96277, 96278, 96279, 96280, 96281],
	"fish_ocean_lionfish": [96282, 96283, 96284, 96285, 96286, 96287],
	"fish_lake_leech": [96288, 96289, 96290, 96291, 96292, 96293],
	"fish_lake_turtle": [96294, 96295, 96296, 96297, 96298, 96299],
	"fish_lake_toad": [96300, 96301, 96302, 96303, 96304, 96305],
	"fish_ocean_sawfish": [96306, 96307, 96308, 96309, 96310, 96311],
	"fish_ocean_wolffish": [96312, 96313, 96314, 96315, 96316, 96317],
	"fish_ocean_hammerhead_shark": [96318, 96319, 96320, 96321, 96322, 96323],
	"fish_lake_muskellunge": [96324, 96325, 96326, 96327, 96328, 96329],
	"fish_lake_kingsalmon": [96330, 96331, 96332, 96333, 96334, 96335],
	"fish_lake_gar": [96336, 96337, 96338, 96339, 96340, 96341],
	"fish_ocean_sea_turtle": [96342, 96343, 96344, 96345, 96346, 96347],
	"fish_ocean_squid": [96348, 96349, 96350, 96351, 96352, 96353],
	"fish_ocean_manowar": [96354, 96355, 96356, 96357, 96358, 96359],
	"fish_ocean_manta_ray": [96360, 96361, 96362, 96363, 96364, 96365],
	"fish_lake_pupfish": [96366, 96367, 96368, 96369, 96370, 96371],
	"fish_lake_axolotl": [96372, 96373, 96374, 96375, 96376, 96377],
	"fish_lake_mooneye": [96378, 96379, 96380, 96381, 96382, 96383],
	"fish_ocean_greatwhiteshark": [96384, 96385, 96386, 96387, 96388, 96389],
	"fish_lake_alligator": [96390, 96391, 96392, 96393, 96394, 96395],
	"fish_lake_bullshark": [96396, 96397, 96398, 96399, 96400, 96401],
	"fish_ocean_whale": [96402, 96403, 96404, 96405, 96406, 96407],
	"fish_ocean_coalacanth": [96408, 96409, 96410, 96411, 96412, 96413],
	"fish_lake_golden_bass": [96414, 96415, 96416, 96417, 96418, 96419],
	"fish_ocean_golden_manta_ray": [96420, 96421, 96422, 96423, 96424, 96425],
	"fish_rain_leedsichthys": [96426, 96427, 96428, 96429, 96430, 96431],
	"wtrash_diamond": [96432, 96433, 96434, 96435, 96436, 96437],
	"fish_rain_anomalocaris": [96438, 96439, 96440, 96441, 96442, 96443],
	"fish_rain_horseshoe_crab": [96444, 96445, 96446, 96447, 96448, 96449],
	"fish_rain_heliocoprion": [96450, 96451, 96452, 96453, 96454, 96455],
	"fish_alien_dog": [96456, 96457, 96458, 96459, 96460, 96461],
	"fish_void_voidfish": [96462, 96463, 96464, 96465, 96466, 96467],
}

const PLAYER_COLOURS = [
	"[color=#a2ffee]",
	"[color=#ffbff2]",
	"[color=#e7caff]",
	"[color=#95ff95]",
	"[color=#ffc8c8]",
	"[color=#cdd1ff]",
	"[color=#ffff98]"
]

const ITEM_COLOURS = [
	"[color=#acfaf9]",  # common/junk
	"[color=#f5d7ff]",  # important/progression
	"[color=#d4deff]",  # rare/useful
	"[color=#d57272]",  # filler (unused by ap)
	"[color=#d57272]",  # trap
]

const TEXT_COLOUR = "[color=#effffe]"

const LOCATION_COLOUR = "[color=#a8ffd3]"

enum Goal {
	TOTAL_COMPLETION,
	RANK,
	COMPLETED_CAMP
}

enum Gamemode {
	CLASSIC,
	ALT
}

# current goal (and also mode) indicate that the ap is active if they are not null
var mode = null
var current_goal = null
var rank_goal = null
var total_completion_goal = null
var chance_eq = null
var auto_hint = null
var fish_sanity = null
