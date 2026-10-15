# NERF Arcade

**Status:** Working (2026-10-14). Native Linux: the game's own Unity player `Nerf.x86_64` runs on RavenGun's own loader, started by a double-click in the app. The light gun board (RIO) answers through the RIO bridge: START, aim and trigger work (mouse, score 12,050). Not tested: player 2.

## 1. Platform and cabinet

- Raw Thrills PC-based cabinet; the game is a Unity 2018.2.21 player for Linux (ELF 64-bit, game version file "Nerf 1.55").
- Your game folder may contain two builds: the original Linux build (`Nerf.x86_64`) and a Windows conversion (`Nerf.exe`). RavenGun uses the Linux one.
- Light gun board: Raw Thrills "RIO" USB board (the game loads `librio.so` and `libRIO2.so`).
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- The cabinet layout: the game expects its folder at `/pm`; RavenGun mounts your game folder there with a local write layer, so nothing is written to your game folder.
- The game's native plug-ins must be at `Nerf_Data/Plugins/x86_64`. In the dump they sit in `x86_64_ori`; RavenGun mounts that folder at the expected place. **MEASURED:** without it, `DllNotFoundException: UnityNatives` and `rio`, hundreds of thousands of log lines, a broken HUD. Side effect: Unity loads each plug-in twice.
- A udev rules file `/etc/udev/rules.d/10-usb-automount.rules` (two lines the game itself would write; RavenGun provides it from `patches/NERF/data/udev-rules.d`). **MEASURED:** without it `Game.Awake()` dies on an access exception and the game half-works.
- gamescope: without it the game cannot open a display in the sandbox ("Authorization required").
- RavenGun provides the cabinet hardware the game expects.

## 3. The official start script, or why there is none

On the cabinet the Raw Thrills OS starts the game (`go.sh`, `xinit`, `run_game.sh`; the run script is not in a typical dump). RavenGun does not use them: the engine starts `Nerf.x86_64` itself inside a sandbox with gamescope. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Profile = NERF
Executable = Nerf.exe      ; legacy field from the Windows route

[Input]
Route = tp-shm
Layout = WartranTroopers
```

- Native route entry (`packaging/native-games.json`): `arch = x86_64`, `launcher = gamescope`, executable `/pm/Nerf.x86_64`, working directory and home `/pm`, preload `librg_rio_bridge.so`, environment `RG_RIO_LOG = 1`.
- **MEASURED** (2026-10-14): no Wine, no loader core and no plug-in loader in the process; `/proc/<pid>/maps` shows none of them.
- Settings the game saved in the dump (`LocalData/testmenu/prefs`, free play) are used. What the game writes lands in the local write layer under `~/.local/share/ravengun/native/NERF/`.
- The earlier Windows route (Wine, DXVK, a plug-in loader) is no longer needed.

## 5. Input

The game reads its board by polling RIO library functions (`RIO_Connected`, `RIO_SW_Count`, `RIO_ADC_Val`, `RIO_ADC_Val_Ex`). RavenGun's **RIO bridge** is preloaded and answers those functions from the daemon's board image (layout `WartranTroopers`; table `patches/NERF/rio-invoer.ini`).

**MEASURED switch ids:** 7 = player 1 START, 8 = player 2 start, 15 = player 1 trigger (shots score; 0 to 4,500 points on that id only), 3 = TEST (held opens the operator menu), 5/6 = volume. Lightgun channels 19/20 = P1 X/Y, 21/22 = P2 X/Y, range 0..4095; Y is inverted (board 0 = bottom).

- START: key `1` or the Move's START button. Coin: key `5` (free play is on).
- Right mouse button (reload in the daemon) also starts, for mouse players; NERF has no reload.
- Player 2's firing id is not measured (16 and 17 are candidates), so a second gun joins but does not shoot yet.
- Calibration: the guns are calibrated in the game's own operator menu (TEST); the result is saved in the local write layer.

## 6. Timing

- Attract ran 12 min 46 s untouched on the native route. **MEASURED.**
- Game log: "Game booted up" about 20 seconds after launch.
- Playing: mouse run, score 12,050. Length of the play session not recorded here.

## 7. What we saw on screen

Raw Thrills logo, NERF ARCADE title, Hasbro notice, the "Nerf Masters" score table, a warning screen and all four levels in turn (graveyard, drone hangar, army base, zombie lagoon) with moving targets; "Free Play, Press Start!" for players 1 and 2. Before the bridge existed a red "RIO DISCONNECTED" banner was on every frame; it is gone.

## 8. Current state and open questions

- Not tested: player 2.
- The particle plug-in does not load (`libbfd-2.28-system.so` is missing on SteamOS), so some effects are missing; a stub library would let it load. Not tried.
- The resolution dialog plug-in (`ScreenSelector.so`, GTK 2) does not load; nothing asks for it.
- Sound was not judged.

## 9. What we tried and what did not work

- No gamescope: display authorisation error.
- No udev rules file: grey screens and thousands of exceptions per minute.
- Removing the plug-in mount: broken HUD, huge log.
- The Windows conversion on Wine worked too (about 5 min of attract and play with START and five aimed shots), but is replaced by the native route.

## 10. What is Linux-specific, and what differs on Windows

- The game is a native Linux program; the cabinet OS is replaced by a sandbox with the `/pm` layout, two mounts, a udev file, gamescope and the RIO bridge.
- Same RIO board as [Jurassic-Park-Arcade](Jurassic-Park-Arcade), answered by the same bridge; only the attachment differs (polled functions here, USB events there).
- On Windows the conversion runs the Windows player on a plug-in loader; none of that is used here.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
