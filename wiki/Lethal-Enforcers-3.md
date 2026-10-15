# Lethal Enforcers 3

**Status:** Working (2026-10-15). A double-click in the RavenGun app starts the game; it was played for 5.5 minutes in mouse mode on FREE PLAY. The movies (`.m1v`, DirectShow) go through the 32-bit GStreamer (`[Launch] Gst32 = true`); without it the game crashed at the first movie.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- Konami "PC Based" lightgun cabinet (Windows). Game executable `game.exe`, 2,760,704 bytes (32-bit, **INFERRED** from the 32-bit GStreamer requirement; size **MEASURED** from the profile).
- TeknoParrot template `GameProfiles/LethalEnforcers3.xml` revision 21, emulation profile `WartranTroopers`.
- Profile options: `General/GameMode = 2 PLAYERS` (other values `PLAYER 1 ONLY`, `PLAYER 2 ONLY`), `General/FpsLimitEnable = 0`, `General/FpsLimit = 60`, `General/UseLocaleEmulator = 1`, `Crosshair/Enable = 0`, `Bezel/Enable = 0`.

## 2. What the game needs

- Your own copy of the game folder. The game creates a `SAVE/` folder next to itself.
- **Movies.** `.\DATA\movies\*.m1v` are MPEG-1 video streams played through DirectShow, which needs a 32-bit GStreamer in Wine. SteamOS has none (no `lib32-gstreamer`); Steam's Proton does. `scripts/setup-gst32.sh` links it (see `docs/gst32.md`). **MEASURED:** without it the game ran, then crashed after about 28 s at the first movie: `err:quartz:autoplug Failed to create filter for "GStreamer splitter filter", hr 0x8007000e`, then a null-pointer crash in `game.exe`.
- `[Wine] GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins` is set in the profile. A 64-bit plug-in path (as used for Luigi's Mansion) does not help a 32-bit game.
- RavenGun provides the cabinet hardware the game expects.

## 3. The official start script, or why there is none

Not examined; `game.exe` starts directly. If your copy contains cabinet scripts, read them first and take over only what you need; see [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = TeknoParrot
EmulationProfile = WartranTroopers
Executable = game.exe
[Launch]
Mode = direct
Gst32 = true
[Wine]
GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins
[Input]
Route = tp-shm
Layout = WartranTroopers
```

Double-click: `rg-direct` runs Wine with the OpenParrot loader and the 32-bit GStreamer, no TeknoParrot front-end. **MEASURED** (bench, 2026-10-15): with `Gst32` the attract movie plays and the game starts. An older attempt with the plain loader injected after 3 s stopped the game (32-bit core, loader-lock); the standard loader route avoids that.

## 5. Input

Layout `WartranTroopers` through `tp-shm`: a 64-byte image, 32-bit button field at offset 8 (test, service, coin 1/2, per player start, trigger, reload, grenade, extra) and one byte per aim axis at offsets 12..19, left/top = 0, axes 2..253 inside the screen. In the app (mouse mode, 2026-10-15): the cabinet was on FREE PLAY, START = key 1, trigger = left button. Reload and player 2 were not noted separately.

## 6. Timing

- Without `Gst32`: the game ran about 28 s before the crash at the first movie. **MEASURED.**
- With `Gst32`: played 5.5 minutes on 2026-10-15. **MEASURED.**
- Boot time to attract and frame pacing: not measured yet.

## 7. What we saw on screen

**MEASURED:** the attract movie plays, FREE PLAY, then the game starts and is played.

## 8. Current state and open questions

- Working via double-click (2026-10-15).
- Not yet played with the real PS Move; player 2 not checked; `GameMode` other than 2 PLAYERS not tried.

## 9. What we tried and what did not work

- **Without `Gst32`**: crash at the first `.m1v` movie (splitter failure, null pointer in `game.exe`, then the loader ended the process).
- **A 64-bit GStreamer plug-in path**: no effect on a 32-bit game.
- **Early loader injection after 3 s with the 32-bit core under Wine**: the game hung (loader lock); the default entry-point route is used instead.

## 10. What is Linux-specific, and what differs on Windows

- SteamOS ships no 32-bit GStreamer, so Wine cannot decode MPEG-1; RavenGun links the one in Steam's Proton. On Windows DirectShow decodes `.m1v` natively.
- Under gamescope the dynamic linker drops `LD_LIBRARY_PATH` for the setcap'ed binary; the loader sets it again after `--`.
- See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
