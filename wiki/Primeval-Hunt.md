# Primeval Hunt

**Status:** Working (2026-10-15). Runs natively on Linux through RavenGun's Lindbergh route; coin, START, shooting and reloading were played for 5.5 minutes. The touch screen is deliberately absent.

## 1. Platform and cabinet

- SEGA Lindbergh Red, a Linux PC board. The game (`prog/main.exe`) is a 32-bit Linux ELF despite the `.exe` name (**MEASURED**).
- The original cabinet has a gun screen plus a touch screen on which the player chooses a destination.

## 2. What the game needs

- Your own dump of the game folder; RavenGun ships no games.
- `lindbergh.so` from the open-source lindbergh-loader, built on your machine by RavenGun's build script (it is not shipped).
- 32-bit (i386) support libraries that SteamOS lacks; the build step stages them.
- RavenGun provides the cabinet hardware the game expects (baseboard, I/O board, flash) in software.
- Mesa OpenGL through zink (Vulkan).

## 3. The official start script, or why there is none

On the cabinet the game is started by the Lindbergh system. lindbergh-loader has its own starter; RavenGun does not use it: the RavenGun engine sets everything the starter would.

## 4. The route we use

**MEASURED** 2026-10-15: double-click in the app. The engine launches `main.exe` with `LD_PRELOAD=lindbergh.so`, with the JVS line of the baseboard handed to the daemon's board. The profile:

```ini
[Game]
Type = Lindbergh
[Input]
Route = jvs
Board = Lindbergh
```

`lindbergh.ini` settings that matter:

```ini
[Display]
KEEP_ASPECT_RATIO = true
HIDE_CURSOR = true
[Input]
INPUT_MODE = 1
[Emulation]
REGION = EX
FREEPLAY = none
[Graphics]
GPU_VENDOR = 2
[GameSpecific]
PRIMEVAL_HUNT_SCREEN_MODE = 1
```

- `GPU_VENDOR = 2` is needed because zink reports `GL_VENDOR` as "Mesa", which the layer would not recognise.
- `PRIMEVAL_HUNT_SCREEN_MODE = 1` shows only the game screen, without the touch screen beside it.
- Your own `lindbergh.ini` in the user layer of the game's patch folder wins over the shipped one.
- Display size comes from the engine (640x480 for this title), not from the ini.

## 5. Input

The daemon is the cabinet's JVS I/O board (board `Lindbergh`, a Type 3 gun board: 2 players, 14 switch bits, 8 analog channels). Channels 0..3 are P1 X, P1 Y, P2 X, P2 Y.

| Action | Mouse mode |
|---|---|
| coin | 5 |
| START | 1 |
| shoot | trigger |
| reload | aim off the screen (or the reload button) |
| gun button | BUTTON_3 (used by this game) |

Calibrate the guns in the game's test menu (TEST) if the crosshair drifts; the EEPROM lives in a local write layer.

## 6. Timing

- **MEASURED:** played 5.5 minutes in mouse mode (coin, START, shooting, reloading).
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

Attract loop, coin and START, play with shooting and reloading. The destination choice normally made on the touch screen does not appear; when its timer runs out the game picks a destination itself.

## 8. Current state and open questions

- Touch screen: deliberately absent, no input route for it.
- Real Move controller and two-player play are not recorded for this title.

## 9. What we tried and what did not work

- The first starts needed extra 32-bit libraries (libXt, libSM, libICE, libbsd, libmd) that SteamOS lacks; they now come from the build container.
- Without `GPU_VENDOR = 2` the layer does not recognise the GPU under zink.

## 10. What is Linux-specific, and what differs on Windows

This is a Linux-native game: there is no Windows version of this route. The whole route (lindbergh-loader, JVS pass-through to the daemon, zink for OpenGL) exists only on Linux. On radeonsi instead of zink remove the two `MESA_LOADER_DRIVER_OVERRIDE`/`LIBGL_KOPPER_DRI2` environment settings from the profile.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
