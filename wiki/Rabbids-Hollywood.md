# Rabbids Hollywood Arcade

**Status:** Working (2026-10-14). A double-click in the RavenGun app starts the game under Proton with a RavenGun plug-in inside it, input over a local TCP connection. Measured on the TV in mouse mode: coin, START, aim and trigger, a played round, 5 min 19 s. An earlier headless run held 10 min 8 s.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Adrenaline Amusements "PC Based" cabinet. This is a PC title: the cabinet runs ordinary Windows and the game is a **64-bit Unity 2017 (Mono)** program. Lightgun game for up to four players. **MEASURED** from the folder.
- TeknoParrot template `GameProfiles/RabbidsHollywood.xml` revision 6, emulation profile `WartranTroopers`, `Executable = Game.exe`.
- The game reads its aim as a **mouse position in its own window** (screen pixels, Y origin at the bottom). The screen shows "Insert credits" per player, coins count in quarters ("1/4 credits").
- The game is multilingual; RavenGun sets English (`language = EN` in its Unity game list) and the title screen comes up in English.

## 2. What the game needs

- Your own dump: about 2.0 GB, 1,788 files, `Game.exe` (650,752 bytes), `UnityPlayer.dll`, `Game_Data/` (1.9 GB). No file is empty and nothing else is needed (no drive letters, no extra asset folder). **MEASURED.**
- The folder name on the original install ends with a **trailing space** (`Rabbids Hollywood `). Wine rejects that with `Directory name invalid (0x10B)`, so RavenGun starts the game from a local view of links. If you copy the folder yourself, rename it without the space.
- The folder already has a doorstop plug-in loader (`BepInEx/`, `doorstop_config.ini`, `winhttp.dll`); RavenGun uses its own clean BepInEx 5.4.21.0 in the view instead.
- Proton (GE-Proton with DXVK) and gamescope. The cabinet's hardware checks are answered by RavenGun's plug-in; you do not need to provide anything.
- Write nothing into your game folder: small config files (`*.json`, `*.conf`, `*.cfg` under 64 KiB) and flag files (`Game.run`, `ForceReboot`) are copied into the view because the game writes to them. **MEASURED:** in a ten-minute run all writes landed in the view.

## 3. The official start script, or why there is none

There is no `game.bat` for this title: the folder has no `.bat` or `.cmd`. It has `GameLauncher.exe` and an operator tool with a `.conf` and a read-me; these are cabinet tooling (**INFERRED**, not run). `Game.exe` starts directly. See [Official Start Scripts](Official-Start-Scripts) for why RavenGun reads cabinet scripts and takes over only the arguments and paths instead of running them.

## 4. The route we use

No injected loader core: `Game.exe` runs directly under Proton, and only a managed plug-in enters the process, loaded through the doorstop. **MEASURED.**

```ini
[Game]
Type = TeknoParrot
EmulationProfile = WartranTroopers
Executable = Game.exe
[Loader]
PostStartMs = 3000
[Wine]
DllOverrides = winhttp=n,b
[Input]
Route = unity-tcp
```

- Command: `proton run Game.exe -popupwindow` (borderless full screen) from a local view, with `WINEDLLOVERRIDES=winhttp=n,b`. **The override is required**: without it Wine does not load the doorstop `winhttp.dll` and no plug-in gets in.
- Inside the game: BepInEx 5.4.21.0 plus the RavenGun plug-in `RavenGun.RabbidsHollywood.dll`. The plug-in is the TCP **server** on `127.0.0.1:33610`, the RavenGun engine is the client (one client at a time).
- Resolution is set by the plug-in (`FORCE_RESOLUTION=1`, `WIDTH=1920`, `HEIGHT=1080`, `FULLSCREEN=1`), not by an argument.
- Own Wine prefix per route (`~/.local/share/ravengun/prefixes/unity-aagames`, ~30 s to build the first time); do not share it with other titles, the doorstop override should not leak.
- The profile's `[Loader] PostStartMs = 3000` waits 3 s after the game starts before the engine connects.
- A TeknoParrot route (OpenParrot loader) also exists as fallback; it parked because the game never opened the I/O pipe. **MEASURED.**

## 5. Input

The wire protocol (`unity-tcp`, all little-endian, no header, fields in alphabetical order) **MEASURED** byte for byte:

