# Wild West Shootout

**Status:** Working (2026-10-15). Starts from a double-click under Wine with DXVK (Vulkan) and a BepInEx plugin for input; coin, START, shooting and an end boss were played for 5.5 minutes in mouse mode.

## 1. Platform and cabinet

- Coastal PC-based cabinet; a Unity 5.6 game (Direct3D 11) with `CowBoy.exe` (about 18 MB).
- Template profile: TeknoParrot `WildWestShootout` (revision 2), input layout `WartranTroopers`.

## 2. What the game needs

- Your own game folder; RavenGun ships no games.
- Wine/Proton with DXVK. Without DXVK and without BepInEx the window never appeared (**MEASURED**, 2026-10-15).
- BepInEx (doorstop `winhttp.dll` in the game folder), which loads the TeknoParrot input plug-in "WWS 1.4".

## 3. The official start script, or why there is none

None. RavenGun starts the game directly (`rg-direct`).

## 4. The route we use

**MEASURED** 2026-10-15:

```ini
[Launch]
Mode = direct
Dxvk = true

[Wine]
DllOverrides = winhttp=n,b

[Input]
Route = tp-shm
Layout = WartranTroopers
```

Template `[Config]`: `General/Windowed = 0`, `General/HideCursor = 1`, `General/ResolutionWidth = 1920`, `General/ResolutionHeight = 1080`, `General/Input API = RawInput`.

## 5. Input

The plug-in reads the `WartranTroopers` layout through `tp-shm`: test, service, coins, per-player start, trigger, reload, grenade and an extra button; aim is one byte per axis. Mouse mode: coin = 5, START = 1, shoot with the trigger. **MEASURED:** coin, START and shooting work.

## 6. Timing

- Played 5.5 minutes (**MEASURED**): up to the end boss.
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

Coin, START, shooting through the levels, and the end boss.

## 8. Current state and open questions

- Real Move and second player not recorded.
- Sound not judged.

## 9. What we tried and what did not work

Without DXVK and without `winhttp=n,b` (BepInEx) the game window never showed up.

## 10. What is Linux-specific, and what differs on Windows

On Windows the game runs through TeknoParrot. On Linux, DXVK translates Direct3D 11 to Vulkan, the `winhttp` override loads BepInEx, and the plug-in reads the `tp-shm` input bridge.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
