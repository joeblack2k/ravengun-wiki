# Mars Sortie

**Status:** Working (2026-10-15). Double-click in the app starts the game under Wine with DXVK in gamescope; attract, coin, START and a full game; played 5.5 minutes. After a game with a score of 10 or more a reward screen follows: hold the trigger for 5 seconds to continue (it is not a hang).

## 1. Platform and cabinet

- UDC PC-based cabinet, Windows, 64-bit, executable `Shooter.exe`.
- Light gun shooter for up to four players (four relative-sensitivity settings in the profile).
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine with **DXVK** (Direct3D 11 on Vulkan). **MEASURED:** without it the picture stayed black, also in gamescope; with DXVK v2.7.1 attract and game are visible.
- A plug-in loader (BepInEx through the `winhttp.dll` override) that the game's Windows conversion uses; the profile sets `DllOverrides = winhttp=n,b;d3d11,d3d10core,dxgi=n,b`.
- RavenGun provides the cabinet hardware the game expects.
- Writable record files: see section 4.

## 3. The official start script, or why there is none

On the cabinet the PC starts the game from its own boot setup. RavenGun starts `Shooter.exe` itself with no script: [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Launch]
Mode = direct
Dxvk = true
ViewCopies = GameRecords1.dat, GameRecords2.dat

[Wine]
Prefix = ravengun-test-dxvk
DllOverrides = winhttp=n,b;d3d11,d3d10core,dxgi=n,b
Runner = wrapper

[Display]
Gamescope = true

[Input]
Route = tp-shm
Layout = WartranTroopers
```

- **`ViewCopies`:** the game rewrites `GameRecords1.dat` and `GameRecords2.dat` next to the executable at every start. RavenGun's view normally links your files; for these two it makes local copies, so your game folder is never written (**MEASURED:** without it the files got a new modification time every start).
- Profile values: `General/Windowed = 0`, `General/HideCursor = 1`, `General/DisplayCrosshair = 1`, `General/CustomCrosshairs = 1`, `General/CustomWebcamPicture = 1`, resolution 1920x1080 (custom resolution off).

## 5. Input

- Layout `WartranTroopers`. Coin: key `5`. START: key `1`. **MEASURED** (2026-10-15): coin, START and shooting work.
- Aim and trigger from PS Move, mouse or controller.
- **Reward screen:** after a game with score >= 10 (`ScoreOfReward = 10` in the game's records) hold the trigger for 5 seconds. **MEASURED.**

## 6. Timing

- Boot to attract: not measured separately.
- Played: 5.5 minutes. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

Black screen without DXVK; with DXVK attract, coin, START, a game and then the reward screen.

## 8. Current state and open questions

- Open: real PS Move, players 2 to 4, the webcam picture option.
- Nothing known to be broken.

## 9. What we tried and what did not work

- Without DXVK: a black picture (also with gamescope).
- Direct links to the records files: the game's writes would touch your game folder; replaced by `ViewCopies`.

## 10. What is Linux-specific, and what differs on Windows

- DXVK replaces the Windows Direct3D 11 driver; the `winhttp` override loads the plug-in loader under Wine.
- Local record copies protect your game folder; on a real cabinet the files live on the cabinet's disk.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