Engine to plug-in, 38 bytes per packet: `Axis_X float32[4]` (offset 0, screen pixels 0..width-1), `Axis_Y float32[4]` (offset 16, Y origin at the bottom), `EnableInputsHack u8` (offset 32, must be 1, otherwise the plug-in falls back to mouse and keyboard), `HideCrosshairs u8` (33), `Trigger u8[4]` (34..37). There is **no Reload field** in this game. If your aim is `v` from the top (0..1), send `Axis_Y = (1 - v) * (height - 1)`. Packets go out at a fixed 120 per second.

Plug-in to engine: `int32` length (61), a type byte (2) and 60 bytes: `Ammo i32[4]`, `Credits i32[4]`, `Damaged u8[4]`, `Life float32[4]`, `Recoil u8[4]` (a one-shot flag: this message is a shot), `StartLamp u8[4]` (last in this game).

Keys in the app: **5** = coin player 1 (6/7/8 for players 2-4), **1** = START player 1 (2/3/4), **0** = test, Esc = quit, left mouse button = trigger. Four coins and START gave `credits 2 -> 3 -> 4`, then `playing 1` and the coin consumed. **MEASURED.** A tested aim of `u=0.3, v=0.3` put the crosshair at 576/324 pixels from the top left. START needs to be held briefly (key 1).

Players 2-4 are supported by the protocol and the game, but only player 1 was exercised.

## 6. Timing

- Unit start to `Game.exe` visible: 3 s in one run, about 16 s in another (cold vs. warm prefix and view). Say which one you measure. **MEASURED.**
- `Game.exe` to coins and START accepted: about 78 s in the ten-minute run. **INFERRED.**
- Headless run, 2026-10-12: 608 s of play, the game still alive at the stop, 115 threads, 120 packets/s on all 20 checks, nothing written to the share. **MEASURED.**
- Double-click run on the TV, 2026-10-14: 5 min 19 s with a played round. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

**MEASURED** on the TV: title screen in English, "Insert credits" per player, then after four coins and START the loading screen, then the game with a crosshair, a weapon and a health bar. In the headless run the state machine ran menu, demo, play, death, back to attract (`OnDemoStateExit`, `OnMenuStateEnter`, `OnDemoStateEnter`), health `100 -> 44 -> 35 -> 25 -> 15 -> 4 -> -6`.

## 8. Current state and open questions

- Working via double-click (2026-10-14), played with mouse mode.
- Not yet measured: playing with the real PS Move buttons and vibration; players 2-4; sound and frame rate.
- Open: the game's saved status (metrics, operator menu, options) is treated as invalid and reset at every start; the cause is not established. Whether a savegame survives two starts is not measured.

## 9. What we tried and what did not work

- **A game that "shuts itself down" after 50 to 70 s** was an old plug-in in the view (32,768 bytes) that lacked a needed answer; the fresh one (34,304 bytes) lived 288 s and later 608 s. Compare size and checksum of what is in the view with what you built, not timestamps.
- **A second diagnostic TCP client next to the engine**: the plug-in keeps one client, so connects and disconnects alternated. Use the engine's own test pattern.
- **Virtual keys sent to the session compositor** did not reach a headless gamescope game; sending to gamescope's own Xwayland (`DISPLAY=:1 xdotool key ...`) worked.
- **Drop-ins on this route**: the Unity start path does not read `dropin.ini`, and `Game_Data` in the view is a folder of links to the share, so placing a file there would write to the share. Not used.
- Time measurements without cold/warm, and instrumented against uninstrumented runs, were not comparable.

## 10. What is Linux-specific, and what differs on Windows

- `WINEDLLOVERRIDES=winhttp=n,b` is needed on Linux; on Windows `winhttp.dll` next to the executable just works.
- The trailing-space folder name is fatal under Wine but fine on Windows; the local view solves it.
- The gun is a virtual absolute mouse (`uinput`, vendor 1209, product 7202; players 2-4 use 7203..7205) plus a virtual keyboard (product `72f0`) for coin, START and test. Keep them invisible to the desktop with `LIBINPUT_IGNORE_DEVICE`, or the desktop cursor moves while you play. A udev rule for `uinput` access is needed; Steam's own rule covers hidraw for the Move.
- Gamescope gives the game its own Xwayland display; a headless run has no picture to judge.
- A per-game user layer `~/.local/share/ravengun/patches/<Game>/game.ini` overrides shipped keys one by one.
- On Windows you would need a virtual input driver instead of `uinput`.

See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
