# Pull The Trigger

**Status:** Working (2026-10-15). A double-click in RavenGun starts the game directly under Wine/Proton; it was played for 5.5 minutes in mouse mode (coin, shoot to start, reload, chapters, bonus select). An earlier black screen did not come back.

## 1. Platform and cabinet

- COVIELSA PC-based lightgun cabinet; Windows executable `PTW.exe` (about 835 KB). **INFERRED** from the profile.
- Two-player lightgun layout. RavenGun uses the TeknoParrot profile `PullTheTrigger` (revision 5) as a template.

## 2. What the game needs

- Your own copy of the game folder; RavenGun ships no games.
- Wine/Proton with DXVK (the profile uses the shared test prefix `ravengun-test-dxvk`) and gamescope.
- The cabinet's I/O is emulated by RavenGun's I/O bridge.

## 3. The official start script, or why there is none

No start script. On Windows the game is normally started through TeknoParrot. RavenGun starts it itself (`rg-direct`), without TeknoParrotUi.

## 4. The route we use

**MEASURED** 2026-10-15:

```ini
[Launch]
Mode = direct

[Wine]
Prefix = ravengun-test-dxvk
Runner = wrapper

[Display]
Gamescope = true
GamescopePath = /usr/bin/gamescope

[Input]
Route = tp-shm
Layout = RawThrillsGUN
```

Template `[Config]` values worth knowing: `General/Windowed = 1`, `General/HideCursor = 1`, `General/ResolutionWidth = 640`, `General/ResolutionHeight = 480`, `General/CabinetID = 1`, `Network/HostIp = 192.168.1.150` (a placeholder LAN address; the game does not need a network), crosshair and force feedback off.

## 5. Input

Layout `RawThrillsGUN`: test, service, coin 1/2, then per player (two) start, trigger, grenade, reload; volume up/down. Aim is one byte per axis, left/top = 0.

Mouse mode: coin = 5, START = 1. Observed in play: shooting starts a game, and the on-screen reload prompt is **PULL BACK / RELEASE**, which the reload action performs.

## 6. Timing

- Played 5.5 minutes (**MEASURED**).
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

Coin accepted, "shoot to start", reload prompts (PULL BACK/RELEASE), chapter selection and a bonus selection. The game window is 4:3-ish (640x480 template).

## 8. Current state and open questions

- Real Move controller and a second player were not recorded.
- Sound was not judged in the recorded run.

## 9. What we tried and what did not work

An earlier attempt gave a **black screen**. The cause is not documented in the sources; the current route (rg-direct with DXVK prefix) did not show it again in the 2026-10-15 run.

## 10. What is Linux-specific, and what differs on Windows

On Windows you would start the game with TeknoParrot. On Linux RavenGun does the launch itself: Wine wrapper, DXVK (Vulkan), gamescope, and the `tp-shm` input bridge fed by Move, mouse or gamepad.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
