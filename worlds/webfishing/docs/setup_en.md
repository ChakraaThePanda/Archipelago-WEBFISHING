# WEBFISHING Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- [WEBFISHING](https://store.steampowered.com/app/3146520/WEBFISHING/) (Steam)

## Installation

1. Find your WEBFISHING install folder: Steam -> right-click WEBFISHING -> **Manage** ->
   **Browse local files**.
2. Download [GDWeave](https://github.com/NotNite/GDWeave/releases/latest/download/GDWeave.zip)
   and extract it there -- you'll end up with a `GDWeave` folder and `winmm.dll` next to
   `webfishing.exe`.
3. Download the [Archipelago mod](https://github.com/ChakraaThePanda/Archipelago-WEBFISHING/releases/latest/download/mwmw.Archipelago.zip)
   and extract the `mwmw.Archipelago` folder into `GDWeave/mods/`.
4. Download the [apworld](https://github.com/ChakraaThePanda/Archipelago-WEBFISHING/releases/latest/download/webfishing.apworld)
   into your Archipelago install's `custom_worlds` folder.
5. Download the [YAML template](https://github.com/ChakraaThePanda/Archipelago-WEBFISHING/releases/latest/download/WEBFISHING.yaml)
   into your Archipelago `Players` folder and configure it to your liking.
6. Generate or join a multiworld using your YAML.

## Connecting

1. Launch WEBFISHING through Steam.
2. Load into a game, open the Esc menu, and click **Archipelago**.
3. Enter your server address, slot name, and password (if any), then connect.

## Notes

- Use a fresh save per Archipelago world/slot -- checks already sent from the wrong save
  cannot be undone.
- If you lose connection, the client tries to notify you; you can also confirm the connection
  is alive by sending a message in local chat.
- See [`en_WEBFISHING.md`](en_WEBFISHING.md) for what randomization actually changes about the
  game, and [`loottables.md`](loottables.md) for Harmonized mode's per-rod fish groupings.
