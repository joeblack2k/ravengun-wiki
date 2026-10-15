# Ghostbusters

**Status:** Not working yet (2026-10-15). On RavenGun's native Linux route the game starts and prints "Welcome to Ghostbusters v01.17", then stops at "Error Loading RTDT Defs File" because data the cabinet supplies at runtime is not in the tested dump.

## 1. Platform and cabinet

- ICE / Play Mechanix / Raw Thrills Linux PC-based lightgun cabinet. The game file `game` (about 11 MB) is a 32-bit i386 Linux ELF; the whole dump is about 2.7 GB (`game`, `g6/`, `utils/`).
- Template profile: TeknoParrot `GhostBusters` (revision 7), emulation profile `RawThrillsGUN`. The loader reports "Ghostbusters 1.17 US".

## 2. What the game needs

- Your own dump; RavenGun ships no games.
- The game expects to live in a folder named **`pm`** (the Play Mechanix install root): it opens absolute paths such as `/pm/g6/ghostb/data` and `/pm/utils/...`. On Windows TeknoParrot refuses it with "GAME PATH CHECK FAILED" unless every file sits in a `pm` folder and the path to the ELF points inside it. RavenGun mounts your game folder at `/pm`; in the Windows-side profile `[Identify] Path = pm/game` and a view folder `pm` with links to your files make the check pass.
- 32-bit libraries `libglut.so.3`, `libXi.so.6`, `libGLU.so.1`, `libesd.so.0`, `libcsv.so`.
- RavenGun provides the cabinet hardware the game expects; the gun board is emulated by the RIO bridge.

## 3. The official start script, or why there is none

The cabinet starts the game from `utils/` scripts (for example `check_usb_drivers.sh`) with the arguments `-f<res> -e -mg`. RavenGun uses `-f1920x1080 -e -mg`.

## 4. The route we use

**MEASURED** 2026-10-15: native Linux route, same recipe as [Aliens Armageddon](Aliens-Armageddon): `rg-elfloader`, your folder at `/pm` (read-only with a local write layer), the RIO bridge, `librg-threadprio.so`, `librg-glslfix.so`, gamescope 1920x1080. Disabled in the app's automatic selection (status "parked").

```ini
[Game]
Type = ElfLdr2
[Input]
Route = tp-shm
Layout = RawThrillsGUN
```

## 5. Input

`librg_rio_bridge.so` answers as the cabinet's gun board over USB. Its table is copied from Aliens Armageddon: the board library is byte-identical in this game with a fixed address shift of -0x5F0C0 (measured 2026-10-15), so hooks for open/read/write/close were derived from that shift and their signatures were checked. Switch ids are Aliens Armageddon's and are not re-verified for this game.

## 6. Timing

Not measured yet.

## 7. What we saw on screen

"Welcome to Ghostbusters v01.17" in the log; no picture is documented. The game then reports "Error Loading RTDT Defs File" and exits.

## 8. Current state and open questions

- Blocking: data supplied by the cabinet at runtime is missing from the dump, so the game cannot read its definition files.
- Not played; aim and button mapping are untested.
- Whether the OpenGL context needs more work after that point is not known.

## 9. What we tried and what did not work

- On the Windows/TeknoParrot route the loader recognised the game but stopped with "GAME PATH CHECK FAILED" for every layout (game in the root, in `g6/ghostb`, lower case, own write folder) until the `pm` folder rule was found; after that it went on to "Starting Game" but showed no picture.
- On the native route the start works; the stop is the data problem above.
- The i386 `libcsv.so` was needed as an absolute path; `rg-elfloader` finds it by base name.

## 10. What is Linux-specific, and what differs on Windows

The game is a Linux program; on Windows TeknoParrot's ElfLdr2 loader would run it under Wine, and enforces the `pm` folder rule. RavenGun runs it natively. See also [Walking Dead](Walking-Dead).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
