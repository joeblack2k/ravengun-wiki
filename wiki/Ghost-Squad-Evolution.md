# Ghost Squad Evolution

**Status:** Working (2026-10-15). Native Linux on the Lindbergh route: double-click in the app, the game's own 32-bit ELF with `lindbergh.so` from lindbergh-loader, a Type 1 JVS board from RavenGun's daemon, OpenGL on Vulkan (Mesa zink). Played 5.5 minutes in mouse mode (coin, START, shooting, reloading). The aim window is not calibrated yet.

## 1. Platform and cabinet

- SEGA Lindbergh Red; the game is a 32-bit Linux ELF (`vsg_l/vsg` in your game folder).
- Older **Type 1** JVS I/O board (837-13551 style): 2 players, 13 switch bits, 8-bit analog axes.
- RavenGun ships no games: you need your own copy of the game folder (a dump of the cabinet's game disk).

## 2. What the game needs

- The cabinet hardware that a Lindbergh game expects (baseboard, I/O, configuration chips, system libraries): RavenGun provides it through `lindbergh.so`, which is lindbergh-loader's `LD_PRELOAD` library.
- lindbergh-loader is not shipped with RavenGun (its licence differs from RavenGun's). A build script builds it on your own machine into `~/.local/share/ravengun/lindbergh-loader/current`; it needs a container tool for the 32-bit build.
- 32-bit libraries that SteamOS does not have are provided by RavenGun (`lib32`).
- Game ID known to lindbergh-loader: `0x455edaec`, entry "GSEvo (DVP-0029A)" (**INFERRED** from the loader's table).
- The game's shaders are old ARB programs; lindbergh-loader patches them for Mesa (**INFERRED**, no libCg needed).

## 3. The official start script, or why there is none

On the cabinet the game is started by the cabinet's boot scripts, which also bring up the baseboard drivers. RavenGun does not use them: the app starts the ELF itself inside a sandbox, with `lindbergh.so` preloaded. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = Lindbergh
EmulationProfile = GSEVO
Executable = vsg

[Input]
Route = jvs
Board = LindberghType1
```

- Process chain (**MEASURED**): gamescope, sandbox, game ELF; `lindbergh.so` hands the baseboard's JVS packets to a pseudo-terminal of the RavenGun daemon (`/dev/ttyRG0` inside the sandbox). The daemon is the board `LindberghType1`.
- Graphics (**MEASURED**): OpenGL on Vulkan through Mesa zink on an AMD GPU; the launch resolution in the profile is 640x480. Removing the zink environment variables falls back to plain radeonsi.
- `lindbergh.ini` (in `patches/GSEVO/`; a copy in your user layer wins): `KEEP_ASPECT_RATIO = true`, `HIDE_CURSOR = true`, `INPUT_MODE = 1`, `REGION = EX`, `FREEPLAY = none` (coins come from the daemon), `GPU_VENDOR = 2` (zink reports vendor "Mesa"; 2 keeps the AMD path), `DEBUG_MSGS = false`. RavenGun sets width, height, fullscreen and the JVS path itself at every start.

## 5. Input

- Coin: key `5`. START: key `1`. Shooting and reloading work (**MEASURED** in mouse mode).
- Reload is `BUTTON_2`; the loader sets it when the gun points off screen (an off-screen shot reloads).
- Axes: channels 0-3 are P1 X, P1 Y, P2 X, P2 Y, not inverted (0 = left/top).
- Calibration: the aim window is not calibrated yet; the game has its own test menu (settings are kept in the local write layer).

## 6. Timing

- Boot to attract: not measured separately.
- Played: 5.5 minutes in mouse mode. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

Attract, coin and START, gameplay with shots and reloads. A real aim check (crosshair against the gun) was not made.

## 8. Current state and open questions

- Open: aim window calibration.
- Open: real PS Move, player 2.
- Open: sound and frame pacing not judged.

## 9. What we tried and what did not work

Not measured yet beyond the working route.

## 10. What is Linux-specific, and what differs on Windows

- The game is a native Linux program; there is no Windows version. What changes is that the cabinet hardware is replaced by a preload library and the Type 1 board by the RavenGun daemon.
- Other Lindbergh titles on RavenGun use the Type 3 board; this one uses Type 1.
- See also [Lets-Go-Jungle](Lets-Go-Jungle) and [Lets-Go-Jungle-Special](Lets-Go-Jungle-Special) for the same route.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
