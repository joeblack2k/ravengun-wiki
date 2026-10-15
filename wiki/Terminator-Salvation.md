# Terminator Salvation

**Status:** Working (2026-10-14). A double-click in the RavenGun app starts the game with no scripts and no TeknoParrot front-end (daemon, `rg-direct`, Wine with the ELF loader BudgieLoader, full screen through gamescope). Measured on the TV in mouse mode: START, choose a mission with the trigger, aim, shoot, reload, a kill, 6 min 32 s.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Raw Thrills lightgun cabinet, 2010, two guns. The game is a **32-bit Linux program** (i386 glibc ELF, `ET_EXEC`, fixed load address `0x08048000`), not a Windows one. Build `01.25.00` (Sep 2011). **MEASURED** from the file.
- Picture: OpenGL through GLUT (15 `glut*` imports) and PhysX 2.8 (`DT_RPATH` `/usr/lib/PhysX/v2.8.1/`). 13 needed libraries: `libGL`, `libGLU`, `libglut`, `libpthread`, `librt`, `libtheora`, `libogg`, `libPhysXLoader`, `libm`, `libgcc_s`, `libc`, `libdl`, `libstdc++`. **MEASURED.**
- File: `game`, 7,764,284 bytes. All symbols are readable (1,020 dynamic symbols, 496 PLT stubs, none wiped), so every import can be resolved by name.
- Two more 32-bit programs sit in the folder (`t4-patch`, `irgun/gunrec_update`).
- **Pitfall (MEASURED):** the folder name on the original share ends with a space (`Terminator Salvation `); some tools then report "directory name invalid".
- The TeknoParrot template is `GameProfiles/Terminator.xml` revision 18, `EmulationProfile = RawThrillsGUN`.

## 2. What the game needs

- Your own dump of the game folder (`game`, `T4Data/`, `T4User/`, `irgun/`, ...).
- **MEASURED** (a 5-second file-access log): the game uses two absolute roots, `/g3/` (data folder) and `/T4User/` (user folder), which do not exist on an ordinary machine. The files it looks for are in the dump under relative paths (`T4Data/etranslation/english.csv`, `T4Data/etranslation_app/english.csv`, `T4User/log/syslog_bb3.txt`). The loader route provides them.
- It also probes `/dev/js0`, `/dev/dsp`, `/dev/sierra2` and `/dev/ttyS0` and the USB bus. The cabinet's I/O and gun boards are emulated by RavenGun, so you do not provide them.
- `libglut.so.3` is supplied by the loader itself (BudgieLoader exports the full freeglut API, 173 functions). The other libraries come from the loader's `libs` folder.
- The game writes into `T4User`; use a view or overlay so your source stays untouched.

## 3. The official start script, or why there is none

