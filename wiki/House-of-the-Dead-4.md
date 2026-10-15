# The House of the Dead 4

**Status:** Not working yet. Attract, coin, START and the intro work on RavenGun's Lindbergh route, but during the game the picture goes white, then GAME OVER.

## 1. Platform and cabinet

SEGA Lindbergh ("Red") cabinet (**INFERRED** from the goal list). The game is a normal 32-bit Linux ELF. The folder we tested is **Rev C** (`hod4M.elf`, game ID `0xe213414d`, DVP-0003C), a clean ELF, and **not** the Special; see [The House of the Dead 4 Special](House-of-the-Dead-4-Special). Two players.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- The folder must be mapped to the HOTD4 profile. (Known pitfall, **MEASURED** in the library setup: a library that links the folder "The House of the Dead 4" to the *Special* profile would start the Special instead.)
- 32-bit (i386) libraries: SteamOS does not ship `libXt`, `libSM`, `libICE`, `libbsd`, `libmd` for i386; RavenGun builds them into its layer. `libopenal.so.0` needs `libsndio.so.7`, for which RavenGun uses a small stub (OpenAL then falls back to Pulse/ALSA).
- A Mesa OpenGL driver (zink on RADV, or radeonsi). The game's shaders are fragment programs adapted from NVIDIA-era code; the layer ships patched shader files.
- The Lindbergh base board, EEPROM and security board are provided by `lindbergh.so`; no user step.

## 3. The official start script, or why there is none

On the cabinet the game ELF is run by the Lindbergh OS. See [Official-Start-Scripts](Official-Start-Scripts). RavenGun starts the ELF directly with the `lindbergh.so` layer preloaded; there is no shell chain.

## 4. The route we use

- `[Game] Type = Lindbergh`
- `[Input] Route = jvs`, `Board = Lindbergh`
- Native Linux, under gamescope, game folder mounted read-only style (overlay) at `/lb`; the executable is `elf/hod4M.elf`.
- `lindbergh.ini` (shipped in the profile folder): `[Display] KEEP_ASPECT_RATIO = true`, `HIDE_CURSOR = true`; `[Input] INPUT_MODE = 1`; `[Emulation] REGION = EX`, `FREEPLAY = none` (coins come from the daemon); `[Graphics] GPU_VENDOR = 2` (Mesa reports its vendor as just "Mesa"; value 2 keeps the Mesa-path patches on); `[System] DEBUG_MSGS = false`.
- OpenGL through Mesa **zink** on RADV (preferred); remove the zink environment variables to use radeonsi instead.
- `stackalign` is on: these games are built for a 4-byte-aligned stack, SteamOS's 32-bit libraries expect 16; a RavenGun wrapper library aligns the stack of every imported GL/X11/OpenAL call.

## 5. Input

Lindbergh route: the original game talks JVS to the base board; RavenGun's `lindbergh.so` layer passes the JVS packets to the daemon's board (route `jvs`, board `Lindbergh`, seen by the game as `/dev/ttyRG0` in the sandbox). Controls:

- Coin and START from the daemon; shoot with the trigger; aim **off screen = reload**.
- If the cursor drifts, calibrate the guns in the game's test menu (TEST).
- Mouse and keyboard are also read from the window (`INPUT_MODE = 1`).

## 6. Timing

Not measured as a full run. Attract is shown; there is no long play yet.

## 7. What we saw on screen

**MEASURED** (2026-10-15): attract looks right; coin and START work; the intro plays; during the game the picture is **white** (shaders were ruled out; radeonsi instead of zink is white too), then GAME OVER.

## 8. Current state and open questions

- Open: the white picture during gameplay.
- `game.ini` still says "never started"; the later goal-list note (2026-10-15) reports the run above. The newer information is used here.
- Profile resolution is 1280x768.

## 9. What we tried and what did not work

- With `stackalign` the game runs; without it the 32-bit system libraries crash on misaligned SSE stack accesses (seen on other Lindbergh titles).
- Shaders excluded as the cause of the white screen.
- Switching from zink to radeonsi: white as well.

## 10. What is Linux-specific, and what differs on Windows

Linux-native game; no Wine. The Lindbergh layer replaces hardware that only exists on the cabinet. Differences from the original: stack alignment wrapper, 32-bit libraries supplied by RavenGun, and Mesa instead of the NVIDIA driver of 2006. See [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
