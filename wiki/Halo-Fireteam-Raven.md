# HALO Fireteam Raven

**Status:** Working (2026-10-15). A double-click in the RavenGun app starts the game on the native Linux route (own loader, no Wine, no TeknoParrot): attract with FREEPLAY, Story Mode played for 5.5 minutes with trigger, aim and reload through emulated arcade lightguns, and sound in stereo or LPCM 5.1 when you supply the FMOD 1.10 libraries yourself. The older Wine route (TeknoParrot's ELF loader) still works as a fallback.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Raw Thrills "PC Based" lightgun cabinet, 2018, with the cabinet's own Linux image. **MEASURED** from the files: `game` is a **64-bit Linux ELF** (`ET_EXEC`, x86-64), not a Windows program. The folder layout on the cabinet is `/pm/g7/halo` with `game`, `game_original`, `halo.so`, `data/`, `eFileMaps/` and `utils/` (cabinet scripts).
- 1 to 4 players. The cabinet variant is chosen at start from a code the cabinet tool `rtinit -ct` prints: 9 = dual-screen 4-player environmental (3880x1080); 4 = mounted-gun 2-player (1920x1080); 3 = super-deluxe 4-player tethered (1920x1080); 8 = 55-inch 2-player tethered (1920x1080). **MEASURED** from the cabinet scripts.
- The game reports `Welcome to Halo v03.11`, `Game Rev: 57529, Library Rev: 1412`. **MEASURED.**
- The TeknoParrot template for this title is `GameProfiles/Halo.xml` revision 2, with `CabinetType = STANDARD TETHERED`; the RavenGun profile uses it unchanged.
- The cabinet has a webcam per player and the game runs a "brightness difference" check on a camera at start-up (`Baseline %u: %u`). It is only a start-up step; aim does not depend on it (see section 9).

## 2. What the game needs

- Your own, unmodified game folder (`g7/halo`, about 2.7 GB of data). `[Identify] Path = game`, `Size = 33554432` in `game.ini` is how RavenGun recognises it. **MEASURED.**
- **MEASURED:** 13 shared libraries in the ELF's needed list: `libGL`, `libGLU`, `libpthread`, `libdl`, `libudev`, `liblapack`, `libiw`, **`libfmod.so.10`**, **`libfmodstudio.so.10`**, `libstdc++`, `libm`, `libgcc_s`, `libc`. On an ordinary Linux machine all resolve except the two FMOD libraries (FMOD 1.10 is proprietary). The game resolves its OpenGL, FMOD and udev calls itself at run time through its own name table.
- Write access in `pmuser/` (the game keeps counters and settings there). RavenGun runs the game from a local view, so the files in your game folder stay untouched.
- A GPU with OpenGL. `[Display] CustomResolution = 1920x1080`.
- The cabinet's lightgun board is emulated by RavenGun (nothing to provide).

## 3. The official start script, or why there is none

The cabinet starts the game with `utils/run_game.sh` (and `utils/go.sh`):

```sh
cd /pm/g7/halo
LD_PRELOAD=/pm/g7/halo/halo.so ${GAMEDIR}/game2 -f${SCREEN_RES} -n
```

`SCREEN_RES` comes from `utils/rtinit -ct` (see section 1), `DISPLAY=:0` is exported, and after the game a `case` on its **exit code** triggers cabinet actions: 222 = restart, 223 = reboot, 224 = modification, 225 = factory reset, 226 = power-cycle. **MEASURED** from the files. `game2` does not exist in the folder; the real file is `game`, the same image.

**Never run these scripts on your PC.** They contain `reboot -f`, `sync`, `rm -rf ${USERDIR}` (deletes the user folder) and, in `go.sh`, `passwd -l`, `swapoff -a` and network setup. RavenGun reads them and takes over only what it needs: the arguments `-f1920x1080 -n`, the working directory and the `HOME` setting. See [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

**Wine route (fallback; the double-click route until 2026-10-15).** **MEASURED**, 2026-10-14: daemon, then `rg-direct`, then Wine running the ELF loader (BudgieLoader, the TeknoParrot ELF loader). The profile:

```ini
[Game]
Type = ElfLdr2
EmulationProfile = WartranTroopers
Is64Bit = true
[Launch]
Mode = direct
[Display]
CustomResolution = 1920x1080
[Input]
Route = tp-shm
Layout = WartranTroopers
```

No TeknoParrot front-end is started (`pgrep -x TeknoParrotUi` found nothing during the runs). Input comes from the RavenGun engine through the `tp-shm` shared-memory I/O bridge. The loader prints `Warning SHT_DYNSYM not found in section headers` for this game; that is harmless (the file simply has no section headers, the symbols are found through the dynamic segment) and also appears with games that run fine.

**Native Linux route (the default since 2026-10-15).** The ELF is started by the kernel's own `ld.so` inside a bubblewrap sandbox; the game folder is a read-only lower layer with a local writable overlay, working directory and `HOME` are `/pm/g7/halo`, arguments `-f1920x1080 -n`, and gamescope draws the picture. RavenGun adds three small libraries in the game process: an input helper (coins, START, TEST from the I/O bridge), an emulation of the cabinet's USB lightguns (see section 5), and an FMOD wrapper for sound. RavenGun also seeds a few files into the writable layer so the cabinet boots straight to attract: free play, the two gun adjustments and the gun calibration records. The cabinet type is set to STANDARD MOUNTED (two guns), the same choice as `CabinetType` in the TeknoParrot profile. **MEASURED.**

**Sound.** The game needs FMOD Studio 1.10 for Linux (`libfmod.so.10`, `libfmodstudio.so.10`), which is proprietary and not part of the game folder; RavenGun ships no FMOD files. Put your own 64-bit copies in `patches/Halo/dropin/fmod/` of your user layer (example source: the Linux version of a Steam game that ships FMOD 1.10, e.g. Celeste's `lib64/`). RavenGun's wrapper loads them in the game process and forwards every call. Without them it can forward to the Windows FMOD 1.10.2 of your own TeknoParrot install under Wine; without either the game runs silently. The app option "Audio output" chooses STEREO or LPCM 5.1; Halo's own mix is stereo, so for 5.1 the wrapper adds an upmix (center, LFE below 120 Hz, delayed surrounds). **MEASURED** per channel during play.

Pass `--tpui --route evdev` only if you want to go through TeknoParrot's own front-end; the double-click route does not need it.

## 5. Input

The profile layout `WartranTroopers` is a 64-byte image with a 32-bit button field at offset 8 and one byte per aim axis at offsets 12..19 (**MEASURED** from the profile):

```
bit 0 test      bit 6 p1.start     p1.trigger = bit 7, p1.reload = 8,
bit 1 service   ...                p1.grenade = 9, p1.aux1 = 10
bit 2 coin 1                       (p2.start = bit 11, p2.trigger = bit 12, ...)
bit 3 coin 2
bit 4/5 volume up/down
axes: p1.x 12, p1.y 13, p2.x 14, p2.y 15, p3.x 16, p3.y 17, p4.x 18, p4.y 19
      min 0, max 255; inside the screen the axes stay at 2..253
```

**Arcade lightguns (native route).** The cabinet guns are "IRTrack - Rev. 2" USB devices (FTDI) that send a small ASCII message stream per gun (IR points, buttons, status). RavenGun replaces the game's FTDI calls in the game process and presents two healthy guns: buttons come from the I/O bridge and aim is handed to the game's gun driver directly as 0..1 per axis (the game's Y axis runs bottom to top). The table is per game (`patches/Halo/irtrack.ini`). On this cabinet type the right-hand player is internally player 3; RavenGun maps player 2's START to that switch. **MEASURED** for player 1; player 2 not yet confirmed with a second physical gun.

Keys in the app (mouse mode, **MEASURED** on the TV):

| Action | How |
|---|---|
| Coin | key 5 |
| START | key 1 (hold it briefly) |
| TEST | key 0 (hold it briefly) |
| Aim | mouse / PS Move |
| Trigger | left button |
| Reload | right button |

**Calibration screens.** At first start the game shows "Player 1 gun (left): pull the gun all the way back and towards the left, then press the trigger" and "Press the TEST button to skip calibration for this gun". On the double-click (Wine) route, **press TEST twice** (hold key 0 briefly each time) to skip the calibration of both guns. On the native route TEST did nothing (six pulses on four boards, no change in the game's log or screen) and **START alone** took the game through the file test and the calibration into attract. **MEASURED** on both routes.

**Coins.** A coin is a counter of presses; a short pulse is one quarter. A coin press held far too long makes the game print `Detected more coin pulses than safely allowed`. **MEASURED.**

## 6. Timing

- Native route: first log line after start **1 s** with a warm file cache, **11 s** with a cold one (first run after a long time); the difference was the file cache, not the picture path. File test finished in the same second as a START pulse. Start to attract about 50 to 75 s. **MEASURED.**
- Native route: attract loop ran **6.0 minutes** without interruption in one run (363 s) and 9.5 minutes over two runs; the loop changes level demo (`attract`, `level1` ... `level5`), so it is not a frozen picture. **MEASURED.**
- Double-click route: 5 min 12 s with a played round, one kill. **MEASURED.**
- Frame pacing: not measured yet.

## 7. What we saw on screen

**MEASURED**, native route, with screenshots and the game's log:

1. Black for a few seconds.
2. The file test screen: `Performing Integrity Test.`, `Tested: 2232`, `Failed: 1`, `Press START or Ding to skip File Test.`
3. The gun calibration screen (see section 5).
4. The attract loop: title screen with two marines, **`Press START to Begin`**, **`Money In: $16.75`** after four coins.

Messages that stay on the attract screen: `QR scanners need to be configured!`, `P1 QR Scanner is not detected!`, `P2 QR Scanner is not detected!`, `Factory Setup Has Not Been Completed!`. They mean "this cabinet has not been set up" and do not stop play. With RavenGun's seeded files and cabinet type (section 4) the native route now boots straight to attract with FREEPLAY and none of these messages; the file test takes about 3 minutes when the game folder is on a network share. On the double-click route the game reached the mode choice and a mission with aiming and a kill.

## 8. Current state and open questions

- **Working** via double-click on the native route (2026-10-15): attract, Story Mode played for 5.5 minutes with emulated arcade lightguns, sound in stereo or LPCM 5.1 with your own FMOD 1.10. The Wine route (2026-10-14, 5 min 12 s with a kill) remains as a fallback.
- Open: player 2 with a second physical gun, and the four-player cabinet variants.
- Open: the attract demo is sometimes silent; probably the game's operator setting for attract sound, not the wrapper (**INFERRED**).

## 9. What we tried and what did not work

- **"TEST skips the calibration" on the native route**: measured false. Six TEST pulses on all four boards changed nothing; START alone worked. (On the Wine route TEST twice does skip it.)
- **Optical aim**: we read the camera "brightness difference" lines and concluded the guns are tracked by the webcams. Withdrawn: aim runs through the board channels of the `WartranTroopers` layout, and the webcam step also failed on days when the game reached attract. The webcams belong to the cabinet's QR scanners (player login), not to the guns.
- **Silent FMOD stub**: an early stub returned an error for every call (the game logged that its sound banks failed to load); it was replaced by the FMOD wrapper described in section 4.
- **Joystick / SDL hypothesis**: refuted. During calibration the game holds no `/dev/input` device open and has not loaded SDL, so an extra virtual device is not the route.
- **A crash in our own helper** (SIGBUS in the input helper): the shared image was truncated while mapped. Fixed by reading with `pread` and writing in place.
- **A probe that overwrote the helper's default switch table** made TEST fail on every run; removing the probe fixed it. Lesson: do not change two things per run.
- **Start-up time comparisons** between a cold and a warm file cache differ by a factor of ten; always say which one you measured.
- **Running the cabinet scripts** is not an option (see section 3).

## 10. What is Linux-specific, and what differs on Windows

- The game is a Linux program. On Linux it runs natively (no Wine) with the kernel's `ld.so`; the default route runs it inside TeknoParrot's ELF loader under Wine. On Windows you would need a Linux environment or an ELF loader.
- On the native route RavenGun loads an input helper with `LD_PRELOAD`; Windows has no equivalent and would use DLL injection.
- The native route runs in bubblewrap with the game folder as a read-only layer and an overlay for writes; the game writes into `pmuser/`, so give it a working directory and `HOME` explicitly.
- Lightgun and keys are virtual `uinput` devices. A udev rule granting your user access to `/dev/input` and `/dev/dri` is needed. The gun is a mouse-class device on purpose, so SDL does not see it as a joystick (this game does not use SDL anyway).
- `libfmod.so.10` / `libfmodstudio.so.10` are not on a normal machine; supply your own (section 4). Without any FMOD the wrapper keeps the game running silently.
- For the picture use gamescope (full screen on the TV, or headless for tests).

See also [Running on Linux](Running-on-Linux), [Wine Notes](Wine-Notes) and [Loader Architecture](Loader-Architecture).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