No start script was found in this folder, only `GeneralPurposeStateMachine.txt` (a state-machine description) and the data and user folders. If you ever find a cabinet start or install script, read it and take over only what you need; do not run it. Some of these scripts wipe drives or reboot the machine; see [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

Profile (`patches/Terminator/game.ini`):

```ini
[Game]
Type = ElfLdr2
EmulationProfile = RawThrillsGUN
Executable = game
[Launch]
Mode = direct
[Display]
Gamescope = true
[Input]
Route = tp-shm
Layout = RawThrillsGUN
```

Double-click: the daemon starts `rg-direct`, which runs BudgieLoader (TeknoParrot's ELF loader) under Wine; the game is drawn full screen through gamescope. Input arrives through the `tp-shm` I/O bridge; the TeknoParrot front-end is not started. **MEASURED.** An alternative route, via TeknoParrot's own front-end with evdev, also exists (`--tpui --route evdev`).

An earlier native route also reached attract: RavenGun's own 32-bit ELF loader (`rg-elfloader`) inside a bubblewrap sandbox on the TV. Notes from that route, useful if you build your own:

- The loader read the symbol count from `DT_HASH` only; this game has only `DT_GNU_HASH`. Derive the count from `(DT_STRTAB - DT_SYMTAB) / 16` (here 1,020).
- Do not use `--ro-bind / /` with bubblewrap if you need to add `/g3`; build the root from separate binds, and copy `/lib`, `/lib64`, `/bin`, `/sbin` as symlinks (`--symlink usr/lib /lib`). Binding them breaks the 32-bit interpreter chain (exit 127).
- For the writable `T4User` use `--overlay-src ... --overlay <upper> <work> /T4User`; the source stayed unchanged while 12,481 bytes went to the upper layer.
- 13 shaders failed to compile under Mesa (they carry no `#version`, so Mesa treats them as GLSL 1.10); one run crashed in attract on a null shader. That route patches them; on the double-click route this was not a problem.

## 5. Input

**Profile `RawThrillsGUN`:** a 64-byte block, buttons at offset 8 (test, service, coin 1/2, per player start/trigger/grenade/reload, volume), one byte per axis at offsets 12/16/20/24 for `p1.x`, `p1.y`, `p2.x`, `p2.y`, left/top = 0. **MEASURED** (the layout the bridge uses; it worked with real Move controllers earlier, aim within about 1 %).

In the app (mouse mode, **MEASURED**): **START** = key 1, hold it briefly; coin = key 5; trigger = left button (it also chooses the mission); reload = right button; test = key 0.

Background from the first native route (**MEASURED**): the real cabinet gives switches over a serial "JAMMA I/O" board on `/dev/ttyS0`, 115200 baud: frames of `LF`, a type character, hex digit pairs and `CR`; type `S` carries 4-bit wrapping counters per switch (trigger, pump, START, COIN, volume, TEST, SERVICE, tilt, bill). The game also sends `P<n><hex>`, `W03` and `s` continuously, and the far end must be read or the buffer fills and the log floods with `JAMMA: jamma_msg() -1`. The gun board is expected on a `ttyUSB*` port; `/g3/irgun` must be writable for the scan.

## 6. Timing

- Double-click route: 6 min 32 s with a played round. **MEASURED.**
- Native route, 2026-10-13: attract loop 19 min 5 s in one run and 11 min 8 s in another, ended by our own time limit. START came about 67 s after the loader jumped to the game. A crash 155 s after START in one run was the null shader. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

**MEASURED:** boot text ending in "Game file errors detected. Please run file check in 'test' mode.", then a warning screen "Data Files Corrupted ... Press Start To Continue". After START: a standby screen for about ten seconds ("Restarting Game Machine"), then the attract loop: demo scenes, gun tutorials, the Play Mechanix, Halcyon and CoinUp logos, "FREEPLAY" along the bottom. TEST opens the operator MAIN MENU (volume-down moves the cursor, START selects). On the double-click route the mission-select screen, aiming, shooting, reloading and a kill were seen.

## 8. Current state and open questions

- Working via double-click (2026-10-14), 6 min 32 s.
- Not yet played with the real PS Move on this route.
- Open: sound on the native route (`/dev/dsp` was `/dev/null`). Not checked on the double-click route.
- Open: the file-check warning appears at every boot; it does not stop the game.
- Open: the game tries TCP to an outside address every 25 to 100 s; no connection is known to have succeeded. RavenGun's sandbox isolates the network.
- The unit identifies itself as a UK unit in the menus (`01.25.00.UK`); what the region changes was not examined.

## 9. What we tried and what did not work

- **A system-call tracer** never saw the game reach its file opens. A wrapper library inside the game process (`LD_PRELOAD`) showed 88 lines. Observe this title from inside, not with an external tracer. A helper started beside the game cannot read the game's memory with the kernel's `ptrace_scope` at 1; start it from the parent or pass it an open descriptor.
- **The paced loop**: early on the game forked about 390 short-lived children in 4 s (one per 11 ms) and then exited with code 0 and no picture in the first native runs. Supplying the missing paths did not change the loop (not caused by missing files); the cause was not isolated at the time. Later native runs, with the serial board emulated and a working loader setup, reached attract.
- **Supplying invented content** for missing configuration files was refused as a principle: it would make the next measurement a measurement of our own invention.
- **A screenshot file's timestamp is not the time of the picture**: one "stall" was an old image.
- **A real `/dev/ttyS0`** is `root:uucp` mode 660; we do not widen permissions, we give the game a pseudo-terminal pair instead.
- Time comparisons across a network mount are not comparable (cold vs. warm cache).

## 10. What is Linux-specific, and what differs on Windows

- The game is a Linux program: on Linux it needs a 32-bit ELF environment (RavenGun uses BudgieLoader under Wine, or its own `rg-elfloader`). On Windows you would need a Linux environment or an ELF loader.
- bubblewrap needs the root built from explicit binds and `/lib*` as symlinks (see section 4); an overlay lets the game write without touching your files.
- Pseudo-terminals (`socat`) stand in for the serial ports; `/dev/ttyS0` permissions are the host's.
- Mesa compiles shaders without `#version` as GLSL 1.10; the original cabinet driver was more lenient.
- A `gnu/stubs-32.h` header is missing on a 64-bit system when you build 32-bit helpers; RavenGun ships a shim include.
- Use gamescope for full screen on the TV.

See [Running on Linux](Running-on-Linux) and [Loader Architecture](Loader-Architecture).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
