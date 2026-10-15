# HALO Fireteam Raven

**Status:** Working (2026-10-14). A double-click in the RavenGun app starts the game with no scripts and no TeknoParrot front-end; it was played on a TV in mouse mode (coin, START, aim, shoot, reload, a kill) for 5 min 12 s. A second, fully native Linux route also exists. Sound is missing on the native route, and a few cabinet "not set up" messages stay on the attract screen.

RavenGun ships no games; you need your own copy of the game folder.

## 2026-10-15 — native route (own loader, no Wine, no TeknoParrot)

Everything here is **MEASURED** on the bench unless marked **INFERRED**. Addresses are virtual addresses in the game binary `g7/halo/game` (33,554,432 bytes, sha256 `e88ba3543d5613c8...`).

**Status.** Halo still *plays* via the TeknoParrot BudgieLoader route (Wine). The goal is the native route: the Linux ELF directly under the system `ld.so` inside a bwrap sandbox, with the NAS folder `g7/halo` as an overlay and a local write layer (`~/.local/share/ravengun/native/Halo/0/upper`); no Wine, no TeknoParrot. The route stays disabled in `packaging/native-games.json` until players can join.

### Input fix

The input shim (`tools/rt-input-shim`, `librg_rt_input.so`) read `/dev/shm/TeknoParrot_JvsState`, which was stale; the daemon writes `/dev/shm/ravengun_JvsState`. After pointing shim and profile at `ravengun_JvsState` (loader commit `185ef71`), START skips the FileSystem Integrity Test and the gun calibration screens and the game reaches its attract loop. TEST does nothing on the calibration screen (confirmed again).

### Coins and free play

- The built-in coin pulse of 14 ms is mostly missed by the game (4 presses gave +$0.25). With 60 ms it over-counts (4 presses gave up to +$3.25).
- Settings live in `pmuser/adj/save/<category>/<name>.{0,1,2}.txt`. File format: uint32 `20` (little endian), then the SHA-1 of the body (20 bytes), then uint32 body length, then the body. The body is the text `# RTDT Data Type AdjValStore\r\nname = <name>\r\nversion = 0\r\ntime_set = 1\r\nval = <value>\r\n` plus a terminating NUL byte.
- Writing `playerCost/freeplay.{0,1,2}.txt` with `val = 1` into the local write layer makes the attract loop show FREEPLAY.

### Sound (FMOD)

- The game links `libfmod.so.10` and `libfmodstudio.so.10` (FMOD Studio 1.10) and resolves 60 FMOD names itself, including the C++ Studio API (`FMOD::Studio::Bus`, `EventInstance`, `ChannelControl`).
- Audio data: 11 RIFF FMOD Studio banks in `data/snd/banks` (attract, diag, level1-6, MasterBank, MasterBank.strings, perm), 917 samples in total, all FSB5 Vorbis.
- The FMOD package on the NAS (`fmodapi44464linux`, FMOD Ex/Designer 4.44.64: `libfmodex`, `libfmodevent`) is the wrong API generation and cannot be used. TeknoParrot's BudgieLoader uses the Windows `fmod64.dll` / `fmodstudio64.dll` 1.10.2.
- The old RavenGun stub returned error 52 for everything, which logged `Failed to load FMOD sound bank: attract/level1/level2 (ec 52)`. It is now a "silent FMOD": every call returns `FMOD_OK` with valid dummy objects (`tools/fmod-stub`, `scripts/build-fmod-stub.sh`, commit `185ef71`).
- Plan, **not built yet**: an FMOD Studio to PipeWire wrapper with 5.1 output (parse the Studio banks, decode FSB5 Vorbis, mix), like DXVK but for audio.

### Why START does not start a game: the guns are cameras *(superseded, see the update below)*

A player can only join with a gun, and Halo's guns are cameras. Game log: `Webcam: Could not ID device for player 0 (0, 0, 0, 0)` and `Webcam: Aborting auto-id. All webcams reported brightness difference of 0.`

Code read with `objdump` on the raw image (the file has no section headers): `objdump -D -b binary -m i386:x86-64 --adjust-vma=0x400000`. The code references strings with absolute `mov $addr`.

