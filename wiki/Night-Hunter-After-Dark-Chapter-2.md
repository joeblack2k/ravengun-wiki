# Night Hunter - After Dark, Chapter 2

**Status:** Working (2026-10-15). A double-click in the RavenGun app starts the game; attract (ranking), START, mission select, play with score, game over and continue were seen over 5.5 minutes. It must run without DXVK, with a BepInEx input plug-in, GStreamer plug-ins for the movie and gamescope.

RavenGun ships no games; you need your own copy of the game folder.

## 1. Platform and cabinet

- UNIS "PC Based" lightgun cabinet (Windows). The game is a 64-bit **Unity** program: `qumo2_en.exe`, 22,321,664 bytes (English build). **MEASURED** from the profile; Unity is **INFERRED** from the BepInEx and AVPro Video requirements.
- It is the sequel to [After Dark](After-Dark), but a different engine.
- TeknoParrot template `GameProfiles/AfterDark2.xml` revision 6, emulation profile `WartranTroopers`. Default resolution 1920x1080.

## 2. What the game needs

- Your own copy of the game folder.
- **BepInEx**: the game folder contains a doorstop `winhttp.dll`; it must load under Wine, which needs `[Wine] DllOverrides = winhttp=n,b`. The TeknoParrot input plug-in `NHAD2TPPlugin` runs inside the game through it and delivers the input. **MEASURED** (diagnosed 2026-10-14).
- **Movie.** The attract movie is played by AVPro Video (Media Foundation, mp4). RavenGun supplies GStreamer plug-ins for Wine: `[Wine] GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins` (the same ones Raccoon Rampage uses). **MEASURED.**
- **No DXVK.** With DXVK the game stays on "Initializing..." because the AVPro video never arrives as a D3D11 texture. With Wine's own Direct3D 11 it continues to attract and play. **MEASURED** 2026-10-15.
- gamescope for full screen.

## 3. The official start script, or why there is none

Not examined; `qumo2_en.exe` starts directly. If your copy contains cabinet scripts, read them first and take over only what you need; see [Official Start Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = TeknoParrot
EmulationProfile = WartranTroopers
Executable = qumo2_en.exe
Is64Bit = true
[Launch]
Mode = direct
[Wine]
DllOverrides = winhttp=n,b
GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins
[Display]
Gamescope = true
[Input]
Route = tp-shm
Layout = WartranTroopers
```

Double-click: `rg-direct` runs Wine with the OpenParrot loader, full screen through gamescope. Leave `Dxvk` unset. **MEASURED.**

## 5. Input

Input arrives through the `NHAD2` BepInEx plug-in fed from the `tp-shm` layout `WartranTroopers` (32-bit button field at offset 8, one byte per aim axis at offsets 12..19). Measured on 2026-10-15 in mouse mode: **coin (key 5), START (key 1), mission select, shooting and score**. Reload and player 2 were not noted separately.

## 6. Timing

- Played 5.5 minutes on 2026-10-15 (attract, mission, game over, continue). **MEASURED.**
- Boot time to attract and frame pacing: not measured yet.

## 7. What we saw on screen

**MEASURED:** attract with the ranking list, START, mission select, a mission with a rising score, game over and a continue screen. With DXVK the screen stayed on "Initializing...".

## 8. Current state and open questions

- Working via double-click (2026-10-15).
- Not yet played with the real PS Move; player 2 not checked.
- Open: boot time and sound were not judged.

## 9. What we tried and what did not work

- **DXVK**: stuck on "Initializing..." (the AVPro movie never became a texture). Wine's own Direct3D 11 works.
- **Without `winhttp=n,b`**: Wine ignores the doorstop and the input plug-in is never loaded, so no input arrives.
- **Movie without the GStreamer plug-ins**: the AVPro movie does not play.

## 10. What is Linux-specific, and what differs on Windows

- `WINEDLLOVERRIDES=winhttp=n,b` is needed on Linux; on Windows the doorstop `winhttp.dll` next to the executable loads by itself.
- The Windows media stack plays the mp4 movie; under Wine it goes through GStreamer plug-ins.
- DXVK (Direct3D to Vulkan) helps many titles but not this one; on Windows the native driver is used.
- See [Wine Notes](Wine-Notes) and [Running on Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
