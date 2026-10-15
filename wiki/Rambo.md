# Rambo

**Status:** Working (2026-10-15). Runs natively on Linux through RavenGun's Lindbergh route: double-click, coin, START, shooting and reloading, 5.5 minutes played in mouse mode.

## 1. Platform and cabinet

- SEGA Lindbergh (Type 3 board), Linux PC. The game ELF is `elf/ramboM.elf` (32-bit i386, about 5.1 MB). The template profile also names `ramboD.elf`; RavenGun starts `ramboM.elf` and refuses any other ELF (**MEASURED**: `ramboD.elf` has a game ID the Lindbergh layer does not know).
- Two-player gun cabinet with a gun/grenade button.

## 2. What the game needs

- Your own dump of the game folder; RavenGun ships no games.
- `lindbergh.so` from the open-source lindbergh-loader, built locally by RavenGun's build script (not shipped), plus `libCg.so` 2.0 so the Cg shaders can be recompiled on Mesa.
- 32-bit support libraries that SteamOS lacks (built into the layer by the build container).
- RavenGun provides the cabinet hardware the game expects (baseboard, I/O board, flash) in software.

## 3. The official start script, or why there is none

The cabinet boots the ELF from its own Linux system. lindbergh-loader's starter is not used; RavenGun's engine does its job.

## 4. The route we use

**MEASURED** 2026-10-15: no TeknoParrot, no Wine, no shell chain.

```ini
[Game]
Type = Lindbergh
Executable = ramboD.elf   ; profile name only; the engine starts elf/ramboM.elf
[Input]
Route = jvs
Board = Lindbergh
```

`lindbergh.ini`: `INPUT_MODE = 1`, `REGION = EX`, `FREEPLAY = none` (coins come from the daemon), `KEEP_ASPECT_RATIO = true`, `HIDE_CURSOR = true`, `GPU_VENDOR = 2`. Display size is set by the engine (1280x768). OpenGL runs through Mesa zink on RADV; remove `MESA_LOADER_DRIVER_OVERRIDE` and `LIBGL_KOPPER_DRI2` from the profile to use radeonsi instead. If the game sees only one gun, `RAMBO_GUNS_SWITCH` in `lindbergh.ini` is the knob to try.

## 5. Input

The daemon plays the cabinet's JVS board (2 players, 14 switches, 8 analog channels). Mouse mode:

| Action | Key / gesture |
|---|---|
| coin | 5 |
| START | 1 |
| shoot | trigger |
| reload | aim beside the screen (offscreen) |
| gun button | BUTTON_3 / grenade |

Use the game's test menu (TEST) to calibrate the guns if the crosshair is off.

## 6. Timing

- Played 5.5 minutes in mouse mode (**MEASURED**).
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

Attract, coin and START, shooting, reloading by aiming off screen.

## 8. Current state and open questions

- Real Move and two-player play are not recorded.
- The template's `ramboD` entry versus the real `ramboM` start is a naming quirk of the shared TeknoParrot profile.

## 9. What we tried and what did not work

Starting `ramboD.elf` is not supported (unknown game ID). Missing 32-bit libraries (`libXt`, `libSM`, `libICE`, `libbsd`, `libmd`) had to be added to the layer.

## 10. What is Linux-specific, and what differs on Windows

This route exists only on Linux; on Windows the title runs through TeknoParrot's own Lindbergh emulation. Here the ELF runs on the host with a preloaded layer and Mesa zink.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
