# Bug Busters

**Status:** Working (2026-10-15). A double-click in the RavenGun app starts the game; it was played for 5.5 minutes in mouse mode. The MPEG-1 movies need the 32-bit GStreamer (`[Launch] Gst32 = true`); without it the game dies right after MODE SELECT. It runs in a window (the taskbar stays visible).

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- EM-Teck "PC Based" lightgun cabinet (Windows). Game executable `BBPC.exe`, 380,928 bytes (32-bit, **INFERRED** from the 32-bit GStreamer requirement). **MEASURED** size from the profile.
- TeknoParrot template `GameProfiles/BugBusters.xml` revision 3, emulation profile `WartranTroopers`. Profile options include `General/UseLocaleEmulator = 1` and `General/InstantReload = 1`.
- The game has a MODE SELECT and ZONE SELECT screen before play. **MEASURED.**

## 2. What the game needs

- Your own copy of the game folder.
- **Movies.** `video/*.m` are MPEG-1 files played through DirectShow. Wine needs a 32-bit GStreamer for that. SteamOS has none; Steam's Proton does. `scripts/setup-gst32.sh` links it (see `docs/gst32.md`) and `[Launch] Gst32 = true` switches it on. **MEASURED:** without it, directly after MODE SELECT Wine logs `err:quartz:autoplug Failed to create filter for "GStreamer splitter filter", hr 0x8007000e`, the game reads a NULL pointer at `0x4456CB` and exits with code 5.
- With the GStreamer of GE-Proton10-34 plus `libvpx.so.6` from the Steam Linux Runtime, the intro plays and the game goes through ZONE SELECT into the game. **MEASURED.**
- RavenGun provides the cabinet hardware the game expects.

## 3. The official start script, or why there is none

Not examined; `BBPC.exe` starts directly. If your copy contains cabinet scripts, read them first and take over only what you need; see [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = TeknoParrot
EmulationProfile = WartranTroopers
Executable = BBPC.exe
[Launch]
Mode = direct
Gst32 = true
[Input]
Route = tp-shm
Layout = WartranTroopers
```

Double-click: `rg-direct` runs Wine with the OpenParrot loader and the 32-bit GStreamer, no TeknoParrot front-end. No gamescope is set, so the game runs in a window (the taskbar stays visible). **MEASURED.** When `rg-direct` runs under gamescope, `LD_LIBRARY_PATH` and the GStreamer variables are passed behind `--` because the setcap'ed gamescope drops them otherwise (relevant if you add `Gamescope = true`).

## 5. Input

Layout `WartranTroopers` through `tp-shm`: a 64-byte image, a 32-bit button field at offset 8 (test, service, coin 1/2, per player start, trigger, reload, grenade, extra) and one byte per aim axis at offsets 12..19, left/top = 0, axes 2..253 inside the screen. Played 5.5 minutes in mouse mode (coin key 5, START key 1, trigger left button). `InstantReload = 1` is on in the profile. Player 2 and the real PS Move were not checked.

## 6. Timing

- Played 5.5 minutes on 2026-10-15. **MEASURED.**
- Boot time to attract and frame pacing: not measured yet.

## 7. What we saw on screen

**MEASURED:** the intro movie, MODE SELECT, ZONE SELECT and play. The game runs in a window with the taskbar visible.

## 8. Current state and open questions

- Working via double-click (2026-10-15).
- Open: a full-screen picture (the window shows the taskbar); the profile does not set `Gamescope`.
- Not yet played with the real PS Move; player 2 not checked.

## 9. What we tried and what did not work

- **Without `Gst32`**: the game died right after MODE SELECT (splitter failure, NULL read, exit 5).
- **A 64-bit GStreamer** does not help a 32-bit game; Wine's 32-bit `winegstreamer.so` needs a 32-bit GStreamer.

## 10. What is Linux-specific, and what differs on Windows

- SteamOS ships no 32-bit GStreamer (no `lib32-gstreamer`), so Wine cannot decode MPEG-1; RavenGun links the one in Steam's Proton. On Windows DirectShow decodes it natively.
- Under gamescope the dynamic linker runs the setcap'ed binary in secure-execution mode and drops `LD_LIBRARY_PATH`; the loader sets it again after `--`.
- See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
