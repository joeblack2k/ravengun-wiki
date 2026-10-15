# The House of the Dead EX

**Status:** Working (2026-10-15). Runs natively on Linux through RavenGun's Lindbergh route; 5.5 minutes played in mouse mode. It needs a small stack-alignment shim to avoid a crash at startup.

## 1. Platform and cabinet

- SEGA Lindbergh (Type 3 board), Linux PC. The game ELF is `elf/hodexRI.elf` (32-bit i386, about 9.5 MB).
- Two-player gun cabinet. Template profile: TeknoParrot `HOTDEX` (revision 9), emulation profile `Hotd4ex`.

## 2. What the game needs

- Your own dump of the game folder; RavenGun ships no games.
- `lindbergh.so` from the open-source lindbergh-loader, built locally by RavenGun's build script, and `libCg.so` 2.0 (the layer recompiles the Cg shaders on Mesa).
- `librg-stackalign.so`, a RavenGun shim. Without it the game died on an xcb assertion in `glXCreatePbuffer` (**MEASURED**).
- RavenGun provides the cabinet hardware the game expects (baseboard, I/O board, flash) in software.
- A writable `/var/tmp` per game (RavenGun gives every Lindbergh game its own).

## 3. The official start script, or why there is none

On the cabinet the Lindbergh system starts the ELF. lindbergh-loader has a starter, but RavenGun's engine replaces it.

## 4. The route we use

**MEASURED** 2026-10-15:

```ini
[Game]
Type = ElfLdr2          ; profile type of the template; the engine uses the Lindbergh route
[Input]
Route = jvs
Board = Lindbergh
```

The engine's native profile: `lindbergh.so` and `librg-stackalign.so` in `LD_PRELOAD` (stackalign first), resolution 1360x768, OpenGL through Mesa zink on RADV (`MESA_LOADER_DRIVER_OVERRIDE=zink`, `LIBGL_KOPPER_DRI2=1`; remove both to use radeonsi). `lindbergh.ini`: `INPUT_MODE = 1`, `REGION = EX`, `FREEPLAY = none`, `GPU_VENDOR = 2`, `KEEP_ASPECT_RATIO = true`, `HIDE_CURSOR = true`.

The stack shim exists because this old i386 code runs with a 4-byte aligned stack, while SteamOS's 32-bit GL libraries are built with SSE and expect 16 bytes.

## 5. Input

The daemon plays the cabinet's JVS board (2 players, 14 switch bits, 8 analog channels). Mouse mode: coin = 5, START = 1, shoot with the trigger, reload by aiming off the screen. Calibrate in the game's test menu if needed; the EEPROM lives in a local write layer.

## 6. Timing

- Played 5.5 minutes (**MEASURED**).
- The first start takes longer (shader cache and Cg recompilation); exact time not measured.

## 7. What we saw on screen

Attract and play in mouse mode. A detailed shot list was not kept in the sources.

## 8. Current state and open questions

- Real Move and two-player play are not recorded.
- Gun outputs (lamps, recoil) of the board are not mapped to the output yet.

## 9. What we tried and what did not work

Without `librg-stackalign.so` the game dies in `glXCreatePbuffer` (xcb assertion). Watch the start log for shader errors from the layer.

## 10. What is Linux-specific, and what differs on Windows

This route exists only on Linux. On Windows the same ELF runs through TeknoParrot's Lindbergh emulation. Here lindbergh-loader's layer, the JVS pass-through to the daemon, zink and the alignment shim replace it.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
