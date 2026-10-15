# Let's Go Jungle: Lost on the Island of Spice

**Status:** Working (2026-10-15). Native Linux on the Lindbergh route: double-click in the app, `lgj_final` (Rev A) with `lindbergh.so` and `librg-stackalign.so`, JVS through RavenGun's daemon after passthrough fix 0003. Played 5.5 minutes in mouse mode (coin, START, shooting).

## 1. Platform and cabinet

- SEGA Lindbergh Red; the game is a 32-bit Linux ELF (`lgj_final` in your game folder).
- On-rails light gun game on the standard Lindbergh Type 3 style I/O board.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- The cabinet hardware a Lindbergh game expects: RavenGun provides it through `lindbergh.so` (lindbergh-loader, built on your own machine by RavenGun's build script into `~/.local/share/ravengun/lindbergh-loader/current`; it is not shipped).
- `librg-stackalign.so`: RavenGun's small preload library that aligns the stack; the game needs it on Mesa.
- Cg shader library `libCg.so` 2.0, recompiled shaders for Mesa (`libcg = true` in the route entry), 32-bit system libraries from RavenGun's `lib32`.
- Game ID in lindbergh-loader: `0xc697c4fb`. Launch resolution 1360x768.

## 3. The official start script, or why there is none

The cabinet boots straight into the game. RavenGun starts the ELF itself in a sandbox with gamescope, with `lindbergh.so` and `librg-stackalign.so` in `LD_PRELOAD`. lindbergh-loader's own starter is not used. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = ElfLdr2        ; legacy field; the app uses the native Lindbergh route entry
EmulationProfile = SegaJvsLetsGoJungle

[Input]
Route = jvs
Board = Lindbergh
```

- Route entry: `arch = i386`, `launcher = gamescope`, `jvs = passthrough`, `stackalign = true`, OpenGL via Mesa zink (`MESA_LOADER_DRIVER_OVERRIDE = zink`, `LIBGL_KOPPER_DRI2 = 1`).
- **Passthrough fix 0003 (MEASURED):** the game waits 1 second for a reply to its JVS packets; the fix makes the baseboard layer pass the packets to the daemon and return the reply in time.
- `lindbergh.ini` in `patches/LGJ/`: `KEEP_ASPECT_RATIO = true`, `HIDE_CURSOR = true`, `INPUT_MODE = 1`, `REGION = EX`, `FREEPLAY = none`, `GPU_VENDOR = 2`. RavenGun sets width, height, fullscreen and the JVS path at each start; your own `lindbergh.ini` in the user layer wins.

## 5. Input

- Coin: key `5`. START: key `1`. Shooting by mouse or PS Move. **MEASURED** in mouse mode.
- Board `Lindbergh`: channels 0-3 = P1 X, P1 Y, P2 X, P2 Y (0 = left/top, not inverted). Trigger = `BUTTON_1`, reload = `BUTTON_2`, which fires when the gun points beside the screen.
- The game calibrates itself in its test menu; the settings live in the local write layer.

## 6. Timing

- Boot to attract: not measured separately.
- Played: 5.5 minutes. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

Attract, a coin and START, then shooting. Contact sheets of the run exist on the bench; no graphics faults are recorded.

## 8. Current state and open questions

- Open: real PS Move, player 2, sound, aim calibration check.
- Profile note: "not yet measured" in the route entry for the parts beyond the 5.5-minute run.

## 9. What we tried and what did not work

- The game waits 1 second for a reply to its I/O packets, which needed passthrough fix 0003; the fix is part of the route now. Details of the failure without it were not recorded.

## 10. What is Linux-specific, and what differs on Windows

- There is no Windows version: the game is a Linux program and the cabinet hardware is replaced by a preload library and the daemon's board.
- Related titles on the same route: [Lets-Go-Jungle-Special](Lets-Go-Jungle-Special), [Ghost-Squad-Evolution](Ghost-Squad-Evolution).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
