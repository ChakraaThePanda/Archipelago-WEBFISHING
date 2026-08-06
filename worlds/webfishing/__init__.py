import settings
from typing import Dict, Any
from .options import WebfishingOptions
from .items import (WebfishingItem, WebfishingItemData, item_table, fixed_quantities, rods, filler_weights)
from .locations import (WebfishingAdvancement, standard_base, harmonised_base, scqe, hard, hard_specific, camp_2,
                        camp_3, camp_4, all_advancements, traveler, collector, shining, glistening, opulent, radiant,
                        alpha, prosperous, spectral, spectral_shop, fish_sanity_categories, fish_sanity_all,
                        FISH_QUALITIES)
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from BaseClasses import Region, Item, Tutorial
from Utils import visualize_regions


class WebfishingWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up WEBFISHING for Archipelago multiworld play.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Miyowi", "ChakraaThePanda"],
    )]


class WebfishingWorld(World):
    """WEBFISHING is a multiplayer chatroom-focused fishing game! Relax and fish (on the web!)"""

    game = "WEBFISHING"
    web = WebfishingWeb()
    options_dataclass = WebfishingOptions  # options the player can set
    options: WebfishingOptions  # typing hints for option results
    # settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = False  # show path to required location checks in spoiler

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in all_advancements.items()}

    def _fish_sanity_locations(self, tier, region):
        # Quality tiers beyond Normal are gated by which bait you've unlocked (bait N
        # guarantees/enables quality N: worms=Normal, cricket=Shining, leech=Glistening,
        # minnow=Opulent, squid=Radiant, nautilus/gildedworm=Alpha) - this applies
        # uniformly regardless of tier, including "simple" junk items.
        # Shining and up also need Progressive Rod Power to actually land the fight:
        # 1/2/3 for Shining/Glistening/Opulent, then a steeper 5/7 for Radiant/Alpha -
        # out of 8 total in the pool. Radiant and Alpha intentionally sit above the 5
        # the Hard region entrance already demands, so landing them isn't guaranteed
        # by logic even though it's technically possible with the full item pool.
        rod_power_by_quality = [0, 1, 2, 3, 5, 7]
        locs = []
        for loc_name, loc_data in fish_sanity_categories[tier].items():
            loc = WebfishingAdvancement(self.player, loc_name, loc_data.id, region)
            quality = loc_name.rsplit(" (", 1)[1][:-1]
            quality_index = FISH_QUALITIES.index(quality)
            if quality_index > 0:
                rod_power = rod_power_by_quality[quality_index]
                set_rule(loc, lambda state, q=quality_index, p=rod_power:
                         state.has("Progressive Bait", self.player, q) and
                         state.has("Progressive Rod Power", self.player, p))
            locs.append(loc)
        return locs

    def create_regions(self) -> None:

        match self.options.game_mode.value:

            # Classic mode
            case 0:
                menu_region = Region("Menu", self.player, self.multiworld)

                # Base (no items needed)
                base_region = Region("Base", self.player, self.multiworld)
                base_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, base_region)
                                          for loc_name, loc_data in (standard_base | scqe).items()]

                # Medium (some progression items needed for time)
                medium_region = Region("Medium", self.player, self.multiworld)
                # medium_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, medium_region)
                #                            for loc_name, loc_data in medium.items()]

                # Hard (lots of progression items needed for time)
                hard_region = Region("Hard", self.player, self.multiworld)
                hard_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, hard_region)
                                          for loc_name, loc_data in hard.items()]

                # HardSpecific (same as hard, but can have all checks toggled off)
                hard_specific_region = Region("Hard Specific", self.player, self.multiworld)
                if bool(self.options.rare_fish_checks.value):
                    hard_specific_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                             hard_specific_region) for
                                                       loc_name, loc_data in
                                                       hard_specific.items()]

                # Camp2 (needs one progressive camp upgrade)
                camp_2_region = Region("Camp 2", self.player, self.multiworld)
                camp_2_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, camp_2_region)
                                            for loc_name, loc_data in camp_2.items()]

                # Camp3 (needs two progressive camp upgrades)
                camp_3_region = Region("Camp 3", self.player, self.multiworld)
                camp_3_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, camp_3_region)
                                            for loc_name, loc_data in camp_3.items()]

                # Camp4 (needs two progressive camp upgrades)
                camp_4_region = Region("Camp 4", self.player, self.multiworld)
                camp_4_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, camp_4_region)
                                            for loc_name, loc_data in camp_4.items()]

                # Spectral Shop (needs one spectral bone)
                spectral_shop_region = Region("Spectral Shop", self.player, self.multiworld)
                spectral_shop_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                         spectral_shop_region)
                                                   for loc_name, loc_data in spectral_shop.items()]

                # Fishsanity (first catch of every fish x quality, tucked into difficulty-equivalent regions
                # since Classic mode has no rod-specific regions to slot them into)
                if bool(self.options.fish_sanity.value):
                    for tier in ("simple", "traveler", "collector"):
                        base_region.locations += self._fish_sanity_locations(tier, base_region)
                    for tier in ("shining", "glistening"):
                        medium_region.locations += self._fish_sanity_locations(tier, medium_region)
                    for tier in ("opulent", "radiant", "alpha", "prosperous", "spectral"):
                        hard_region.locations += self._fish_sanity_locations(tier, hard_region)

                self.multiworld.regions += [menu_region, base_region, medium_region, hard_region, hard_specific_region,
                                            camp_2_region, camp_3_region, camp_4_region, spectral_shop_region]

                menu_region.connect(base_region)
                base_region.add_exits({"Medium": "Some Upgrades", "Camp 2": "Progressive Camp 1",
                                       "Spectral Shop": "Spectral Bone"})
                medium_region.add_exits({"Hard": "Upgrade Abundance", "Camp 3": "Progressive Camp 2"})
                hard_region.add_exits({"Camp 4": "Progressive Camp 3"})
                hard_region.connect(hard_specific_region)

            # Harmonized mode
            case 1:
                menu_region = Region("Menu", self.player, self.multiworld)

                # Base (no items needed)
                base_region = Region("Base", self.player, self.multiworld)
                base_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, base_region)
                                          for loc_name, loc_data in harmonised_base.items()]

                # Medium (some progression items needed for time)
                medium_region = Region("Medium", self.player, self.multiworld)

                # Collector (fish found with the standard collector rod)
                traveler_region = Region("Traveler", self.player, self.multiworld)
                traveler_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                    traveler_region) for loc_name, loc_data in
                                              traveler.items()]

                # Hard (lots of progression items needed for time)
                hard_region = Region("Hard", self.player, self.multiworld)
                hard_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, hard_region)
                                          for loc_name, loc_data in hard.items()]

                # Collector (fish found with the standard collector rod)
                collector_region = Region("Collector", self.player, self.multiworld)
                collector_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                     collector_region) for loc_name, loc_data in
                                               collector.items()]

                # Shining (fish found with the shining rod)
                shining_region = Region("Shining", self.player, self.multiworld)
                shining_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                   shining_region) for loc_name, loc_data in
                                             shining.items()]

                # Glistening (fish found with the glistening rod)
                glistening_region = Region("Glistening", self.player, self.multiworld)
                glistening_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                      glistening_region) for loc_name, loc_data in
                                                glistening.items()]

                # Opulent (fish found with the opulent rod)
                opulent_region = Region("Opulent", self.player, self.multiworld)
                opulent_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                   opulent_region) for loc_name, loc_data in
                                             opulent.items()]

                # Radiant (fish found with the radiant rod)
                radiant_region = Region("Radiant", self.player, self.multiworld)
                radiant_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                   radiant_region) for loc_name, loc_data in
                                             radiant.items()]

                # Alpha (fish found with the alpha rod)
                alpha_region = Region("Alpha", self.player, self.multiworld)
                alpha_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                 alpha_region) for loc_name, loc_data in
                                           alpha.items()]

                # Prosperous (fish found with the prosperous rod)
                prosperous_region = Region("Prosperous", self.player, self.multiworld)
                prosperous_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                      prosperous_region) for loc_name, loc_data in
                                                prosperous.items()]

                # Spectral (fish found with the spectral rod)
                spectral_region = Region("Spectral", self.player, self.multiworld)
                spectral_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                    spectral_region) for loc_name, loc_data in
                                              spectral.items()]

                # Camp2 (needs one progressive camp upgrade)
                camp_2_region = Region("Camp 2", self.player, self.multiworld)
                camp_2_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, camp_2_region)
                                            for loc_name, loc_data in camp_2.items()]

                # Camp3 (needs two progressive camp upgrades)
                camp_3_region = Region("Camp 3", self.player, self.multiworld)
                camp_3_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, camp_3_region)
                                            for loc_name, loc_data in camp_3.items()]

                # Camp4 (needs two progressive camp upgrades)
                camp_4_region = Region("Camp 4", self.player, self.multiworld)
                camp_4_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id, camp_4_region)
                                            for loc_name, loc_data in camp_4.items()]

                # Spectral Shop (needs one spectral bone)
                spectral_shop_region = Region("Spectral Shop", self.player, self.multiworld)
                spectral_shop_region.locations += [WebfishingAdvancement(self.player, loc_name, loc_data.id,
                                                                         spectral_shop_region)
                                                   for loc_name, loc_data in spectral_shop.items()]

                # Fishsanity (first catch of every fish x quality, one tier per rod region -
                # except "simple", which is the starter rod's junk pool and needs no item at all)
                if bool(self.options.fish_sanity.value):
                    base_region.locations += self._fish_sanity_locations("simple", base_region)

                    for tier, region in (("traveler", traveler_region), ("collector", collector_region),
                                        ("shining", shining_region), ("glistening", glistening_region),
                                        ("opulent", opulent_region), ("radiant", radiant_region),
                                        ("alpha", alpha_region), ("prosperous", prosperous_region),
                                        ("spectral", spectral_region)):
                        region.locations += self._fish_sanity_locations(tier, region)

                self.multiworld.regions += [menu_region, base_region, traveler_region, medium_region, hard_region,
                                            collector_region, shining_region, glistening_region, opulent_region,
                                            radiant_region, alpha_region, prosperous_region, spectral_region,
                                            camp_2_region, camp_3_region, camp_4_region, spectral_shop_region]

                menu_region.connect(base_region)
                base_region.add_exits({"Medium": "Some Upgrades", "Camp 2": "Progressive Camp 1",
                                       "Spectral Shop": "Spectral Bone", "Traveler": "Traveler's Rod"})
                medium_region.add_exits({"Hard": "Upgrade Abundance", "Camp 3": "Progressive Camp 2",
                                         "Collector": "Collector Rod", "Shining": "Shining Rod",
                                         "Glistening": "Glistening Rod", "Spectral": "Spectral Bones"})
                hard_region.add_exits({"Camp 4": "Progressive Camp 3", "Opulent": "Opulent Rod",
                                       "Radiant": "Radiant Rod", "Alpha": "Alpha Rod", "Prosperous": "Prosperous Rod"})

    def set_rules(self) -> None:

        upgrade_abundance = lambda state: state.has("Progressive Bait", self.player, 6) and \
                                          state.has("Progressive Rod Power", self.player, 5) and \
                                          state.has("Progressive Tacklebox Upgrade", self.player, 2) and \
                                          state.has("Progressive Rod Speed", self.player, 3) and \
                                          state.has("Progressive Rod Luck", self.player, 3) and \
                                          state.has("Magnet Lure", self.player) and \
                                          state.has("Golden Hook", self.player) and \
                                          state.has("Shower Lure", self.player) and \
                                          state.has("Sparkling Lure", self.player) and \
                                          state.has("Large Lure", self.player) and \
                                          state.has("Fly Hook", self.player)

        spectral_bones = lambda state: state.has("Spectral Rib", self.player) and \
                                       state.has("Spectral Skull", self.player) and \
                                       state.has("Spectral Spine", self.player) and \
                                       state.has("Spectral Humerus", self.player) and \
                                       state.has("Spectral Femur", self.player)

        # Standard & Harmonized
        set_rule(self.multiworld.get_entrance("Some Upgrades", self.player),
                 lambda state: state.has("Progressive Bait", self.player, 3) and
                               state.has("Progressive Rod Power", self.player, 2) and
                               state.has("Progressive Tacklebox Upgrade", self.player, 1) and
                               state.has("Progressive Rod Speed", self.player, 1) and
                               state.has("Progressive Rod Luck", self.player, 1))

        set_rule(self.multiworld.get_entrance("Upgrade Abundance", self.player),
                 upgrade_abundance)

        set_rule(self.multiworld.get_entrance("Progressive Camp 1", self.player),
                 lambda state: state.has("Progressive Camp Tier Unlock", self.player, 1))

        set_rule(self.multiworld.get_entrance("Progressive Camp 2", self.player),
                 lambda state: state.has("Progressive Camp Tier Unlock", self.player, 2))

        set_rule(self.multiworld.get_entrance("Progressive Camp 3", self.player),
                 lambda state: state.has("Progressive Camp Tier Unlock", self.player, 3))

        set_rule(self.multiworld.get_entrance("Spectral Bone", self.player),
                 lambda state: state.has("Spectral Rib", self.player) or
                               state.has("Spectral Skull", self.player) or
                               state.has("Spectral Spine", self.player) or
                               state.has("Spectral Humerus", self.player) or
                               state.has("Spectral Femur", self.player))

        # Harmonized mode only
        if self.options.game_mode.value == 1:
            set_rule(self.multiworld.get_entrance("Traveler's Rod", self.player),
                     lambda state: state.has("Traveler's Rod", self.player))

            set_rule(self.multiworld.get_entrance("Collector Rod", self.player),
                     lambda state: state.has("Collector's Rod", self.player))

            set_rule(self.multiworld.get_entrance("Shining Rod", self.player),
                     lambda state: state.has("Shining Collector's Rod", self.player))

            set_rule(self.multiworld.get_entrance("Glistening Rod", self.player),
                     lambda state: state.has("Glistening Collector's Rod", self.player))

            set_rule(self.multiworld.get_entrance("Spectral Bones", self.player), spectral_bones)

            set_rule(self.multiworld.get_entrance("Opulent Rod", self.player),
                     lambda state: state.has("Opulent Collector's Rod", self.player))

            set_rule(self.multiworld.get_entrance("Radiant Rod", self.player),
                     lambda state: state.has("Radiant Collector's Rod", self.player))

            set_rule(self.multiworld.get_entrance("Alpha Rod", self.player),
                     lambda state: state.has("Alpha Collector's Rod", self.player))

            set_rule(self.multiworld.get_entrance("Prosperous Rod", self.player),
                     lambda state: state.has("Prosperous Rod", self.player))

            self.multiworld.completion_condition[self.player] = upgrade_abundance and spectral_bones and (
                lambda state: state.has("Traveler's Rod", self.player) and
                              state.has("Collector's Rod", self.player) and
                              state.has("Shining Collector's Rod", self.player) and
                              state.has("Glistening Collector's Rod", self.player) and
                              state.has("Opulent Collector's Rod", self.player) and
                              state.has("Radiant Collector's Rod", self.player) and
                              state.has("Alpha Collector's Rod", self.player) and
                              state.has("Prosperous Rod", self.player)
            )

        # Standard complete condition
        else:
            self.multiworld.completion_condition[self.player] = upgrade_abundance

        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml",
        #                   show_entrance_names=True, show_other_regions=True)

    def create_items(self) -> None:
        # guaranteed items regardless of gamemode
        for name, quantity in fixed_quantities.items():
            for i in range(quantity):
                item = self.create_item(name)
                self.multiworld.itempool.append(item)

        # items only in harmonized
        if self.options.game_mode.value == 1:
            for name in rods.keys():
                item = self.create_item(name)
                self.multiworld.itempool.append(item)

        # filling in remaining slots with junk
        # (counted from the locations actually placed into regions this seed, not the static
        # all_advancements total, since hard_specific/fish_sanity are conditional on options)
        placed_locations = len(standard_base) + len(scqe) + len(hard) + len(camp_2) + len(camp_3) + \
                           len(camp_4) + len(spectral_shop)
        # rare_fish_checks only gates Hard Specific in Classic mode - Harmonized always places these
        # via their rod-tier regions regardless of the toggle
        if self.options.game_mode.value == 1 or bool(self.options.rare_fish_checks.value):
            placed_locations += len(hard_specific)
        if bool(self.options.fish_sanity.value):
            placed_locations += len(fish_sanity_all)

        filler_quantity = placed_locations - sum(fixed_quantities.values())
        if self.options.game_mode.value == 1:
            filler_quantity -= sum(rods.values())

        for _ in range(filler_quantity):
            name = self.random.choices(list(filler_weights.keys()), weights=list(filler_weights.values()))[0]
            item = self.create_item(name)
            self.multiworld.itempool.append(item)

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = WebfishingItem(name, item_data.item_type, item_data.code, self.player)
        return item

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict("goal", "total_completion", "rank", "game_mode", "rare_fish_checks",
                                    "fish_chance_equalizer", "auto_hint", "fish_sanity")