- Webcam init at `0x49cdb0`: skips if byte `[0x1766561] != 0`; stores `time()` at `0x1c1f140`; calls the enumerator `0x49cc10`; then starts up to 4 devices (`0x49c300`) and prints `Webcam init successfully started %u devices!` on stdout.
- Enumerator `0x49cc10`: `popen("ls -1 /dev/video*")`, `getline` per line, `open(path, O_RDWR|O_NONBLOCK)`, `ioctl VIDIOC_QUERYCAP`; keeps the device if `device_caps` has VIDEO_CAPTURE. Device table at `0x1766580`, `0x206` bytes per device, maximum 4.
- Auto-identification (screen flash, per-camera brightness difference) is around `0x44e8xx` and `0x4548xx`. A stored ordering is used (`0x454d54`) only when the stored count equals the number of devices present (checked per device via `0x49d730`).
- The game finds cameras by enumerating `/dev/video*`, also runs `find /sys/devices/ -iname 'video*' | grep video4linux/%s`, supports YUYV and MJPG, and imports `open/ioctl/read/select/poll/close` but not `mmap` (V4L2 read I/O).

### Two GOTs: why plain LD_PRELOAD does not reach the game

The game binary is a rebuilt dump with two GOTs. The official JUMP_SLOT relocations are at `0x238dxxx`, but the code's PLT stubs jump through an older GOT at `0x1691xxx` (e.g. PLT `0x40d990` to GOT `0x1691250` = `open`) that is already filled with libc addresses before `LD_PRELOAD` constructors run. So ordinary `LD_PRELOAD` interposition does not reach the game.

RavenGun's new virtual-webcam library (`tools/v4l2-fake`, `librg_v4l2_fake.so`) therefore patches both: the relocations by symbol name, and a scan of the game's writable segments for pointers equal to libc's `open/open64/ioctl/read/close`. Measured afterwards: GOT `0x1691250` points into `librg_v4l2_fake.so`.

### Virtual webcams (in progress, not working yet)

Native profile key `"fake_video": N` binds `/dev/null` to `/dev/video0..N-1` in the sandbox and sets `RG_V4L2_FAKE`. The library answers `open/ioctl/read` for those paths with YUYV frames at 60 fps (tested outside the game). Inside the game the device table at `0x1766580` is still empty and the init guard byte is already 1; under investigation.

### Aim

From earlier research (`patches/Halo/AIM-GELEZEN.md` in the ravengun-patches repo): the aim getter at `0xdd5c60` reads a per-player gate byte at `0x1aa37c0` (must be <= 3) and the aim pair (float x, y) at `0x1f392a0 + 8*player`. Earlier runs showed player count `[0x1f392d0] = 0` and the per-player structure pointer `[0x181f7e0] = NULL`, because no gun/player is attached.

### Update 2026-10-15 (later): corrections

- **Superseded:** "a player can only join with a gun, and Halo's guns are cameras" (and the heading "the guns are cameras"). The webcams in Halo are the **QR scanners** (player login), not the guns. Evidence: the strings `%s/webcamID/qr%i.ppm`, `P1 QR Scanner is not detected!`, `QR scanners need to be configured!`, `ATTRACT_WEBCAM_CONFIG` and `WebcamAutoIdProc`. The webcam auto-ID is therefore not what blocks players from joining.
- The guns are on a mechanical mount (cabinet type `STANDARD TETHERED`; the calibration screen says "Pull gun all the way back and towards the left ... You should hit the limits of the gun"). Aim comes from analog channels of the IO board: earlier research found that the per-frame player input asks analog channels 793/794 for player 1, at fixed addresses `0x181d418` and `0x181d538`. Separately the binary contains `cmgr_*` code (FTDI, "fpga", "led_data") which looks like an LED/FPGA board, not the aim.
- **Still OPEN:** why START in the attract loop does not let player 1 join.
- **Correction:** the webcam init guard `[0x1766561] = 1` is a *mode*, set by `0x49c2c0(mode, 1, 0)` from the cabinet setup code at `0x436520`; it is not a "skip" flag. Init then takes path `0x49ce70` and still enumerates.

### Virtual webcams: measured results (loader commit `28d8127`)

