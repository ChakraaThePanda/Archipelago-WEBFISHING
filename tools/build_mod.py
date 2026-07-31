"""
Packages the built client mod into mwmw.Archipelago.zip for a release.

Expects two things to already be built:
1. The C# GDWeave patches, via:
       dotnet build -c Release client/mwmw.Archipelago/mwmw.Archipelago -p:GDWeavePath=<...>
   producing client/mwmw.Archipelago/mwmw.Archipelago/bin/Release/net8.0/{manifest.json,
   mwmw.Archipelago.dll, mwmw.Archipelago.deps.json, mwmw.Archipelago.pdb}
2. The Godot resource pack, via the Godot 3.5.2 editor exporting client/ArchipelagoClient/'s
   "Windows Desktop" preset (the export preset's export_path already points to
   client/ArchipelagoClient/mwmw.Archipelago.pck)

Usage:
    python tools/build_mod.py

Produces ./mwmw.Archipelago.zip (gitignored release artifact) containing a single
mwmw.Archipelago/ folder - extract that folder straight into GDWeave/mods/.
"""
from __future__ import annotations

import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DLL_BUILD_DIR = ROOT / "client" / "mwmw.Archipelago" / "mwmw.Archipelago" / "bin" / "Release" / "net8.0"
PCK_PATH = ROOT / "client" / "ArchipelagoClient" / "mwmw.Archipelago.pck"
OUTPUT = ROOT / "mwmw.Archipelago.zip"

DLL_BUILD_FILES = ["manifest.json", "mwmw.Archipelago.dll", "mwmw.Archipelago.deps.json", "mwmw.Archipelago.pdb"]

missing = [DLL_BUILD_DIR / name for name in DLL_BUILD_FILES if not (DLL_BUILD_DIR / name).is_file()]
if not PCK_PATH.is_file():
    missing.append(PCK_PATH)
if missing:
    raise SystemExit("Missing build output, see this script's docstring for how to produce it:\n" +
                     "\n".join(f"  {path}" for path in missing))

OUTPUT.unlink(missing_ok=True)
with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name in DLL_BUILD_FILES:
        zf.write(DLL_BUILD_DIR / name, pathlib.Path("mwmw.Archipelago") / name)
    zf.write(PCK_PATH, "mwmw.Archipelago/mwmw.Archipelago.pck")

print(f"Built {OUTPUT} ({OUTPUT.stat().st_size} bytes)")
