# The House of the Dead 4 Special

**Status:** Not working yet. It runs through the ride-reset and more than 5 minutes of attract, but coin and START do not start a game.

## 1. Platform and cabinet

SEGA Lindbergh ("Yellow", ride cabinet; **INFERRED**, the lindbergh notes call it Type 3) running the Special, Rev B (DVP-0010B, game ID `0x7d6ab3e3`). The game is a normal clean 32-bit Linux ELF, `elf/hod4M.elf`. Two players. This is a ride version: it also expects seat signals.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- 32-bit libraries as for the Lindbergh route: 32-bit (i386) libraries: SteamOS does not ship `libXt`, `libSM`, `libICE`, `libbsd`, `libmd` for i386; RavenGun builds them into its layer. `libopenal.so.0` needs `libsndio.so.7`, for which RavenGun uses a small stub (OpenAL then falls back to Pulse/ALSA).
- A writable `/var/tmp` for the game (RavenGun gives every Lindbergh game its own persistent one); the ride reset needs it.
- Mesa OpenGL (zink on RADV or radeonsi).

## 3. The official start script, or why there is none

On the cabinet the ELF is run by the Lindbergh OS. See [Official-Start-Scripts](Official-Start-Scripts). RavenGun starts the ELF directly with `lindbergh.so` preloaded.

## 4. The route we use

- `[Game] Type = Lindbergh`
- `[Input] Route = jvs`, `Board = Lindbergh`
- Native Linux, under gamescope, game folder mounted read-only style (overlay) at `/lb`; the executable is `elf/hod4M.elf`.
- `lindbergh.ini` (shipped in the profile folder): `[Display] KEEP_ASPECT_RATIO = true`, `HIDE_CURSOR = true`; `[Input] INPUT_MODE = 1`; `[Emulation] REGION = EX`, `FREEPLAY = none` (coins come from the daemon); `[Graphics] GPU_VENDOR = 2` (Mesa reports its vendor as just "Mesa"; value 2 keeps the Mesa-path patches on); `[System] DEBUG_MSGS = false`.
- OpenGL through Mesa **zink** on RADV (preferred); remove the zink environment variables to use radeonsi instead.
- `stackalign` is on: these games are built for a 4-byte-aligned stack, SteamOS's 32-bit libraries expect 16; a RavenGun wrapper library aligns the stack of every imported GL/X11/OpenAL call.
- Window size 1024x768.

## 5. Input

Lindbergh route: the original game talks JVS to the base board; RavenGun's `lindbergh.so` layer passes the JVS packets to the daemon's board (route `jvs`, board `Lindbergh`, seen by the game as `/dev/ttyRG0` in the sandbox). Controls:

- Coin and START from the daemon; shoot with the trigger; aim **off screen = reload**.
- If the cursor drifts, calibrate the guns in the game's test menu (TEST).
- Mouse and keyboard are also read from the window (`INPUT_MODE = 1`).

At start the ride asks for **START** to reset. After a game the game sends a ride command (0x18 or 0x19) and waits for 5 or 6; RavenGun's patch 0004 corrects the emulated answer.

## 6. Timing

**MEASURED** (2026-10-15): double-click, ride reset with START, then more than 5 minutes of attract without a crash.

## 7. What we saw on screen

Attract (**MEASURED**), no game yet.

## 8. Current state and open questions

- Coin and START do not start a game: the ride version most likely waits for seat signals (seat belts, the ride's own start button; assumption, derived from the Lindbergh loader's ride-board code).
- Open: emulate those ride signals.

## 9. What we tried and what did not work

- Without `/var/tmp`, the ride reset does not work.
- Patch 0004 fixed the reply to the ride's post-game command; the first game still does not start.

## 10. What is Linux-specific, and what differs on Windows

Linux-native game; no Wine. See [House of the Dead 4](House-of-the-Dead-4) for the shared Lindbergh route notes and [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