- **Why the game first never opened `/dev/video*`:** `halo.so` (the dump's HASP shim) in `LD_PRELOAD` makes every child process die silently, so `popen("ls -1 /dev/video*")` returned nothing (`getline` gave -1). Proven with `nsenter` into the game's mount namespace: `sh -c 'ls -1 /dev/video*'` prints nothing with `halo.so` preloaded and prints `/dev/video0` and `/dev/video1` without it. Fix: `librg_v4l2_fake.so` clears `LD_PRELOAD` in the game process after loading, so children run clean. This also affects the FileSystem Integrity Test, which runs `sha1sum` via `popen`.
- Halo passes ioctl request numbers sign-extended (`0xffffffff80685600` for `VIDIOC_QUERYCAP`); only the low 32 bits count.
- Halo uses V4L2 **MMAP** streaming (`REQBUFS` count 16, memory MMAP, 640x480 YUYV, buffers of 614400 bytes) and calls `mmap` through the same old GOT. This corrects the earlier note that the game uses read I/O. The library hands out anonymous memory per buffer and fills it on `DQBUF`.
- The identification compares each camera's value against 80 (`cmp $0x50` at `0x4547a1`); exactly one camera must exceed it. Results: constant black frames gave `Could not ID device for player 0 (16, 16, 0, 0)`; one constantly bright camera gave `Could not auto-ID devices: 0 webcams ID'd, 2 webcams present`. So the game now sees two QR scanners present, and the auto-ID measures a brightness *change* during a flash, not constant brightness.
- The native route stays disabled; Halo keeps playing through BudgieLoader.

### Next steps

1. Get the virtual webcams found and assigned to players (stored ordering, or answer the brightness auto-ID).
2. Feed aim and trigger from RavenGun's input into the aim pair.
3. Then the FMOD wrapper for sound.

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

**Default (double-click in the app).** **MEASURED**, 2026-10-14: daemon, then `rg-direct`, then Wine running the ELF loader (BudgieLoader, the TeknoParrot ELF loader). The profile:

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

**Native Linux route (also working).** The ELF is started by the kernel's own `ld.so` inside a bubblewrap sandbox with `LD_PRELOAD=/pm/g7/halo/halo.so:<RavenGun input helper>`. Working directory and `HOME` are `/pm/g7/halo`, arguments `-f1920x1080 -n`, the game folder is a read-only lower layer with a writable overlay. Gamescope draws the picture. A stub that exports the two FMOD library names and returns error code 52 lets the game run without sound. **MEASURED.** *(Superseded 2026-10-15: the stub is now a "silent FMOD" returning `FMOD_OK`; and the native route cannot start a game yet because the guns are cameras. See the 2026-10-15 section above.)*

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

Messages that stay on the attract screen: `QR scanners need to be configured!`, `P1 QR Scanner is not detected!`, `P2 QR Scanner is not detected!`, `Factory Setup Has Not Been Completed!`. They mean "this cabinet has not been set up" and do not stop play. On the double-click route the game reached the mode choice and a mission with aiming and a kill.

## 8. Current state and open questions

- **Working** via double-click (5 min 12 s, played on the TV, 2026-10-14). The five-minute bar is met on both routes (attract loop and played game).
- Not yet played with the real PS Move on the double-click route.
- Open: the QR / factory-setup messages. The strings belong to attract states (`ATTRACT_FACTORY_SETUP_INCOMP`, `ATTRACT_WEBCAM_CONFIG`, `ATTRACT_GUN%i_MISSING`); the factory setup is an item in the cabinet's DIAG (TEST) menu. **INFERRED** from names in the binary; running that menu item in the attract loop has not been tried.
- Open: sound on the native route (needs the FMOD stub; nothing is heard). *(Superseded 2026-10-15: the silent FMOD stub exists; real sound needs the planned FMOD Studio to PipeWire wrapper.)*
- Open: whether the second player and the four-player variants work in play; only player 1 was exercised.

## 9. What we tried and what did not work

- **"TEST skips the calibration" on the native route**: measured false. Six TEST pulses on all four boards changed nothing; START alone worked. (On the Wine route TEST twice does skip it.)
- **Optical aim**: we read the camera "brightness difference" lines and concluded the guns are tracked by the webcams. Withdrawn: aim runs through the board channels of the `WartranTroopers` layout, and the webcam step also failed on days when the game reached attract. *(Superseded 2026-10-15: on the native route a player can only join with a webcam gun; the game log says `Could not ID device for player 0`. See the 2026-10-15 section above.)*
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
- `libfmod.so.10` / `libfmodstudio.so.10` are not on a normal machine; the stub that returns error code 52 is working tooling, not a fault. Without it the game jumps to address 0.
- For the picture use gamescope (full screen on the TV, or headless for tests).

See also [Running on Linux](Running-on-Linux), [Wine Notes](Wine-Notes) and [Loader Architecture](Loader-Architecture).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
