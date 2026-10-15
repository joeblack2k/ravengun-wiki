# Drakons: Realm Keepers

**Status:** Working (2026-10-14). Double-click in the RavenGun app starts the game under Wine, input comes through the `tp-shm` I/O bridge; played with the test pattern for more than 5 minutes (coin, START, world select, aim, shoot, CONTINUE). Not yet played with a real PS Move.

## 1. Platform and cabinet

- Adrenaline Amusements PC-based cabinet, Windows, 64-bit (`Is64Bit = true`).
- Executable: `Game.exe` (the profile identifies it by name and file size, so your dump must match the version RavenGun was tested with).
- Light gun game with a world-select screen and CONTINUE prompts.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- A Windows environment: RavenGun runs it under Wine (`[Launch] Mode = direct`, no TeknoParrotUi).
- RavenGun provides the cabinet hardware the game expects.
- Light gun input as shared-memory board image (see section 5).
- Graphics: nothing special is set in the profile; no DXVK key is needed according to the profile (**INFERRED**: the `[Launch]` section only has `Mode = direct`).

## 3. The official start script, or why there is none

On the cabinet the game is started by the cabinet's own PC image; there is no start script you would run on a desktop PC. RavenGun starts `Game.exe` itself (the app calls the daemon, which runs the Wine route). See [Official-Start-Scripts](Official-Start-Scripts) for how that differs per platform and [Loader-Architecture](Loader-Architecture) for the route.

## 4. The route we use

Profile `DrakonsRealmKeepers`, `Type = TeknoParrot` (the loader family), emulation profile `WartranTroopers`.

```ini
[Launch]
Mode = direct

[Input]
Route = tp-shm
Layout = WartranTroopers
```

- **MEASURED** (2026-10-14): double-click in the app, no TeknoParrotUi, Wine, `tp-shm` bridge with the `WartranTroopers` layout.
- The loader template for this game is called `Drakons`, not `DrakonsRealmKeepers`; the profile name in RavenGun differs from the template name (**INFERRED** from the profile comment). If you re-import profiles with the RavenGun tools, this is why the mapping is by hand.
- Profile values worth knowing: `General/Input API = RawInput`, `General/Windowed = 0`, `General/HideCursor = 1`, `General/Use Relative Input = 0`, player relative sensitivity 8, `FFB Blaster/Enable = 0`.

## 5. Input

The `WartranTroopers` layout is the four-player shooter layout shared by many Windows PC-based titles (control word at offset 8 with test, service, coins, per-player start, trigger, reload, grenade, extra button; one byte per aim axis from offset 12, left/top = 0).

- Coin: key `5`. START: key `1` (keys the RavenGun input daemon reads; a PS Move button or mouse button does the same).
- Aim and trigger: from the PS Move, a mouse (mouse-gun mode) or a controller. **MEASURED** with the test pattern: aiming and shooting worked.
- Calibration: none was needed in the measured run.

## 6. Timing

- Boot to attract: not measured separately.
- Played: more than 5 minutes (attract plus a game up to CONTINUE and a score of 400). **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

Attract, coin and START, world selection, the shooting stage with aim and trigger responding, a CONTINUE screen and a final score of 400. No error dialogs were recorded.

## 8. Current state and open questions

- Open: playing with a real PS Move (only the test pattern was used).
- Open: player 2 and the extra buttons were not exercised.
- Nothing known to be broken.

## 9. What we tried and what did not work

Not measured yet beyond the working route. The route was prepared from the recipe of another Windows PC-based title (the shared-memory layout `WartranTroopers`) and worked on the first real start.

## 10. What is Linux-specific, and what differs on Windows

- On Windows the original loader's UI starts the game and writes the input state itself; on Linux the RavenGun daemon writes the shared board image and starts the game without that UI.
- Wine runs the 64-bit game; the cabinet's own PC image is not needed.
- Everything else (coin and START keys) is a RavenGun convention rather than a game feature.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
