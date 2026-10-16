# Aliens Armageddon

**Status:** Not working yet (2026-10-15). On RavenGun's native Linux route the game reaches calibration, the attract loop and the in-game HUD, but the enemy models are missing from the game files of the tested dump, so enemies are invisible and the game cannot be played properly.

## 1. Platform and cabinet

- Raw Thrills Linux PC-based lightgun cabinet. The game file `game` (about 9.1 MB) is a 32-bit i386 Linux ELF, the 1920x1080 build. **MEASURED**
- The cabinet's gun board is Raw Thrills' RIO board over USB (an older version than the one in Jurassic Park). Aiming on this cabinet goes through infrared cameras in the guns, not through the RIO board's analog channels. **INFERRED** from the game's strings.
- Template profile: TeknoParrot `AliensArmageddon` (revision 19), emulation profile `RawThrillsGUN`.

## 2. What the game needs

- Your own dump of the game folder; RavenGun ships no games. All of the game's files must be present, including its `.g6` model files.
- 32-bit libraries `libglut.so.3`, `libXi.so.6`, `libGLU.so.1`, `libesd.so.0`, and PhysX 2.x libraries (`libPhysXLoader.so.1`, `libPhysXCore.so`, `libNxCharacter.so.1`, `libNxCooking.so`) plus `libcsv.so`. RavenGun stages them.
- RavenGun provides the cabinet hardware the game expects; the cabinet's gun board is emulated by the RIO bridge (section 5).

## 3. The official start script, or why there is none

The cabinet starts the game with `utils/run_game.sh` using the arguments `-f<res> -e`. RavenGun uses the same arguments (`-f1920x1080 -e`). There is no start script for other platforms.

## 4. The route we use

**MEASURED** 2026-10-15: native Linux route, no Wine.

- A bubblewrap sandbox mounts your game folder at `/pm` (read-only, with a local write layer).
- RavenGun's own ELF loader (`rg-elfloader`) starts the game, because the game asks for `/usr/lib/libcsv.so` by absolute path; the loader finds it by base name.
- Preloaded RavenGun layers: the cabinet-hardware layer, `librg-threadprio.so`, the RIO bridge `librg_rio_bridge.so`, and `librg-glslfix.so` (an OpenGL shader fix).
- Window: 1920x1080 through gamescope.

```ini
[Game]
Type = ElfLdr2
EmulationProfile = RawThrillsGUN
[Input]
Route = tp-shm
Layout = RawThrillsGUN
```

The native-route entry in `patches/<Game>/native.json` (the Aliens Armageddon folder under `patches/`) is still marked "not tested" and disabled in the app's automatic selection, even though the bench run below reached the game.

## 5. Input

The input bridge is `librg_rio_bridge.so` (32-bit), driven by a table `rio-invoer.ini`. It answers as the cabinet's gun board over USB: it intercepts the game's `pmrt_usb_*` calls (open, close, interrupt read/write, bulk read/write) and returns 64-byte reports with 19 switch fields and 4 analog fields. This older RIO version needs no encryption on the reports.

- Buttons, coin and START come through the board. The switch ids for START, TEST and trigger were measured; the rest are taken from Jurassic Park and are not all verified on this cabinet.
- Aim goes through the RIO analog channels 19..22: **MEASURED** 2026-10-15, the game's gun calibration (top-left, bottom-right, trigger, START to accept) works with a mouse as the lightgun. The real cabinet also has IR cameras in the guns (`cmgr`/FTDI, `io_irtrack`); that path is not emulated and was not needed for calibration.
- Messages seen with the emulated board: "Problem detected with 12v fuse/power supply" and "Right gun not calibrated" (only player 1 was calibrated); the calibration is not kept between starts yet.

## 6. Timing

Not measured yet. The sources only say the game reaches calibration, attract and the HUD; no time to attract and no play duration were recorded.

## 7. What we saw on screen

- The calibration screen.
- The attract loop.
- The in-game HUD.
- **Enemies are invisible**: 16 `.g6` model files are absent from the game folder of the tested dump (`brute*`, `buddy*`, `bullet`, `burn_*`, `cams`, `camtest2`, `capella`, `c_interior*`). The game runs without them, but nothing draws.

## 8. Current state and open questions

- Blocking: the missing model files. A complete dump, or the missing files from a complete copy, is needed before this title can be called working.
- The 12 V fuse warning (a board status bit) and keeping the calibration between starts are open.
- Switch ids beyond START/TEST/trigger are unverified.
- Nothing has been played for five minutes yet.

## 9. What we tried and what did not work

- The static analysis of the game found its RIO functions by their constants and call graph (no symbols), and matched them to Jurassic Park function by function.
- `librg-glslfix.so` is preloaded to fix OpenGL shader compatibility on Mesa (details of what it fixed for this title were not recorded).

## 10. What is Linux-specific, and what differs on Windows

The game is a Linux program; there is no Windows build. TeknoParrot's ElfLdr2 loader runs it under Wine on Windows. RavenGun instead runs it natively with its own loader, the RIO bridge and a sandbox. Related: the Raw Thrills titles [Ghostbusters](Ghostbusters) and [Walking Dead](Walking-Dead) use the same bridge and route.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
